from django import forms
from django.forms import ModelForm, Form, ChoiceField
from .models import Study


class StudyForm(ModelForm):
  class Meta:
      model = Study
      fields = '__all__'