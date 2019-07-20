from django import forms
from django.forms import ModelForm, Form, ChoiceField
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from szgenapp.models.datasets import DatasetRow, Dataset, DatasetFile


class DatasetForm(ModelForm):
    """
    Base formset for editing Datasets and Dataset Files
    """

    # def add_fields(self, form, index):
    #     super(DatasetForm, self).add_fields(form, index)
    #     form.nested = DatasetFileFormset(instance=form.instance,
    #                                      data=form.data if form.is_bound else None,
    #                                      prefix='dsfile-%s-%s' % (
    #                                      form.prefix, DatasetFileFormset.get_default_prefix()),
    #                                      )
    # def is_valid(self):
    #     result = super().is_valid()
    #
    #     if self.is_bound:
    #         for form in self.forms:
    #             if hasattr(form, 'nested'):
    #                 result = result and form.nested.is_valid()
    #     return result
    #
    # def save(self, commit=True):
    #     """
    #     Also save the nested formsets.
    #     """
    #     result = super().save(commit=commit)
    #
    #     for form in self.forms:
    #         if hasattr(form, 'nested'):
    #             if not self._should_delete_form(form):
    #                 form.nested.save(commit=commit)
    #
    #     return result

    class Meta:
        model = Dataset
        fields = '__all__'

class DatasetFileForm(ModelForm):

    class Meta:
        model = DatasetFile
        fields = '__all__'

DatasetFileFormset = inlineformset_factory(Dataset, DatasetFile, form=DatasetFileForm, extra=1)
# DatasetRowFormset = inlineformset_factory(Dataset, DatasetRow, extra=1)
