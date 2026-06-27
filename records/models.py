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
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name="QR Kod")

    def __str__(self):
        return f"{self.plate} - {self.brand_model}"

    def save(self, *args, **kwargs):
        # 1. Önce aracı kaydet ki bir ID oluşsun
        super().save(*args, **kwargs)

        # 2. Eğer QR kod yoksa oluştur
        if not self.qr_code:
            # İŞTE TAM OLARAK DÜZELTİLEN SATIR BURASI
            qr_url = f"https://otodijitaldefter.pythonanywhere.com/arac/{self.id}/"

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(qr_url)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")

            canvas = BytesIO()
            qr_image.save(canvas, format='PNG')

            file_name = f'arac_{self.id}_qr.png'
            # Save metodunu tekrar çağırmadan dosyayı kaydet
            self.qr_code.save(file_name, File(canvas), save=False)

            # Sadece bir kere güncelleme yap
            super().save(update_fields=['qr_code'])

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Araç")
    date = models.DateField(verbose_name="Bakım Tarihi")
    km = models.IntegerField(verbose_name="Bakım Kilometresi")
    next_km = models.IntegerField(verbose_name="Gelecek Bakım Kilometresi")
    description = models.TextField(verbose_name="Yapılan İşlemler / Açıklama")

    def __str__(self):
        return f"{self.vehicle.plate} - {self.date}"