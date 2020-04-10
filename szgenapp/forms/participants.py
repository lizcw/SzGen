from django.forms import ModelForm, CharField

from szgenapp.models.participants import StudyParticipant


class StudyParticipantForm(ModelForm):
    class Meta:
        model = StudyParticipant
        fields = ['study', 'fullnumber', 'family', 'individual', 'status', 'country', 'accessid',
                  'alphacode', 'secondaryid', 'npid', 'district', 'notes']


class StudyParticipantRelatedForm(ModelForm):
    related_participant = CharField(required=True, min_length=2, max_length=50, strip=True, label="Related Participant Full Number")
    class Meta:
        model = StudyParticipant
        fields = ['fullnumber', 'related_participant']
