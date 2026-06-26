from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import MaintenanceForm  # Formumuzu içeri aldık


# (Önceki vehicle_detail fonksiyonun burada aynen kalsın, ona dokunma)
def vehicle_detail(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    maintenances = vehicle.maintenances.all().order_by('-date')
    context = {
        'vehicle': vehicle,
        'maintenances': list(maintenances),
    }
    return render(request, 'records/vehicle_detail.html', context)


# YENİ EKLENEN KISIM
def add_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_maintenance')  # Kaydedince formu sıfırlayıp aynı sayfada kalsın
    else:
        form = MaintenanceForm()

    return render(request, 'records/add_maintenance.html', {'form': form})