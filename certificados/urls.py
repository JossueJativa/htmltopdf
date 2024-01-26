from django.urls import path
from . import views

app_name = "certificados"

urlpatterns = [
    path('certificado/<str:username>/<str:course>/<str:date>/<str:email>/', views.certificado, name='certificado'),
]