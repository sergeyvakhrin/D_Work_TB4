from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import SMSAuthenticationView, UserRetrieveAPIView, UserUpdateAPIView, UserDeleteAPIView, \
    UserListAPIView

app_name = UsersConfig.name


urlpatterns = [
    path('auth/sms/', SMSAuthenticationView.as_view(permission_classes=(AllowAny, )), name='sms-auth'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny, )), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny, )), name='token_refresh'),

    path('users/', UserListAPIView.as_view(), name="user-list"),
    path('<int:pk>/', UserRetrieveAPIView.as_view(permission_classes=(AllowAny, )), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(permission_classes=(AllowAny, )), name='user-update'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(permission_classes=(AllowAny, )), name='user-delete'),
]