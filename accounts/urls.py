from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # custom sign in url
    path('signin/', views.user_login, name='signin'),
    # django auth authentication urls
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password urls
    path("password_change/", auth_views.PasswordChangeView.as_view(), name='password_change'),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # All Auth urls could be replaced with the built-in django auth urls as below:
    # path('', include('django.contrib.auth.urls')),

    path('register/', views.register, name='register'),
    path('', views.index, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]
