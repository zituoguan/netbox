import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.module_loading import import_string
from django_rq import get_queue

from core.models import Job
from netbox.config import get_config
from netbox.constants import RQ_QUEUE_DEFAULT
from netbox.registry import registry
from utilities.api import get_serializer_for_model
from utilities.rqworker import get_rq_retry
from utilities.utils import serialize_object
from .choices import *
from .models import EventRule, ScriptModule

logger = logging.getLogger('netbox.events_processor')


def serialize_for_event(instance):
    """
    Return a serialized representation of the given instance suitable for use in a queued event.
    """
    serializer_class = get_serializer_for_model(instance.__class__)
    serializer_context = {
        'request': None,
    }
    serializer = serializer_class(instance, context=serializer_context)

    return serializer.data


def get_snapshots(instance, action):
    snapshots = {
        'prechange': getattr(instance, '_prechange_snapshot', None),
        'postchange': None,
    }
    if action != ObjectChangeActionChoices.ACTION_DELETE:
        # Use model's serialize_object() method if defined; fall back to serialize_object() utility function
        if hasattr(instance, 'serialize_object'):
            snapshots['postchange'] = instance.serialize_object()
        else:
            snapshots['postchange'] = serialize_object(instance)

    return snapshots


def enqueue_object(queue, instance, user, request_id, action):
    """
    Enqueue a serialized representation of a created/updated/deleted object for the processing of
    events once the request has completed.
    """
    # Determine whether this type of object supports event rules
    app_label = instance._meta.app_label
    model_name = instance._meta.model_name
    if model_name not in registry['model_features']['event_rules'].get(app_label, []):
        return

    queue.append({
        'content_type': ContentType.objects.get_for_model(instance),
        'object_id': instance.pk,
        'event': action,
        'data': serialize_for_event(instance),
        'snapshots': get_snapshots(instance, action),
        'username': user.username,
        'request_id': request_id
    })


def process_event_rules(event_rules, model_name, event, data, username, snapshots=None, request_id=None):
    try:
        user = get_user_model().objects.get(username=username)
    except ObjectDoesNotExist:
        user = None

    for event_rule in event_rules:

        # Evaluate event rule conditions (if any)
        if not event_rule.eval_conditions(data):
            continue

        # Webhooks
        if event_rule.action_type == EventRuleActionChoices.WEBHOOK:

            # Select the appropriate RQ queue
            queue_name = get_config().QUEUE_MAPPINGS.get('webhook', RQ_QUEUE_DEFAULT)
            rq_queue = get_queue(queue_name)

            # Compile the task parameters
            params = {
                "event_rule": event_rule,
                "model_name": model_name,
                "event": event,
                "data": data,
                "snapshots": snapshots,
                "timestamp": timezone.now().isoformat(),
                "username": username,
                "retry": get_rq_retry()
            }
            if snapshots:
                params["snapshots"] = snapshots
            if request_id:
                params["request_id"] = request_id

            # Enqueue the task
            rq_queue.enqueue(
                "extras.webhooks.send_webhook",
                **params
            )

        # Scripts
        elif event_rule.action_type == EventRuleActionChoices.SCRIPT:
            # Resolve the script from action parameters
            script_module = event_rule.action_object
            script_name = event_rule.action_parameters['script_name']
            script = script_module.scripts[script_name]()

            # Enqueue a Job to record the script's execution
            Job.enqueue(
                "extras.scripts.run_script",
                instance=script_module,
                name=script.class_name,
                user=user,
                data=data
            )

        else:
            raise ValueError(f"Unknown action type for an event rule: {event_rule.action_type}")


def process_event_queue(events):
    """
    Flush a list of object representation to RQ for EventRule processing.
    """
    events_cache = {
        'type_create': {},
        'type_update': {},
        'type_delete': {},
    }

    for data in events:
        action_flag = {
            ObjectChangeActionChoices.ACTION_CREATE: 'type_create',
            ObjectChangeActionChoices.ACTION_UPDATE: 'type_update',
            ObjectChangeActionChoices.ACTION_DELETE: 'type_delete',
        }[data['event']]
        content_type = data['content_type']

        # Cache applicable Event Rules
        if content_type not in events_cache[action_flag]:
            events_cache[action_flag][content_type] = EventRule.objects.filter(
                **{action_flag: True},
                content_types=content_type,
                enabled=True
            )
        event_rules = events_cache[action_flag][content_type]

        process_event_rules(
            event_rules, content_type.model, data['event'], data['data'], data['username'],
            snapshots=data['snapshots'], request_id=data['request_id']
        )


def flush_events(queue):
    """
    Flush a list of object representation to RQ for webhook processing.
    """
    if queue:
        for name in settings.EVENTS_PIPELINE:
            try:
                func = import_string(name)
                func(queue)
            except Exception as e:
                logger.error(f"Cannot import events pipeline {name} error: {e}")
