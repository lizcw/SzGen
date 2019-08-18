from django.forms import ModelForm, modelform_factory
from django.forms.models import inlineformset_factory

from szgenapp.models.clinical import *


class ClinicalForm(ModelForm):
    class Meta:
        model = Clinical
        fields = ['participant', ]


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


DemographicFormset = modelform_factory(Demographic, form=DemographicForm)
DiagnosisFormset = modelform_factory(Diagnosis, form=DiagnosisForm)
MedicalHistoryFormset = modelform_factory(MedicalHistory, form=MedicalHistoryForm)
SymptomsGeneralFormset = modelform_factory(SymptomsGeneral, form=SymptomsGeneralForm)
SymptomsBehaviourFormset = modelform_factory(SymptomsBehaviour, form=SymptomsBehaviourForm)
SymptomsDepressionFormset = modelform_factory(SymptomsDepression, form=SymptomsDepressionForm)
SymptomsHallucinationFormset = modelform_factory(SymptomsHallucination, form=SymptomsHallucinationForm)
SymptomsDelusionFormset = modelform_factory(SymptomsDelusion, form=SymptomsDelusionForm)
