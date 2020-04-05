import logging

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView, CreateView, DetailView

from szgenapp.forms import WikiForm
from szgenapp.models import Wiki, Document

logger = logging.getLogger(__name__)


class HelpDetail(LoginRequiredMixin, TemplateView):
    """
    Help Information for Users
    """
    context_object_name = 'help'
    template_name = 'help/help-view.html'


class WikiList(LoginRequiredMixin, ListView):
    """
    List of Wiki Entries
    """
    model = Wiki
    template_name = 'help/wiki-list.html'
    queryset = Wiki.objects.all()
    context_object_name = 'wikis'

    def get_context_data(self, **kwargs):
        data = super(WikiList, self).get_context_data(**kwargs)
        data['documents'] = Document.objects.filter(help=True)
        return data


class WikiDetail(LoginRequiredMixin, DetailView):
    """
    Wiki Entry Information for Users
    """
    model = Wiki
    context_object_name = 'wiki'
    template_name = 'help/wiki-view.html'


class WikiCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Enter wiki data for new wiki
    """
    model = Wiki
    template_name = 'help/wiki-create.html'
    form_class = WikiForm
    permission_required = 'szgenapp.add_wiki'

    def form_valid(self, form):
        try:
            form.instance.author = self.request.user
            return super(WikiCreate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to create Wiki - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('wiki_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(WikiCreate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


class WikiUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Enter wiki data for new wiki
    """
    model = Wiki
    template_name = 'help/wiki-create.html'
    form_class = WikiForm
    permission_required = 'szgenapp.change_wiki'

    def form_valid(self, form):
        try:
            return super(WikiUpdate, self).form_valid(form)
        except IntegrityError as e:
            msg = 'Database Error: Unable to update Wiki - see Administrator: %s' % e
            form.add_error(None, msg)
            logger.error(msg)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('wiki_detail', args=[self.object.id])

    def get_initial(self, *args, **kwargs):
        initial = super(WikiUpdate, self).get_initial(**kwargs)
        initial['action'] = 'Create'
        return initial


class WikiDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Delete a Wiki and all participants
    """
    model = Wiki
    success_url = reverse_lazy("wiki")
    template_name = 'help/wiki-confirm-delete.html'
    permission_required = 'szgenapp.delete_wiki'
