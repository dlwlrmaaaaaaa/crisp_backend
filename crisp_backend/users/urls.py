from django.urls import path
from .views import CitizenRegisterView, LoginView, WorkersRegisterView


urlpatterns = [
    path('register', CitizenRegisterView.as_view(), name='citizen-register'),
    path('login', LoginView.as_view(), name="login"),
    path('create', WorkersRegisterView.as_view(), name='worker-register'),
    
    path('portal', LoginView.as_view(), name='worker-portal'),


]
