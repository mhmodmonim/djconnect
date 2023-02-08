from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated Successfully')
            else:
                return HttpResponse("Disabled Account")
        else:
            return HttpResponse("Invalid Login Credentials!")
    return render(request, 'accounts/login.html', {'form': form })

