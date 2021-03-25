from django.test import TestCase
from server.user.forms import UserSettingsForm


from server.schema.utils import form_to_schema

class SchemaTestCase(TestCase):
    # TODO asserts
    def test_basic_form(self):
        form = UserSettingsForm()
        schema = form_to_schema(form)
        properties = schema['properties']
