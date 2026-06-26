from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('arac/', views.vehicle_detail, name='vehicle_detail'), # ID olmadan da buraya gelsin
    path('arac/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail_id'), # ID ile de çalışsın
    path('bakim-ekle/', views.add_maintenance, name='add_maintenance'),
]