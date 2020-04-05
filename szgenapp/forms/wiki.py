from django.forms import ModelForm

from szgenapp.models import Wiki


class WikiForm(ModelForm):
  class Meta:
      model = Wiki
      fields = ['title', 'content']