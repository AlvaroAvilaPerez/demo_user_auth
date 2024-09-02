from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin


class ProtectedView(LoginRequiredMixin, View):

    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def get(self, req, *args, **kwargs):
        user = req.user

        if isinstance(user, AnonymousUser):
            return HttpResponse("You cannot access this resource")
        else:
            return HttpResponse("You have access to this resource")


class LoginView(View):
    form_class = LoginForm

    def post(self, req, *args, **kwargs):
        form = self.form_class(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                redirect_to = req.GET.get('redirect_to')

                if redirect_to is None:
                    return HttpResponse('You successfully logged in')
                else:
                    return HttpResponseRedirect(redirect_to)

            else:
                return HttpResponse('You cannot login with these credentials!')
        else:
            return HttpResponse("The Form is not valid!")

    def get(self, req, *args, **kwargs):
        form = self.form_class()
        return render(
            req,
            "blog/login.html",
            {"form": form},
        )


class LogoutView(View):

    def get(self, req, *args, **kwargs):
        user = req.user

        if isinstance(user, AnonymousUser):
            return HttpResponse("You have not even logged in yet so you cannot logout")
        else:
            logout(req)
            return HttpResponse("Successfully Logged out")


