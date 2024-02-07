import datetime
import decimal
import json
import re
from decimal import Decimal
from itertools import count, groupby

import bleach
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.db.models import Count, ManyToOneRel, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.http import QueryDict
from django.utils import timezone
from django.utils.datastructures import MultiValueDict
from django.utils.html import escape
from django.utils.timezone import localtime
from jinja2.sandbox import SandboxedEnvironment
from mptt.models import MPTTModel

from dcim.choices import CableLengthUnitChoices, WeightUnitChoices
from extras.utils import is_taggable
from netbox.config import get_config
from netbox.plugins import PluginConfig
from urllib.parse import urlencode
from utilities.constants import HTTP_REQUEST_META_SAFE_COPY


def title(value):
    """
    Improved implementation of str.title(); retains all existing uppercase letters.
    """
    return ' '.join([w[0].upper() + w[1:] for w in str(value).split()])


def get_viewname(model, action=None, rest_api=False):
    """
    Return the view name for the given model and action, if valid.

    :param model: The model or instance to which the view applies
    :param action: A string indicating the desired action (if any); e.g. "add" or "list"
    :param rest_api: A boolean indicating whether this is a REST API view
    """
    is_plugin = isinstance(model._meta.app_config, PluginConfig)
    app_label = model._meta.app_label
    model_name = model._meta.model_name

    if rest_api:
        if is_plugin:
            viewname = f'plugins-api:{app_label}-api:{model_name}'
        else:
            # Alter the app_label for group and user model_name to point to users app
            if app_label == 'auth' and model_name in ['group', 'user']:
                app_label = 'users'
            if app_label == 'users' and model._meta.proxy and model_name in ['netboxuser', 'netboxgroup']:
                model_name = model._meta.proxy_for_model._meta.model_name

            viewname = f'{app_label}-api:{model_name}'
        # Append the action, if any
        if action:
            viewname = f'{viewname}-{action}'

    else:
        viewname = f'{app_label}:{model_name}'
        # Prepend the plugins namespace if this is a plugin model
        if is_plugin:
            viewname = f'plugins:{viewname}'
        # Append the action, if any
        if action:
            viewname = f'{viewname}_{action}'

    return viewname


def csv_format(data):
    """
    Encapsulate any data which contains a comma within double quotes.
    """
    csv = []
    for value in data:

        # Represent None or False with empty string
        if value is None or value is False:
            csv.append('')
            continue

        # Convert dates to ISO format
        if isinstance(value, (datetime.date, datetime.datetime)):
            value = value.isoformat()

        # Force conversion to string first so we can check for any commas
        if not isinstance(value, str):
            value = '{}'.format(value)

        # Double-quote the value if it contains a comma or line break
        if ',' in value or '\n' in value:
            value = value.replace('"', '""')  # Escape double-quotes
            csv.append('"{}"'.format(value))
        else:
            csv.append('{}'.format(value))

    return ','.join(csv)


def foreground_color(bg_color, dark='000000', light='ffffff'):
    """
    Return the ideal foreground color (dark or light) for a given background color in hexadecimal RGB format.

    :param dark: RBG color code for dark text
    :param light: RBG color code for light text
    """
    THRESHOLD = 150
    bg_color = bg_color.strip('#')
    r, g, b = [int(bg_color[c:c + 2], 16) for c in (0, 2, 4)]
    if r * 0.299 + g * 0.587 + b * 0.114 > THRESHOLD:
        return dark
    else:
        return light


def dynamic_import(name):
    """
    Dynamically import a class from an absolute path string
    """
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def count_related(model, field):
    """
    Return a Subquery suitable for annotating a child object count.
    """
    subquery = Subquery(
        model.objects.filter(
            **{field: OuterRef('pk')}
        ).order_by().values(
            field
        ).annotate(
            c=Count('*')
        ).values('c')
    )

    return Coalesce(subquery, 0)


def serialize_object(obj, resolve_tags=True, extra=None, exclude=None):
    """
    Return a generic JSON representation of an object using Django's built-in serializer. (This is used for things like
    change logging, not the REST API.) Optionally include a dictionary to supplement the object data. A list of keys
    can be provided to exclude them from the returned dictionary. Private fields (prefaced with an underscore) are
    implicitly excluded.

    Args:
        obj: The object to serialize
        resolve_tags: If true, any assigned tags will be represented by their names
        extra: Any additional data to include in the serialized output. Keys provided in this mapping will
            override object attributes.
        exclude: An iterable of attributes to exclude from the serialized output
    """
    json_str = serializers.serialize('json', [obj])
    data = json.loads(json_str)[0]['fields']
    exclude = exclude or []

    # Exclude any MPTTModel fields
    if issubclass(obj.__class__, MPTTModel):
        for field in ['level', 'lft', 'rght', 'tree_id']:
            data.pop(field)

    # Include custom_field_data as "custom_fields"
    if hasattr(obj, 'custom_field_data'):
        data['custom_fields'] = data.pop('custom_field_data')

    # Resolve any assigned tags to their names. Check for tags cached on the instance;
    # fall back to using the manager.
    if resolve_tags and is_taggable(obj):
        tags = getattr(obj, '_tags', None) or obj.tags.all()
        data['tags'] = sorted([tag.name for tag in tags])

    # Skip excluded and private (prefixes with an underscore) attributes
    for key in list(data.keys()):
        if key in exclude or (isinstance(key, str) and key.startswith('_')):
            data.pop(key)

    # Append any extra data
    if extra is not None:
        data.update(extra)

    return data


def deserialize_object(model, fields, pk=None):
    """
    Instantiate an object from the given model and field data. Functions as
    the complement to serialize_object().
    """
    content_type = ContentType.objects.get_for_model(model)
    if 'custom_fields' in fields:
        fields['custom_field_data'] = fields.pop('custom_fields')
    data = {
        'model': '.'.join(content_type.natural_key()),
        'pk': pk,
        'fields': fields,
    }
    instance = list(serializers.deserialize('python', [data]))[0]

    return instance


def dict_to_filter_params(d, prefix=''):
    """
    Translate a dictionary of attributes to a nested set of parameters suitable for QuerySet filtering. For example:

        {
            "name": "Foo",
            "rack": {
                "facility_id": "R101"
            }
        }

    Becomes:

        {
            "name": "Foo",
            "rack__facility_id": "R101"
        }

    And can be employed as filter parameters:

        Device.objects.filter(**dict_to_filter(attrs_dict))
    """
    params = {}
    for key, val in d.items():
        k = prefix + key
        if isinstance(val, dict):
            params.update(dict_to_filter_params(val, k + '__'))
        else:
            params[k] = val
    return params


def dict_to_querydict(d, mutable=True):
    """
    Create a QueryDict instance from a regular Python dictionary.
    """
    qd = QueryDict(mutable=True)
    for k, v in d.items():
        item = MultiValueDict({k: v}) if isinstance(v, (list, tuple, set)) else {k: v}
        qd.update(item)
    if not mutable:
        qd._mutable = False
    return qd


def normalize_querydict(querydict):
    """
    Convert a QueryDict to a normal, mutable dictionary, preserving list values. For example,

        QueryDict('foo=1&bar=2&bar=3&baz=')

    becomes:

        {'foo': '1', 'bar': ['2', '3'], 'baz': ''}

    This function is necessary because QueryDict does not provide any built-in mechanism which preserves multiple
    values.
    """
    return {
        k: v if len(v) > 1 else v[0] for k, v in querydict.lists()
    }


def deepmerge(original, new):
    """
    Deep merge two dictionaries (new into original) and return a new dict
    """
    merged = dict(original)
    for key, val in new.items():
        if key in original and isinstance(original[key], dict) and val and isinstance(val, dict):
            merged[key] = deepmerge(original[key], val)
        else:
            merged[key] = val
    return merged


def drange(start, end, step=decimal.Decimal(1)):
    """
    Decimal-compatible implementation of Python's range()
    """
    start, end, step = decimal.Decimal(start), decimal.Decimal(end), decimal.Decimal(step)
    if start < end:
        while start < end:
            yield start
            start += step
    else:
        while start > end:
            yield start
            start += step


def to_meters(length, unit):
    """
    Convert the given length to meters.
    """
    try:
        if length < 0:
            raise ValueError("Length must be a positive number")
    except TypeError:
        raise TypeError(f"Invalid value '{length}' for length (must be a number)")

    valid_units = CableLengthUnitChoices.values()
    if unit not in valid_units:
        raise ValueError(f"Unknown unit {unit}. Must be one of the following: {', '.join(valid_units)}")

    if unit == CableLengthUnitChoices.UNIT_KILOMETER:
        return length * 1000
    if unit == CableLengthUnitChoices.UNIT_METER:
        return length
    if unit == CableLengthUnitChoices.UNIT_CENTIMETER:
        return length / 100
    if unit == CableLengthUnitChoices.UNIT_MILE:
        return length * Decimal(1609.344)
    if unit == CableLengthUnitChoices.UNIT_FOOT:
        return length * Decimal(0.3048)
    if unit == CableLengthUnitChoices.UNIT_INCH:
        return length * Decimal(0.0254)
    raise ValueError(f"Unknown unit {unit}. Must be 'km', 'm', 'cm', 'mi', 'ft', or 'in'.")


def to_grams(weight, unit):
    """
    Convert the given weight to kilograms.
    """
    try:
        if weight < 0:
            raise ValueError("Weight must be a positive number")
    except TypeError:
        raise TypeError(f"Invalid value '{weight}' for weight (must be a number)")

    valid_units = WeightUnitChoices.values()
    if unit not in valid_units:
        raise ValueError(f"Unknown unit {unit}. Must be one of the following: {', '.join(valid_units)}")

    if unit == WeightUnitChoices.UNIT_KILOGRAM:
        return weight * 1000
    if unit == WeightUnitChoices.UNIT_GRAM:
        return weight
    if unit == WeightUnitChoices.UNIT_POUND:
        return weight * Decimal(453.592)
    if unit == WeightUnitChoices.UNIT_OUNCE:
        return weight * Decimal(28.3495)
    raise ValueError(f"Unknown unit {unit}. Must be 'kg', 'g', 'lb', 'oz'.")


def render_jinja2(template_code, context):
    """
    Render a Jinja2 template with the provided context. Return the rendered content.
    """
    environment = SandboxedEnvironment()
    environment.filters.update(get_config().JINJA2_FILTERS)
    return environment.from_string(source=template_code).render(**context)


def prepare_cloned_fields(instance):
    """
    Generate a QueryDict comprising attributes from an object's clone() method.
    """
    # Generate the clone attributes from the instance
    if not hasattr(instance, 'clone'):
        return QueryDict(mutable=True)
    attrs = instance.clone()

    # Prepare querydict parameters
    params = []
    for key, value in attrs.items():
        if type(value) in (list, tuple):
            params.extend([(key, v) for v in value])
        elif value not in (False, None):
            params.append((key, value))
        else:
            params.append((key, ''))

    # Return a QueryDict with the parameters
    return QueryDict(urlencode(params), mutable=True)


def shallow_compare_dict(source_dict, destination_dict, exclude=tuple()):
    """
    Return a new dictionary of the different keys. The values of `destination_dict` are returned. Only the equality of
    the first layer of keys/values is checked. `exclude` is a list or tuple of keys to be ignored.
    """
    difference = {}

    for key, value in destination_dict.items():
        if key in exclude:
            continue
        if source_dict.get(key) != value:
            difference[key] = value

    return difference


def flatten_dict(d, prefix='', separator='.'):
    """
    Flatten netsted dictionaries into a single level by joining key names with a separator.

    :param d: The dictionary to be flattened
    :param prefix: Initial prefix (if any)
    :param separator: The character to use when concatenating key names
    """
    ret = {}
    for k, v in d.items():
        key = separator.join([prefix, k]) if prefix else k
        if type(v) is dict:
            ret.update(flatten_dict(v, prefix=key, separator=separator))
        else:
            ret[key] = v
    return ret


def array_to_ranges(array):
    """
    Convert an arbitrary array of integers to a list of consecutive values. Nonconsecutive values are returned as
    single-item tuples. For example:
        [0, 1, 2, 10, 14, 15, 16] => [(0, 2), (10,), (14, 16)]"
    """
    group = (
        list(x) for _, x in groupby(sorted(array), lambda x, c=count(): next(c) - x)
    )
    return [
        (g[0], g[-1])[:len(g)] for g in group
    ]


def array_to_string(array):
    """
    Generate an efficient, human-friendly string from a set of integers. Intended for use with ArrayField.
    For example:
        [0, 1, 2, 10, 14, 15, 16] => "0-2, 10, 14-16"
    """
    ret = []
    ranges = array_to_ranges(array)
    for value in ranges:
        if len(value) == 1:
            ret.append(str(value[0]))
        else:
            ret.append(f'{value[0]}-{value[1]}')
    return ', '.join(ret)


def content_type_name(ct, include_app=True):
    """
    Return a human-friendly ContentType name (e.g. "DCIM > Site").
    """
    try:
        meta = ct.model_class()._meta
        app_label = title(meta.app_config.verbose_name)
        model_name = title(meta.verbose_name)
        if include_app:
            return f'{app_label} > {model_name}'
        return model_name
    except AttributeError:
        # Model no longer exists
        return f'{ct.app_label} > {ct.model}'


def content_type_identifier(ct):
    """
    Return a "raw" ContentType identifier string suitable for bulk import/export (e.g. "dcim.site").
    """
    return f'{ct.app_label}.{ct.model}'


#
# Fake request object
#

class NetBoxFakeRequest:
    """
    A fake request object which is explicitly defined at the module level so it is able to be pickled. It simply
    takes what is passed to it as kwargs on init and sets them as instance variables.
    """
    def __init__(self, _dict):
        self.__dict__ = _dict


def copy_safe_request(request):
    """
    Copy selected attributes from a request object into a new fake request object. This is needed in places where
    thread safe pickling of the useful request data is needed.
    """
    meta = {
        k: request.META[k]
        for k in HTTP_REQUEST_META_SAFE_COPY
        if k in request.META and isinstance(request.META[k], str)
    }
    return NetBoxFakeRequest({
        'META': meta,
        'COOKIES': request.COOKIES,
        'POST': request.POST,
        'GET': request.GET,
        'FILES': request.FILES,
        'user': request.user,
        'path': request.path,
        'id': getattr(request, 'id', None),  # UUID assigned by middleware
    })


def clean_html(html, schemes):
    """
    Sanitizes HTML based on a whitelist of allowed tags and attributes.
    Also takes a list of allowed URI schemes.
    """

    ALLOWED_TAGS = {
        "div", "pre", "code", "blockquote", "del",
        "hr", "h1", "h2", "h3", "h4", "h5", "h6",
        "ul", "ol", "li", "p", "br",
        "strong", "em", "a", "b", "i", "img",
        "table", "thead", "tbody", "tr", "th", "td",
        "dl", "dt", "dd",
    }

    ALLOWED_ATTRIBUTES = {
        "div": ['class'],
        "h1": ["id"], "h2": ["id"], "h3": ["id"], "h4": ["id"], "h5": ["id"], "h6": ["id"],
        "a": ["href", "title"],
        "img": ["src", "title", "alt"],
        "th": ["align"],
        "td": ["align"],
    }

    return bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=schemes
    )


def highlight_string(value, highlight, trim_pre=None, trim_post=None, trim_placeholder='...'):
    """
    Highlight a string within a string and optionally trim the pre/post portions of the original string.

    Args:
        value: The body of text being searched against
        highlight: The string of compiled regex pattern to highlight in `value`
        trim_pre: Maximum length of pre-highlight text to include
        trim_post: Maximum length of post-highlight text to include
        trim_placeholder: String value to swap in for trimmed pre/post text
    """
    # Split value on highlight string
    try:
        if type(highlight) is re.Pattern:
            pre, match, post = highlight.split(value, maxsplit=1)
        else:
            highlight = re.escape(highlight)
            pre, match, post = re.split(fr'({highlight})', value, maxsplit=1, flags=re.IGNORECASE)
    except ValueError as e:
        # Match not found
        return escape(value)

    # Trim pre/post sections to length
    if trim_pre and len(pre) > trim_pre:
        pre = trim_placeholder + pre[-trim_pre:]
    if trim_post and len(post) > trim_post:
        post = post[:trim_post] + trim_placeholder

    return f'{escape(pre)}<mark>{escape(match)}</mark>{escape(post)}'


def local_now():
    """
    Return the current date & time in the system timezone.
    """
    return localtime(timezone.now())


def get_related_models(model, ordered=True):
    """
    Return a list of all models which have a ForeignKey to the given model and the name of the field. For example,
    `get_related_models(Tenant)` will return all models which have a ForeignKey relationship to Tenant.
    """
    related_models = [
        (field.related_model, field.remote_field.name)
        for field in model._meta.related_objects
        if type(field) is ManyToOneRel
    ]

    if ordered:
        return sorted(related_models, key=lambda x: x[0]._meta.verbose_name.lower())

    return related_models
