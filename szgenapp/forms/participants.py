from django import forms
from django.forms import ModelForm, Form, ChoiceField
from szgenapp.models.participants import Participant, StudyParticipant


class ParticipantForm(ModelForm):
  class Meta:
      model = Participant
      fields = '__all__'


class StudyParticipantForm(ModelForm):
  class Meta:
      model = StudyParticipant
      fields = '__all__'