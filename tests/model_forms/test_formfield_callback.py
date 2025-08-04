from django import forms
from django.db import models
from django.forms import modelform_factory
from django.test import TestCase


class MyModel(models.Model):
    active = models.BooleanField()
    name = models.CharField(max_length=64, blank=True, null=True)


def all_required(field, **kwargs):
    formfield = field.formfield(**kwargs)
    formfield.required = True
    return formfield


class FormWithCallbackInMeta(forms.ModelForm):
    formfield_callback = all_required

    class Meta:
        model = MyModel
        formfield_callback = all_required
        fields = ['active', 'name']


class FormWithCallbackInClass(forms.ModelForm):
    formfield_callback = all_required

    class Meta:
        model = MyModel
        fields = ['active', 'name']


class FormFieldCallbackMetaTests(TestCase):
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