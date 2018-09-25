import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'astraios.settings'
django.setup()
from asteroid_field.models import Asteroid
from math import *
import random

x_lim = 8000 #m
y_lim = 8000 #m
max_asteroid_rad = 120 #m
min_asteroid_rad = 7 #m

def ast_plist(min_rad, max_rad, spokes, delta_ang):
	spoke_ang_list = []
	start_spoke = random.randrange(8)
	for count in range(8):
		spoke_ang_list.append(2*((start_spoke+count)%8)*pi/spokes+random.uniform(-delta_ang,delta_ang))
	ast_plist = []
	rad = max_rad * random.uniform(0.7,1)
	for spoke in spoke_ang_list:
		rad_iteration = 0
		delta_rad = rad/3
		rad_change = random.uniform(-delta_rad,delta_rad)
		while rad + rad_change > max_rad or rad + rad_change < min_rad:
			rad_change += random.uniform(-delta_rad,delta_rad)
			rad_change *= 0.99
			rad_iteration += 1
		rad += rad_change
		ast_plist.append({"x":round(rad*cos(spoke),9),"y":round(rad*sin(spoke),9)})
	return ast_plist

def log_rad(min_rad,max_rad):
	rad = (max_rad-min_rad)**random.random() + min_rad
	return(rad)

def overlap(x,y,bound,max_rad, asteroid_list = []):
	for asteroid in asteroid_list:
		if sqrt((asteroid.x - x)**2+(asteroid.y - y)**2) < bound + asteroid.bound:
			return True
	vincinity = Asteroid.objects.filter(x__gte = x - (bound+max_rad), x__lte = x + (bound+max_rad), y__gte = y - (bound+max_rad), y__lte = y + (bound+max_rad))
	for asteroid in vincinity:
		if sqrt((asteroid.x - x)**2+(asteroid.y - y)**2) < bound + asteroid.bound:
			return True
	return False

def spawn_asteroids(num,min_rad,max_rad, spokes = 8, delta_ang = pi/8):
	count = 0
	asteroid_list = []
	while count < num:
		iteration = 0
		x = random.uniform(0,x_lim)
		y = random.uniform(0,y_lim)
		bound = log_rad(min_rad,max_rad)
		reduced_max_rad = max_rad
		while overlap(x,y,bound,max_rad,asteroid_list):
			if reduced_max_rad > min_rad:
				reduced_max_rad *= 0.99
			x = random.uniform(0,x_lim)
			y = random.uniform(0,y_lim)
			bound =log_rad(min_rad,reduced_max_rad)
			iteration += 1
			progress = int((count / num)*20)
			print("Iteration",iteration,"\t Creation",count,"\tProgress ["+"#"*progress+" "*(20-progress)+"]",end="\r")
		asteroid_list.append(Asteroid(name=str(round(x))+","+str(round(y)), bound = bound, x = x, y = y, plist = ast_plist(0,bound, spokes , delta_ang)))
		count += 1
		if len(asteroid_list) >= 50:
			Asteroid.objects.bulk_create(asteroid_list)
			asteroid_list = []
	print()
	print("Done, inserted",count,"entries.")
	return True

while True:
	number = int(input("Spawn how many asteroids? "))
	if number == 0:
		break
	spawn_asteroids(number,min_asteroid_rad,max_asteroid_rad)
