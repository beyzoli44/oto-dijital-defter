from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ana sayfa
    path('arac/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'), # Detay sayfası
    path('bakim-ekle/', views.add_maintenance, name='add_maintenance'), # Bakım ekleme
]