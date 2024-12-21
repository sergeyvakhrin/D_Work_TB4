from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import SMSAuthenticationView

app_name = UsersConfig.name


urlpatterns = [
    path('auth/sms/', SMSAuthenticationView.as_view(permission_classes=(AllowAny, )), name='sms-auth'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny, )), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny, )), name='token_refresh'),
    
]