from django.db import models


# Create your models here.

TIPO_CHOICES = ['ventilacion', 'ecografia', 'cirugia', 'monitoreo', 'diagnostico por imagenes']
SECTOR_CHOICES = ['guardia', 'UTI', 'UCO', 'quirofano', 'rayos', 'taller']

TIPO_CHOICES = [(item, item) for item in TIPO_CHOICES]
SECTOR_CHOICES = [(item, item) for item in SECTOR_CHOICES]


class Distribuidor(models.Model):
	razon_social = models.CharField(max_length=50)
	tfno = models.IntegerField()
	direccion = models.CharField(max_length=50)
	email = models.EmailField()

	class Meta:
		ordering = ['razon_social']

	def __str__(self):
		return self.razon_social


class Equipo(models.Model):
	fecha_instalacion = models.DateTimeField(auto_now_add=True)
	marca = models.CharField(max_length=50)
	modelo = models.CharField(max_length=50)
	numero_serie = models.IntegerField(primary_key=True)
	tipo = models.CharField(choices=TIPO_CHOICES, max_length=50)
	sector = models.CharField(choices=SECTOR_CHOICES, default='taller', max_length=50)
	fecha_mantenimiento_anual = models.DateField()
	operativo = models.BooleanField(default=True)

	distribuidor = models.ForeignKey(Distribuidor, on_delete=models.CASCADE)

	class Meta:
		ordering = ['sector']

	def __str__(self):
		return f"{self.marca} {self.modelo}, SN: {self.numero_serie}"


class ConstanciaService(models.Model):
	fecha = models.DateField(auto_now_add=True)
	responsable = models.CharField(max_length=50)
	falla = models.CharField(max_length=50)
	observaciones = models.TextField()
	cerrada = models.BooleanField(default=False)

	equipo =  models.ForeignKey(Equipo, on_delete=models.CASCADE)


