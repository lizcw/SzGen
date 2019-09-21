from django.forms import ModelForm

from szgenapp.models import Study


class StudyForm(ModelForm):
  class Meta:
      model = Study
      fields = '__all__'