# loosely based on: https://github.com/Cahersan/django-schemulator
from collections import OrderedDict
from django import forms
from django.db.models.fields.files import ImageFieldFile

# django keywords to rjsf keywords
KEYWORDS = {
  #Base keywords
  "label": "title",
  "help_text": "description",
  "initial": "default",
  "required": "required",

  #String/number type-specific keywords
  "max_length": "maxLength",
  "min_length": "minLength",

  #Numerical type-specific keywords
  "min_value": "minimum",
  "max_value": "maximum",
}

# django fields to rjsf types
FIELD_TO_TYPE = {
  'IntegerField': 'integer',
  'BooleanField': 'boolean',
  'BooleanField': 'number',
  'TypedChoiceField': '',
  'ModelChoiceField': 'integer',
}

# django fields to rjsf formats
FIELD_TO_FORMAT = {
  'EmailField': 'email',
  'DateTimeField': 'date-time',
}


def field_to_schema(field):
  field_type = field.__class__.__name__
  schema = {
    'type': FIELD_TO_TYPE.get(field_type, 'string'),
  }

  # Setup of JSON Schema keywords
  for (field_attr, schema_attr) in KEYWORDS.items():
    if hasattr(field, field_attr):
      schema[schema_attr] = getattr(field, field_attr)

  # RJSF doesn't like minLength = null
  if schema.get('minLength', 0) is None:
    schema.pop('minLength')

  for field_attr in ['maxLength', 'title', 'maximum', 'minimum', 'default']:
    if schema.get(field_attr, '') is None:
      schema.pop(field_attr)

  # Set __django_form_field_cls keyword
  schema['__django_form_field_cls'] = field_type
  schema['__widget'] = field.widget.__class__.__name__

  return schema


def form_to_schema(form):
  schema = {
    'type': 'object',
    'properties': OrderedDict([
      (name, field_to_schema(field))
      for (name, field) in form.fields.items()
    ]),
    'required': []
  }

  for name, field in schema['properties'].items():
    if field.pop('required', None):
      schema['required'].append(name)
    if getattr(form, 'instance', None):
      if hasattr(form.instance, name) and getattr(form.instance, name) != None:
        value = getattr(form.instance, name)
        if hasattr(value, 'pk'):
          value = value.pk
        schema['properties'][name]['default'] = value

  return schema
