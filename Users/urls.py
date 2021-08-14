from django.contrib.auth import views as auth_views
from django.urls import path, include

from Users import views

urlpatterns = [
    path('Register/', views.Register_Login, name='register'),
    path('Login/', views.Login, name='login'),
    path('Logout/', views.Logout, name='logout'),
    path('SignUp/', views.SignUp, name='sign_up'),
    path('ConfirmEmail/<str:UserCode>/', views.Confirm_email, name='ConfirmEmail'),
    path('Accounts/', include('allauth.urls')),
    # django views
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
