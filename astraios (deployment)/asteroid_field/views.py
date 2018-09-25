from django.http import HttpResponse
from django.shortcuts import render
from . import models
from . import radar
from . import physics_engine
from math import sqrt, cos, sin, fabs, pi
import json

s = 10

def index(request):
    context = {
        'ship_list': models.Ship.objects.all(),
    }
    return render(request, "index.html", context)

def fire_engine(request):
	shipname = request.GET.get("shipname")
	de = float(request.GET.get("de"))
	ship = models.Ship.objects.get(name = shipname)
	orientation = ship.orientation
	ship.ix += de*cos(orientation/180*pi)
	ship.iy += de*sin(orientation/180*pi)
	ship.fuel -= fabs(de/ship.isp)
	ship.save()
	radar.screen.set_view(ship.x,ship.y,s)
	context = {
		'ship_name': ship.name,
		'health' : ship.health,
		'max_health' : ship.max_health,
		'fuel' : ship.fuel,
		'max_fuel' : ship.max_fuel,
		'isp' : ship.isp,
		'rcs' : ship.rcs,
		'de':0,
		'dt':0,
		'main_x' : round(ship.x,2),
		'vx': round(ship.vx,2),
		'main_y' : round(ship.y,2),
		'vy': round(ship.vy,2),
		'impulse': str(round(ship.ix))+", "+ str(round(ship.iy)),
		'screen_x' : radar.screen.x,
		'screen_y' : radar.screen.y,
		'ship_list' : str(radar.neighbor_ship(ship.x,ship.y,s)).replace("'",'"'),
		'ast_list' : str(radar.neighbor_ast(ship.x,ship.y,s)).replace("'",'"'),
		'scale' : s,
	}
	return render(request, "asteroid_field/index.html", context)

def fire_thruster(request):
	shipname = request.GET.get("shipname")
	dt = float(request.GET.get("dt"))
	ship = models.Ship.objects.get(name = shipname)
	ship.orientation = (ship.orientation + dt)%360
	ship.fuel -= fabs(dt/ship.rcs)
	ship.save()
	radar.screen.set_view(ship.x,ship.y,s)
	context = {
		'ship_name': ship.name,
		'health' : ship.health,
		'max_health' : ship.max_health,
		'fuel' : ship.fuel,
		'max_fuel' : ship.max_fuel,
		'isp' : ship.isp,
		'rcs' : ship.rcs,
		'de':0,
		'dt':0,
		'main_x' : round(ship.x,2),
		'vx': round(ship.vx,2),
		'main_y' : round(ship.y,2),
		'vy': round(ship.vy,2),
		'impulse': str(round(ship.ix,3))+", "+ str(round(ship.iy,3)),
		'screen_x' : radar.screen.x,
		'screen_y' : radar.screen.y,
		'ship_list' : str(radar.neighbor_ship(ship.x,ship.y,s)).replace("'",'"'),
		'ast_list' : str(radar.neighbor_ast(ship.x,ship.y,s)).replace("'",'"'),
		'scale' : s,
	}
	return render(request, "asteroid_field/index.html", context)

def physics_step(request):
	try:
		time = float(request.GET.get("time"))
	except:
		time = 0
	info = request.GET.get("info")
	try:
		info = info.replace("'",'"')
		info = json.loads(info)
	except:
		info = {'ship':'','de':0,'dt':0}
	physics_engine.step(float(time))
	try:
		ship = models.Ship.objects.get(name = info['ship'])
	except:
		ship = models.Ship.objects.filter(pk=1).first()
	radar.screen.set_view(ship.x,ship.y,s)
	context = {
		'ship_name': ship.name,
		'health' : ship.health,
		'max_health' : ship.max_health,
		'fuel' : ship.fuel,
		'max_fuel' : ship.max_fuel,
		'isp' : ship.isp,
		'rcs' : ship.rcs,
		'de':info['de'],
		'dt':info['dt'],
		'main_x' : round(ship.x,2),
		'vx': round(ship.vx,2),
		'main_y' : round(ship.y,2),
		'vy': round(ship.vy,2),
		'impulse': str(round(ship.ix,3))+", "+ str(round(ship.iy,3)),
		'screen_x' : radar.screen.x,
		'screen_y' : radar.screen.y,
		'ship_list' : str(radar.neighbor_ship(ship.x,ship.y,s)).replace("'",'"'),
		'ast_list' : str(radar.neighbor_ast(ship.x,ship.y,s)).replace("'",'"'),
		'scale' : s,
	}
	return render(request, "asteroid_field/index.html", context) 

def ship_view(request):
	shipname = request.GET.get("shipname")
	try:
		info = info.replace("'",'"')
		info = json.loads(info)
	except:
		info = {'ship':'','de':0,'dt':0}
	ship = models.Ship.objects.get(name = shipname)
	radar.screen.set_view(ship.x,ship.y,s)
	context = {
		'ship_name': ship.name,
		'health' : ship.health,
		'max_health' : ship.max_health,
		'fuel' : ship.fuel,
		'max_fuel' : ship.max_fuel,
		'isp' : ship.isp,
		'rcs' : ship.rcs,
		'de':info['de'],
		'dt':info['dt'],
		'main_x' : round(ship.x,2),
		'vx': round(ship.vx,2),
		'main_y' : round(ship.y,2),
		'vy': round(ship.vy,2),
		'impulse': str(round(ship.ix,3))+", "+ str(round(ship.iy,3)),
		'screen_x' : radar.screen.x,
		'screen_y' : radar.screen.y,
		'ship_list' : str(radar.neighbor_ship(ship.x,ship.y,s)).replace("'",'"'),
		'ast_list' : str(radar.neighbor_ast(ship.x,ship.y,s)).replace("'",'"'),
		'scale' : s,
	}
	return render(request, "asteroid_field/index.html", context)

def teleport(request):
	try:
		x = float(request.GET.get("x"))
		y = float(request.GET.get("y"))
		s = float(request.GET.get("s"))
	except:
		return index(request)
	radar.screen.set_view(x,y,s)
	context = {
		'main_x' : round(x,3),
		'main_y' : round(y,3),
		'screen_x' : radar.screen.x,
		'screen_y' : radar.screen.y,
		'ship_list' : str(radar.neighbor_ship(x,y,s)).replace("'",'"'),
		'ast_list' : str(radar.neighbor_ast(x,y,s)).replace("'",'"'),
		'scale' : s,
	}
	return render(request, "asteroid_field/index.html", context)
