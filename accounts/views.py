from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from actions.models import Action
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User
from .models import Profile, Contact
from django.contrib import messages
from actions.utils import create_action


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
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    user_form = UserRegistrationForm(request.POST or None)
    if user_form.is_valid():
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        Profile.objects.create(user=new_user)
        create_action(new_user, 'has created an account')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})

    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    user_form = UserEditForm(
        instance=request.user,
        data=request.POST or None)

    profile_form = ProfileEditForm(
        instance=request.user.profile,
        data=request.POST or None,
        files=request.FILES or None
    )

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        messages.success(request, "Profile Updated Successfully")
    else:
        if request.method == 'POST':
            messages.error(request, "Error updating your profile!")

    return render(request, 'accounts/edit.html', {'user_form': user_form,
                                                  'profile_form': profile_form})


@login_required
def index(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)\
                      .select_related('user', 'user__profile')\
            .prefetch_related('target')[:10]
    return render(request, 'accounts/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions
                   })


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'users/list.html', {
        'users': users,
        'section': 'People'
    })


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'users/detail.html', {
        'user': user,
        'section': 'People'
    })


def user_follow(request):
    user_id = request.POST['id']
    action = request.POST['action']
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'starts following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})

    return JsonResponse({'status': 'error'})


