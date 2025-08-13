from django.urls import path
from .views import RegisterView, LoginView, DeleteUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
]
