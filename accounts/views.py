from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import SignUpForm, AdminRequestMessageForm
from accounts.models import Profile, AdminRequestMessage


class SubmittableLoginView(LoginView):
    template_name = 'login.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = '/'


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = '/'



def profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)

        return render(request, 'profile.html',
                      context={'profile': profile}
                      )
    else:
        return redirect('/accounts/login/')


class PermissionRequestView(LoginRequiredMixin, CreateView):
    model = AdminRequestMessage
    form_class = AdminRequestMessageForm
    template_name = 'permission_request_form.html'
    success_url = reverse_lazy('accounts:permission-request-form')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

