from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File


class Vehicle(models.Model):
    plate = models.CharField(max_length=20, verbose_name="Plaka")
    motor_no = models.CharField(max_length=50, verbose_name="Motor No")
    chassis_no = models.CharField(max_length=50, verbose_name="Şasi No")
    brand_model = models.CharField(max_length=100, verbose_name="Marka ve Model")
    vehicle_type = models.CharField(max_length=50, verbose_name="Tipi")
    # YENİ EKLENEN ALAN: QR Kod Resmi
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name="QR Kod")

    def __str__(self):
        return f"{self.plate} - {self.brand_model}"

    # OTOMATİK QR KOD ÜRETME MOTORU
    def save(self, *args, **kwargs):
        # Önce aracı veritabanına kaydedip bir ID alıyoruz
        super().save(*args, **kwargs)

        # Eğer aracın henüz bir QR kodu yoksa şimdi oluştur
        if not self.qr_code:
            # QR kodu okutunca gidilecek adres
            qr_url = f"http://127.0.0.1:8000/arac/{self.id}/"

            qr_image = qrcode.make(qr_url)
            canvas = BytesIO()
            qr_image.save(canvas, format='PNG')
            canvas.seek(0)

            # Resmi isimlendirip kaydet
            file_name = f'arac_{self.id}_qr.png'
            self.qr_code.save(file_name, File(canvas), save=False)
            super().save(*args, **kwargs)


class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Araç")
    date = models.DateField(verbose_name="Bakım Tarihi")
    km = models.IntegerField(verbose_name="Bakım Kilometresi")
    next_km = models.IntegerField(verbose_name="Gelecek Bakım Kilometresi")
    description = models.TextField(verbose_name="Yapılan İşlemler / Açıklama")

    def __str__(self):
        return f"{self.vehicle.plate} - {self.date}"