from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import MaintenanceForm

def index(request):
    plaka = request.GET.get('plaka')
    error = None

    if plaka:
        vehicle = Vehicle.objects.filter(plate=plaka).first()
        if vehicle:
            return redirect('vehicle_detail', vehicle_id=vehicle.id)
        else:
            error = "Bu plakaya ait kayıt bulunamadı!"

    return render(request, 'index.html', {'error': error, 'plaka': plaka})

def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    maintenances = vehicle.maintenances.all().order_by('-date')
    context = {
        'vehicle': vehicle,
        'maintenances': maintenances,
    }
    return render(request, 'records/vehicle_detail.html', context)

def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_maintenance')
    else:
        form = MaintenanceForm()
    return render(request, 'records/add_maintenance.html', {'form': form})