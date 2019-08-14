from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from szgenapp.models.clinical import *


class ClinicalForm(ModelForm):
    class Meta:
        model = Clinical
        fields = '__all__'


class DemographicForm(ModelForm):
    class Meta:
        model = Demographic
        fields = '__all__'


class DiagnosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class MedicalHistoryForm(ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


class SymptomsGeneralForm(ModelForm):
    class Meta:
        model = SymptomsGeneral
        fields = '__all__'


class SymptomsDelusionForm(ModelForm):
    class Meta:
        model = SymptomsDelusion
        fields = '__all__'


class SymptomsHallucinationForm(ModelForm):
    class Meta:
        model = SymptomsHallucination
        fields = '__all__'


class SymptomsDepressionForm(ModelForm):
    class Meta:
        model = SymptomsDepression
        fields = '__all__'


class SymptomsBehaviourForm(ModelForm):
    class Meta:
        model = SymptomsBehaviour
        fields = '__all__'


DemographicFormset = inlineformset_factory(Clinical, Demographic, form=DemographicForm, extra=1)
DiagnosisFormset = inlineformset_factory(Clinical, Diagnosis, form=DiagnosisForm, extra=1)
MedicalHistoryFormset = inlineformset_factory(Clinical, MedicalHistory, form=MedicalHistoryForm, extra=1)
SymptomsGeneralFormset = inlineformset_factory(Clinical, SymptomsGeneral, form=SymptomsGeneralForm, extra=1)
SymptomsBehaviourFormset = inlineformset_factory(Clinical, SymptomsBehaviour, form=SymptomsBehaviourForm, extra=1)
SymptomsDepressionFormset = inlineformset_factory(Clinical, SymptomsDepression, form=SymptomsDepressionForm, extra=1)
SymptomsHallucinationFormset = inlineformset_factory(Clinical, SymptomsHallucination, form=SymptomsHallucinationForm, extra=1)
SymptomsDelusionFormset = inlineformset_factory(Clinical, SymptomsDelusion, form=SymptomsDelusionForm, extra=1)
