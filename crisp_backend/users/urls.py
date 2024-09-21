from django.urls import path
from .views import CitizenRegisterView, WorkersRegisterView, ProtectedView, HealthView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', CitizenRegisterView.as_view(), name='citizen-register'),
    path('create/', WorkersRegisterView.as_view(), name='worker-register'), 
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/protected', ProtectedView.as_view(), name='protected_View'),
    path('health/', HealthView.as_view(), name='health-check')
]
