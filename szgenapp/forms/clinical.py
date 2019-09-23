from django.forms import ModelForm, BooleanField, HiddenInput
from django.forms.models import inlineformset_factory

from szgenapp.models.clinical import *


class ClinicalForm(ModelForm):
    class Meta:
        model = Clinical
        fields = '__all__'
        widgets = {'participant': HiddenInput()}


class DemographicForm(ModelForm):
    class Meta:
        model = Demographic
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class DiagnosisForm(ModelForm):
    dup_approx = BooleanField(initial=False, required=False)
    illness_duration_approx = BooleanField(initial=False, required=False)
    hospitalisation_number_approx = BooleanField(initial=False, required=False)

    class Meta:
        model = Diagnosis
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class MedicalHistoryForm(ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsGeneralForm(ModelForm):
    class Meta:
        model = SymptomsGeneral
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsDelusionForm(ModelForm):
    class Meta:
        model = SymptomsDelusion
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsHallucinationForm(ModelForm):
    class Meta:
        model = SymptomsHallucination
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsDepressionForm(ModelForm):
    class Meta:
        model = SymptomsDepression
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsBehaviourForm(ModelForm):
    class Meta:
        model = SymptomsBehaviour
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


class SymptomsManiaForm(ModelForm):
    class Meta:
        model = SymptomsMania
        fields = '__all__'
        widgets = {'clinical': HiddenInput()}


DemographicFormset = inlineformset_factory(Clinical, Demographic, form=DemographicForm, extra=1, can_delete=False)
DiagnosisFormset = inlineformset_factory(Clinical, Diagnosis, form=DiagnosisForm, extra=1, can_delete=False)
MedicalHistoryFormset = inlineformset_factory(Clinical, MedicalHistory, form=MedicalHistoryForm, extra=1,
                                              can_delete=False)
SymptomsGeneralFormset = inlineformset_factory(Clinical, SymptomsGeneral, form=SymptomsGeneralForm, extra=1,
                                               can_delete=False)
SymptomsBehaviourFormset = inlineformset_factory(Clinical, SymptomsBehaviour, form=SymptomsBehaviourForm, extra=1,
                                                 can_delete=False)
SymptomsDepressionFormset = inlineformset_factory(Clinical, SymptomsDepression, form=SymptomsDepressionForm, extra=1,
                                                  can_delete=False)
SymptomsHallucinationFormset = inlineformset_factory(Clinical, SymptomsHallucination, form=SymptomsHallucinationForm,
                                                     extra=1, can_delete=False)
SymptomsDelusionFormset = inlineformset_factory(Clinical, SymptomsDelusion, form=SymptomsDelusionForm, extra=1,
                                                can_delete=False)
SymptomsManiaFormset = inlineformset_factory(Clinical, SymptomsMania, form=SymptomsManiaForm, extra=1, can_delete=False)
