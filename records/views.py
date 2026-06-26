from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import MaintenanceForm


def index(request):
    # Ana sayfa: Arama kutusundan gelen 'plaka' sorgusunu yakalar
    plaka = request.GET.get('plaka')
    vehicle = None
    if plaka:
        vehicle = Vehicle.objects.filter(plaka=plaka).first()
        # Eğer araç bulunursa doğrudan detay sayfasına yönlendirebiliriz
        if vehicle:
            return redirect('vehicle_detail', vehicle_id=vehicle.id)

    return render(request, 'index.html', {'vehicle': vehicle, 'plaka': plaka})


def vehicle_detail(request, vehicle_id):
    # Bu fonksiyon hem linkten gelen ID ile hem de yönlendirmeyle çalışır
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