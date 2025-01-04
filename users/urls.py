from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from .views import PasswordChange

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),
    path("profile/update/", views.update_profile, name="update_profile"),
    path('change-password/',PasswordChange.as_view(template_name='registration/change_password.html'), name="change_password"),
    path('password-success/', views.password_success,name="password_success"),
    path('author/<int:author_id>/followers/', views.author_followers_view, name='author_followers'),
    path('author/<int:author_id>/following/', views.author_following_view, name='author_following'),
]
