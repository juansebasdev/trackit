from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate, LoginView
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('profile/email/', EmailUpdate.as_view(), name='profile_email'),
    path('login/', LoginView, name='login'),
]