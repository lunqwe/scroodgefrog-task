from django.urls import path
from .views import CreateUserView, LoginView

urlpatterns = [
    path('sign-up/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
]
