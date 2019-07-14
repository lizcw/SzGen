from django import forms
from django.forms import ModelForm, Form, ChoiceField
from szgenapp.models.participants import Participant


class ParticipantForm(ModelForm):
  class Meta:
      model = Participant
      fields = '__all__'