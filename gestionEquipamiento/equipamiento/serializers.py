from rest_framework import serializers
from equipamiento.models import Equipo, Distribuidor, ConstanciaService

class EquipoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Equipo
		fields = ['url', 'marca', 'modelo', 'numero_serie', 'tipo', 'sector', 'operativo', 'fecha_mantenimiento_anual', 'distribuidor']


class DistribuidorSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Distribuidor
		fields = ['url', 'razon_social', 'tfno', 'direccion', 'email']


class ConstanciaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = ConstanciaService
		fields = ['id', 'equipo', 'fecha', 'cerrada', 'responsable', 'falla', 'observaciones', 'url']
