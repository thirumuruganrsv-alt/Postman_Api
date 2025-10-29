from django.urls import path
from .views import RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ChangePasswordView
from .views import ForgotPasswordView
from .views import ResetPasswordView
from .views import ProfileDetailAPIView
from .models import Profile
from .views import ProfileListCreateAPIView
from .views import ProfileDetailView
from users import views
from .views import ProfileCreateAPIView




urlpatterns = [

    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

#change password and reset password

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('api/profile/<int:pk>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/<int:id>/', ProfileDetailView.as_view(), name='api_profile_update'),
    path('profile/', ProfileListCreateAPIView.as_view(), name='profile-list-create'),
    path('api/profile/<int:pk>/', ProfileListCreateAPIView.as_view()),
    path('profile/create/', ProfileCreateAPIView.as_view(), name='profile-create')


]

