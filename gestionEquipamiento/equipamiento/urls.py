from django.urls import path, include
from equipamiento import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'equipos', views.Equipamiento)
router.register(r'distribuidores', views.Distribuidores)
router.register(r'constancias-service', views.ConstanciaService)


urlpatterns = [
	path('no-op/', views.EquiposNoOperativos.as_view({'get': 'list'})),
	path('mantenimiento/', views.MantenimientoAnual.as_view({'get': 'list'})),
	path('', include(router.urls))
]


