from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('arac/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
    path('bakim-ekle/', views.add_maintenance, name='add_maintenance'),
]