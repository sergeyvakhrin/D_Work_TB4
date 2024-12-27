from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, logout_view, UserProfileView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('auth/sms/', RegisterView.as_view(), name='sms_auth'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),

]