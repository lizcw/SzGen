from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class HelpDetail(LoginRequiredMixin, TemplateView):
    """
    Help Information for Users
    """
    context_object_name = 'help'
    template_name = 'help/help-view.html'