from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from main.forms.login_register import LoginRegisterForm


def index(request):
    print(request.user)
    ctx = {'user': request.user}
    return render(request, 'index.html', ctx)


def login_register(request):
    form = LoginRegisterForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status_code=400)
    email = form.cleaned_data['email']
    password = form.cleaned_data['password']
    # If user login successfully, login the request
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    # If, email exists, return incorrect credentials
    if User.objects.filter(email=email).exists():
        return HttpResponse(status_code=400)
    user = User.objects.create_user(email, email, password)
    login(request, user)
    return HttpResponseRedirect('/')
