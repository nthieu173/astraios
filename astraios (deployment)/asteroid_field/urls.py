from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^step/', views.physics_step, name='physics_step'),
	url(r'^engine/', views.fire_engine, name='fire_engine'),
	url(r'^thruster/', views.fire_thruster, name='fire_thruster'),
	url(r'^ship/', views.ship_view, name ='ship_view'),
	url(r'^teleport/', views.teleport, name='teleport'),
]
