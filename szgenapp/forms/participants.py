from django.forms import ModelForm

from szgenapp.models.participants import StudyParticipant


class StudyParticipantForm(ModelForm):
    class Meta:
        model = StudyParticipant
        fields = ['study', 'fullnumber', 'family', 'individual', 'status', 'country', 'accessid',
                  'alphacode', 'secondaryid', 'npid', 'district', 'notes']


class StudyParticipantRelatedForm(ModelForm):
    class Meta:
        model = StudyParticipant
        fields = ['fullnumber', 'related_participant']
