from django.urls import path
from .views import GenerateZIP



urlpatterns = [
    path('', GenerateZIP.as_view(), name='generate_zip')
]