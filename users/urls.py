from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('forgotpass', views.forgotpass, name='forgotpass'),
    path('provider_regi', views.provider_regi, name='provider_regi'),
    path('seekerprofile', views.seekerprofile, name='seekerprofile'),
    path('information', views.information, name='information'),
    path('profile', views.profile, name='profile'),
    path('account', views.account, name='account'),
    path('companyupdate', views.companyupdate, name='companyupdate'),

    path('passwordupdate', views.passwordupdate, name='passwordupdate'),
    path('providerupdate', views.providerupdate, name='providerupdate'),

    path('password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

]
