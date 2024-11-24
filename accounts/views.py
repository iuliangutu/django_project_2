from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from accounts.forms import SignUpForm
from accounts.models import Profile


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


