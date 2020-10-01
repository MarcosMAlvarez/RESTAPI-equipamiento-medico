from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from equipamiento.models import Equipo, Distribuidor, ConstanciaService
from equipamiento.serializers import EquipoSerializer, DistribuidorSerializer, ConstanciaSerializer


class Equipamiento(viewsets.ModelViewSet):
	queryset = Equipo.objects.all()
	serializer_class = EquipoSerializer

	permission_classes = [IsAuthenticated]


class EquiposNoOperativos(viewsets.ModelViewSet):
	'''
	Lista de todos los equipos que no estan operativos
	'''
	queryset = Equipo.objects.filter(operativo=False)
	serializer_class = EquipoSerializer
	permission_classes = [IsAuthenticated]

	http_method_names = ['get']


class MantenimientoAnual(viewsets.ModelViewSet):
	'''
	Lista de equipos a los que hay que realizar
	mantenimiento anual.
	'''
	from datetime import date

	today = date.today()
	a_year_ago = date(today.year - 1, today.month, today.day)

	queryset = Equipo.objects.filter(fecha_mantenimiento_anual__lte=a_year_ago)
	serializer_class = EquipoSerializer
	permission_classes = [IsAuthenticated]

	http_method_names = ['get']


class Distribuidores(viewsets.ModelViewSet):
	queryset = Distribuidor.objects.all()
	serializer_class = DistribuidorSerializer


class ConstanciaService(viewsets.ModelViewSet):
	queryset = ConstanciaService.objects.all()
	serializer_class = ConstanciaSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['equipo']

