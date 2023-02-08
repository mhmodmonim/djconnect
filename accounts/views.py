from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm


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

def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return render(request,'accounts/register_done.html',{'new_user': new_user})

    return  render(request, 'accounts/register.html',{'user_form': user_form})



@login_required
def index(request):
    return render(request, 'accounts/dashboard.html',
                            {'section': 'dashboard'})

