from django import forms
from django.forms import ModelForm, Form, ChoiceField, inlineformset_factory
from szgenapp.models.participants import Participant, StudyParticipant


class ParticipantForm(ModelForm):
  class Meta:
      model = Participant
      fields = ['status', 'country', 'accessid', 'alphacode', 'secondaryid', 'npid']


class StudyParticipantForm(ModelForm):
  class Meta:
      model = StudyParticipant
      fields = ['study', 'family', 'individual', 'fullnumber', 'district']

StudyParticipantFormset = inlineformset_factory(Participant, StudyParticipant,
                                                form=StudyParticipantForm, extra=1,
                                                can_delete=False, max_num=1)