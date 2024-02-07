import json

from django import forms
from django.db.models import Count
from django.forms.fields import JSONField as _JSONField, InvalidJSONInput
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from netaddr import AddrFormatError, EUI

from utilities.forms import widgets
from utilities.validators import EnhancedURLValidator

__all__ = (
    'ColorField',
    'CommentField',
    'JSONField',
    'LaxURLField',
    'MACAddressField',
    'SlugField',
    'TagFilterField',
)


class CommentField(forms.CharField):
    """
    A textarea with support for Markdown rendering. Exists mostly just to add a standard `help_text`.
    """
    widget = widgets.MarkdownWidget
    label = _('Comments')
    help_text = _(
        '<i class="mdi mdi-information-outline"></i> '
        '<a href="{url}" target="_blank" tabindex="-1">Markdown</a> syntax is supported'
    ).format(url=static('docs/reference/markdown/'))

    def __init__(self, *, label=label, help_text=help_text, required=False, **kwargs):
        super().__init__(label=label, help_text=help_text, required=required, **kwargs)


class SlugField(forms.SlugField):
    """
    Extend Django's built-in SlugField to automatically populate from a field called `name` unless otherwise specified.

    Parameters:
        slug_source: Name of the form field from which the slug value will be derived
    """
    widget = widgets.SlugWidget
    label = _('Slug')
    help_text = _("URL-friendly unique shorthand")

    def __init__(self, *, slug_source='name', label=label, help_text=help_text, **kwargs):
        super().__init__(label=label, help_text=help_text, **kwargs)

        self.widget.attrs['slug-source'] = slug_source


class ColorField(forms.CharField):
    """
    A field which represents a color value in hexadecimal `RRGGBB` format. Utilizes NetBox's `ColorSelect` widget to
    render choices.
    """
    widget = widgets.ColorSelect


class TagFilterField(forms.MultipleChoiceField):
    """
    A filter field for the tags of a model. Only the tags used by a model are displayed.

    :param model: The model of the filter
    """

    def __init__(self, model, *args, **kwargs):
        def get_choices():
            tags = model.tags.annotate(
                count=Count('extras_taggeditem_items')
            ).order_by('name')
            return [
                (str(tag.slug), '{} ({})'.format(tag.name, tag.count)) for tag in tags
            ]

        # Choices are fetched each time the form is initialized
        super().__init__(label=_('Tags'), choices=get_choices, required=False, *args, **kwargs)


class LaxURLField(forms.URLField):
    """
    Modifies Django's built-in URLField to remove the requirement for fully-qualified domain names
    (e.g. http://myserver/ is valid)
    """
    default_validators = [EnhancedURLValidator()]


class JSONField(_JSONField):
    """
    Custom wrapper around Django's built-in JSONField to avoid presenting "null" as the default text.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.help_text:
            self.help_text = _('Enter context data in <a href="https://json.org/">JSON</a> format.')
            self.widget.attrs['placeholder'] = ''
            self.widget.attrs['class'] = 'font-monospace'

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        if value in ('', None):
            return ''
        if type(value) is str:
            try:
                value = json.loads(value, cls=self.decoder)
            except json.decoder.JSONDecodeError:
                return value
        return json.dumps(value, sort_keys=True, indent=4, ensure_ascii=False, cls=self.encoder)


class MACAddressField(forms.Field):
    """
    Validates a 48-bit MAC address.
    """
    widget = forms.CharField
    default_error_messages = {
        'invalid': _('MAC address must be in EUI-48 format'),
    }

    def to_python(self, value):
        value = super().to_python(value)

        # Validate MAC address format
        try:
            value = EUI(value.strip())
        except AddrFormatError:
            raise forms.ValidationError(self.error_messages['invalid'], code='invalid')

        return value
