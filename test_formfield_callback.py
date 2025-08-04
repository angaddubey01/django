import os
import sys
import unittest

from django.conf import settings

# Set up minimal Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
    )

# Setup Django
import django
django.setup()

from django import forms
from django.db import models
from django.forms import modelform_factory
from django.test import SimpleTestCase

# Define a test model
class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        # This is a fake model, so we don't want to create a table for it
        app_label = 'modelforms_test'
        

def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield


class FormWithCallbackInMeta(forms.ModelForm):
    class Meta:
        model = MyModel
        formfield_callback = all_required
        fields = ['active', 'name']


# Define a class with formfield_callback as a class attribute
def create_form_with_callback_as_class_attr():
    class FormWithCallbackInClass(forms.ModelForm):
        # Define this explicitly to avoid it being lost
        formfield_callback = all_required

        class Meta:
            model = MyModel
            fields = ['active', 'name']

    # Verify the attribute is set
    setattr(FormWithCallbackInClass, 'formfield_callback', all_required)
    return FormWithCallbackInClass

FormWithCallbackInClass = create_form_with_callback_as_class_attr()


class DebugFormFieldCallbackTests(unittest.TestCase):
    def test_debug_callbacks(self):
        # Test Meta attribute
        FactoryForm1 = modelform_factory(MyModel, form=FormWithCallbackInMeta)
        print("=== Meta formfield_callback test ===")
        print("Meta.formfield_callback exists:", hasattr(FactoryForm1.Meta, 'formfield_callback'))
        print("Form.formfield_callback exists:", hasattr(FactoryForm1, 'formfield_callback'))
        form1 = FactoryForm1()
        print("name.required:", form1.fields['name'].required)
        print("active.required:", form1.fields['active'].required)

        # Test class attribute
        print("\n=== Debug FormWithCallbackInClass ===")
        print("FormWithCallbackInClass.__dict__:", [k for k in FormWithCallbackInClass.__dict__.keys()])
        print("Class callback exists on source:", hasattr(FormWithCallbackInClass, 'formfield_callback'))
        print("Class callback value:", getattr(FormWithCallbackInClass, 'formfield_callback', None))
        
        FactoryForm2 = modelform_factory(MyModel, form=FormWithCallbackInClass)
        print("\n=== Class formfield_callback test ===")
        print("Meta.formfield_callback exists:", hasattr(FactoryForm2.Meta, 'formfield_callback'))
        print("Form.formfield_callback exists:", hasattr(FactoryForm2, 'formfield_callback'))
        print("FactoryForm2.__dict__:", [k for k in FactoryForm2.__dict__.keys()])
        form2 = FactoryForm2()
        print("name.required:", form2.fields['name'].required)
        print("active.required:", form2.fields['active'].required)


class FormFieldCallbackTests(SimpleTestCase):
    def test_formfield_callback_in_meta_is_used(self):
        """
        When a formfield_callback is specified in the Meta class of a form,
        it should be used when creating a factory form based on that form.
        """
        FactoryForm = modelform_factory(MyModel, form=FormWithCallbackInMeta)
        form = FactoryForm()
        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['active'].required)

    def test_formfield_callback_in_class_is_used(self):
        """
        When a formfield_callback is specified as a class attribute,
        it should be used when creating a factory form based on that form.
        """
        FactoryForm = modelform_factory(MyModel, form=FormWithCallbackInClass)
        form = FactoryForm()
        self.assertTrue(form.fields['name'].required)
        self.assertTrue(form.fields['active'].required)

    def test_formfield_callback_in_factory_overrides_meta(self):
        """
        When a formfield_callback is provided to modelform_factory, it should
        override any formfield_callback specified in the Meta class.
        """
        def make_optional(field, **kwargs):
            formfield = field.formfield(**kwargs)
            formfield.required = False
            return formfield

        FactoryForm = modelform_factory(
            MyModel,
            form=FormWithCallbackInMeta,
            formfield_callback=make_optional
        )
        form = FactoryForm()
        self.assertFalse(form.fields['name'].required)
        self.assertFalse(form.fields['active'].required)


if __name__ == '__main__':
    # Run the tests
    unittest.main()