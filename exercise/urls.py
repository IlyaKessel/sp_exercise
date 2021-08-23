from django.urls import path
from engine import views

urlpatterns = [
    path('api/v1/domain-request', views.DomainAPIView.as_view(), name='domain-request'),
]
