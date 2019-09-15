from axes.utils import reset
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url, render
from django.template import RequestContext
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from ipware.ip import get_ip

from szgenapp.forms.auth import UserUpdateForm

try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

# import the logging library
import logging

logger = logging.getLogger(__name__)

from szgenapp.forms.auth import AxesCaptchaForm


## Login

class LoginAppView(LoginView):
    """
    Provides the ability to login as a user with a username and password
    """
    template_name = 'app/index.html'
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    newUser = False

    # @method_decorator(axes_dispatch, name='dispatch')
    # @method_decorator(sensitive_post_parameters('password'))
    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    # def dispatch(self, request, *args, **kwargs):
    #     # Sets a test cookie to make sure the user has cookies enabled
    #     request.session.set_test_cookie()
    #     return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(self.__class__, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()

        if user is not None:
            msg = 'User: %s' % user

            if user.is_active:
                if user.last_login == None:
                    self.newUser = True
                    msg = '%s : first time login - redirecting to change password - ' % msg
                login(self.request, user)
                msg = '%s has logged in' % msg
                logger.info(msg)

            else:
                # Return a 'disabled account' error message
                form.add_error = 'Your account has been disabled. Please contact registration.'
                msg = '%s has disabled account' % msg
                logger.warning(msg)

        else:
            # Return an 'invalid login' error message.
            form.add_error = 'Login credentials are invalid. Please try again'
            msg = 'Login failed with invalid credentials'
            logger.error(msg)

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        self.check_and_delete_test_cookie()
        return super(self.__class__, self).form_valid(form)

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(self.__class__, self).form_invalid(form)

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get_success_url(self):
        if self.newUser:
            redirect_to = "/profile"
        elif self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name, ''))

        netloc = urlparse.urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    successurl = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(self.successurl)


def locked_out(request):
    if request.POST:
        form = AxesCaptchaForm(request.POST)
        if form.is_valid():
            ip = get_ip(request)
            if ip is not None:
                msg = "User locked out with IP address=%s" % ip
                logger.warning(msg)
                reset(ip=ip)

            return HttpResponseRedirect(reverse_lazy('index'))
    else:
        form = AxesCaptchaForm()

    return render(request, 'auth/locked.html', context=dict(form=form))


def csrf_failure(request, reason=""):
    ctx = {'title': 'CSRF Failure',
           'message': 'Your browser does not accept cookies and this can be a problem in ensuring a secure connection.'}
    template_name = 'registration/csrf_failure.html'
    return render(request, template_name, ctx)


class ProfileView(FormView):
    template_name = 'auth/profile.html'
    success_url = reverse_lazy('index')
    form_class = UserUpdateForm

    def get_initial(self):
        initial = super(ProfileView, self).get_initial()
        if self.request.user.is_authenticated:
            initial.update({'user': self.request.user})
        return initial

    def get_form_kwargs(self):
        kwargs = super(ProfileView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({'instance': self.request.user})
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)
