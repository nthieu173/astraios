import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'astraios.settings'
django.setup()
from physics import *
from asteroid_field.models import *
import math
from operator import itemgetter

max_rad = 120
max_bound = 2

def step(time):
	update_all_ship_velocity()
	step_time = time
	count = 0
	while True:
		collision = get_earliest(ship_collision(time),proj_collision(time))
		update_ships = Ship.objects.all()
		if collision == False:
			for ship in update_ships:
				ship.x += ship.vx*time
				ship.y += ship.vy*time
				ship.save()
			for projectile in Projectile.objects.all():
				projectile.x += projectile.vx*time
				projectile.y += projectile.vy*time
				projectile.save()
			break
		if collision['type'] == 'ss':
			ship = Ship.objects.get(pk = collision['pks'][0])
			other_ship = Ship.objects.get(pk = collision['pks'][1])
			resolution = collision_resolution(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(other_ship.bound,other_ship.x,other_ship.y,other_ship.vx,other_ship.vy),collision['t'])
			ship.x = resolution['obj1']['x']
			ship.y = resolution['obj1']['y']
			ship.vx = resolution['obj1']['vx']
			ship.vy = resolution['obj1']['vy']
			other_ship.x = resolution['obj2']['x']
			other_ship.y = resolution['obj2']['y']
			other_ship.vx = resolution['obj2']['vx']
			other_ship.vy = resolution['obj2']['vy']
			ship.save()
			other_ship.save()
			update_ships.exclude(pk=collision['pks'][0]).exclude(pk=collision['pks'][1])
		elif collision['type'] == 'sa':
			ship = Ship.objects.get(pk = collision['pks'][0])
			ast = Asteroid.objects.get(pk = collision['pks'][1])
			resolution = collision_resolution(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(ast.bound,ast.x,ast.y,0,0),collision['t'],2)
			ship.x = resolution['x']
			ship.y = resolution['y']
			ship.vx = resolution['vx']
			ship.vy = resolution['vy']
			ship.save()
			update_ships.exclude(pk=collision['pks'][0])
		elif collision['type'] == 'pa':
			projectile = Projectile.objects.get(pk=collision['pks'][0])
			projectile.delete()
		elif collision['type'] == 'ps':
			projectile = Projectile.objects.get(pk=collision['pks'][0])
			ship = Ship.objects.get(pk = collision['pks'][1])
			resolution = collision_resolution(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(projectile.bound,projectile.x,projectile.y,projectile.vx,projectile.vy),collision['t'],-2)
			ship.x = resolution['x']
			ship.y = resolution['y']
			ship.vx = resolution['vx']
			ship.vy = resolution['vy']
			ship.health -= projectile.dmg
			ship.save()
			projectile.delete()
			update_ships.exclude(pk=collision['pks'][1])
		for ship in update_ships:
			ship.x += ship.vx*collision['t']
			ship.y += ship.vy*collision['t']
			ship.save()
		for projectile in Projectile.objects.all():
			projectile.x += projectile.vx*collision['t']
			projectile.y += projectile.vy*collision['t']
			projectile.save()
		time -= collision['t']
		count += 1
		print("Stepped",count,"times.",end="\r")
	print("Physic stepped successfully.")
	return True

def update_all_ship_position():
	for ship in Ship.objects.all():
		ship.vx += ship.ix
		ship.vy += ship.iy
		ship.ix = 0
		ship.iy = 0
		ship.save()

def to_obj(b,x,y,vx,vy):
	converted = {}
	converted['bound'] = b
	converted['x'] = x
	converted['y'] = y
	converted['vx'] = vx
	converted['vy'] = vy
	return converted

def update_all_ship_velocity():
	for ship in Ship.objects.all():
		ship.vx += ship.ix
		ship.vy += ship.iy
		ship.ix = 0
		ship.iy = 0
		ship.save()

def get_earliest(queue1,queue2):
	if len(queue1) == 0 and len(queue2) == 0:
		return False
	elif len(queue1) == 0:
		return queue2[0]
	elif len(queue2) == 0:
		return queue1[0]
	elif queue1[0]['t'] <= queue2[0]['t']:
		return queue1[0]
	else:
		return queue2[0]

def proj_collision(time):
	collision_queue = []
	ships = Ship.objects.all()
	asteroids = Asteroid.objects.all()
	for projectile in Projectile.objects.all():
		check_x = projectile.vx*time
		if check_x > 0:
			asteroids.filter(x__gte = projectile.x- projectile.bound-max_rad,x__lte = projectile.x + check_x + projectile.bound+max_rad)
			ships.filter(x__gte = projectile.x- projectile.bound-max_bound,x__lte = projectile.x + check_x + projectile.bound+max_bound)
		else:
			asteroids.filter(x__lte = projectile.x+ projectile.bound+max_rad,x__gte = projectile.x - check_x - projectile.bound-max_rad)
			ships.filter(x__lte = projectile.x+ projectile.bound+max_bound,x__gte = projectile.x - check_x - projectile.bound-max_bound)
		check_y = projectile.vy*time
		if check_y > 0:
			asteroids.filter(y__gte = projectile.y- projectile.bound-max_rad,y__lte = projectile.y + check_y + projectile.bound+max_rad)
			ships.filter(y__gte = projectile.y- projectile.bound-max_bound,y__lte = projectile.y + check_y + projectile.bound+max_bound)
		else:
			asteroids.filter(y__lte = projectile.y+ projectile.bound+max_rad,y__gte = projectile.y - check_y - projectile.bound-max_rad)
			ships.filter(x__lte = projectile.y+ projectile.bound+max_bound,x__gte = projectile.y - check_y - projectile.bound-max_bound)
		for ship in ships:
			result = bb_collide(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(projectile.bound,projectile.x,projectile.y,projectile.vx,projectile.vy),time)
			if result == True:
				projectile.delete()
				ship.health -= projectile.dmg
				ship.save()
			elif not result == False:
				collision_queue.append({'t':result,'type':'ps','pks':(projectile.pk,ship.pk)})
		for asteroid in asteroids:
			result = bb_collide(to_obj(projectile.bound,projectile.x,projectile.y,projectile.vx,projectile.vy),to_obj(asteroid.bound,asteroid.x,asteroid.y,0,0),time)
			if result == True:
				projectile.delete()
			elif not result == False:
				collision_queue.append({'t':result,'type':'pa','pks':(projectile.pk,asteroid.pk)})
	collision_queue = sorted(collision_queue, key=itemgetter('t'))
	return collision_queue

def ship_collision(time):
	collision_queue = []
	for ship in Ship.objects.all():
		ships = Ship.objects.all().exclude(pk=ship.pk)
		asteroids = Asteroid.objects.all()
		check_x = ship.vx*time
		if check_x > 0:
			asteroids.filter(x__gte = ship.x- ship.bound-max_rad,x__lte = ship.x + check_x + ship.bound+max_rad)
			ships.filter(x__gte = ship.x- ship.bound-max_bound,x__lte = ship.x + check_x + ship.bound+max_bound)
		else:
			asteroids.filter(x__lte = ship.x+ ship.bound+max_rad,x__gte = ship.x - check_x - ship.bound-max_rad)
			ships.filter(x__lte = ship.x+ ship.bound+max_bound,x__gte = ship.x - check_x - ship.bound-max_bound)
		check_y = ship.vy*time
		if check_y > 0:
			asteroids.filter(y__gte = ship.y- ship.bound-max_rad,y__lte = ship.y + check_y + ship.bound+max_rad)
			ships.filter(y__gte = ship.y- ship.bound-max_bound,y__lte = ship.y + check_y + ship.bound+max_bound)
		else:
			asteroids.filter(y__lte = ship.y+ ship.bound+max_rad,y__gte = ship.y - check_y - ship.bound-max_rad)
			ships.filter(y__lte = ship.y+ ship.bound+max_bound,y__gte = ship.y - check_y - ship.bound-max_bound)
		for other_ship in ships:
			result = bb_collide(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(other_ship.bound,other_ship.x,other_ship.y,other_ship.vx,other_ship.vy),time)
			#~ print(result)
			if type(result) == float:
				collision_queue.append({'t':result,'type':'ss','pks':(ship.pk,other_ship.pk)})
		for asteroid in asteroids:
			result = bb_collide(to_obj(ship.bound,ship.x,ship.y,ship.vx,ship.vy),to_obj(asteroid.bound,asteroid.x,asteroid.y,0,0),time)
			if type(result) == float:
				collision_queue.append({'t':result,'type':'sa','pks':(ship.pk,asteroid.pk)})
	collision_queue = sorted(collision_queue, key=itemgetter('t'))
	return collision_queue
