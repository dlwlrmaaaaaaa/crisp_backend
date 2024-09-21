from django.urls import path
from .views import ReportView

urlpatterns = [
    path('<uuid:pk>/', ReportView.as_view(), name='report_list'),
    path('', ReportView.as_view(), name='create_report')
]
