from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
 CustomTokenObtainPairView, RegisterView, ProfileView,
 ChangePasswordView, UserListView
)

app_name = 'accounts'

urlpatterns = [
 path('register/', RegisterView.as_view(), name='register'),
 path('login/', CustomTokenObtainPairView.as_view(), name='login'),
 path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 path('profile/', ProfileView.as_view(), name='profile'),
 path('change-password/', ChangePasswordView.as_view(), name='change_password'),
 path('users/', UserListView.as_view(), name='user_list'),
]