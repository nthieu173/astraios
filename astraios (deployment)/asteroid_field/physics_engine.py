from .models import *
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
from math import *
from copy import copy

def collision_resolution(obj1,obj2,time,mod=0):
	#mod=[1,2] asteroid is at position 1 or 2. mod=[-1,-2] projectile is at position 1 or 2
	new_obj1 = copy(obj1)
	new_obj2 = copy(obj2)
	check_result = bb_collide(new_obj1,new_obj2,time)
	if mod == 0:
		result = bb_collision(obj1,obj2,check_result)
		result['time'] = check_result
		return result
	elif mod == 1:
		result = ab_collision(new_obj2,new_obj1,check_result)
		result['time'] = check_result
		return result
	elif mod == 2:
		result = ab_collision(new_obj1,new_obj2,check_result)
		result['time'] = check_result
		return result
	elif mod == -1:
		result = soft_collision(new_obj2,new_obj1,check_result)
		result['time'] = check_result
		return result
	elif mod == -2:
		result = soft_collision(new_obj1,new_obj2,check_result)
		result['time'] = check_result
		return result

def naive_position(obj,t):
	#naively update the position, assuming no collision
	new_obj = copy(obj)
	new_obj['x'] = obj['x']+obj['vx']*t
	new_obj['y'] = obj['y']+obj['vy']*t
	return new_obj

def linear(line):
	#turn 2 points of a line into linear equation form.
	#only works if x1 =/= x2 (when it's not a vertical line)
	m = (line["y1"]-line["y2"])/(line["x1"]-line["x2"])
	b = line["y1"]-m*line["x1"]
	return {'m':m,'b':b}

def bb_collide(obj1,obj2,col_time):
	#bounding circle vs bounding circle
	x_rel = obj1["x"]-obj2["x"]
	y_rel = obj1["y"]-obj2["y"]
	if sqrt((x_rel)**2+(y_rel)**2) < obj1["bound"] + obj2["bound"]:
		return True
	vx_rel = obj1["vx"]-obj2["vx"]
	vy_rel = obj1["vy"]-obj2["vy"]
	if vx_rel == 0 and vy_rel == 0:
		return False
	else:
		t_min = -(x_rel*vx_rel+y_rel*vy_rel)/(vx_rel**2+vy_rel**2)
		a = vx_rel**2+vy_rel**2
		b = 2*(x_rel*vx_rel+y_rel*vy_rel)
		c = x_rel**2+y_rel**2-(obj1["bound"] + obj2["bound"])**2
		delta = b**2-4*a*c
		if delta >= 0:
			t = [(-b +sqrt(delta))/(2*a),(-b -sqrt(delta))/(2*a)]
			for time in t:
				if time > 0 and time <= t_min:
					t = time
					break
		else:
			t = t_min
		if type(t) == list:
			t = t_min
		if t < 0 or t >= col_time:
			return False
		if sqrt((x_rel+vx_rel*t_min)**2+(y_rel+vy_rel*t_min)**2) <= obj1["bound"] + obj2["bound"]:
			return t
		else:
			return False

def pl_collide(point,line,col_time):
	#point vs line
	if (point["x"]-line["x1"])*(point["x"]-line["x2"]) <= 0 and (point["y"]-line["y1"])*(point["y"]-line["y2"]) <= 0 and (point["x"]-line["x1"])/(line["x1"]-line["x2"]) == (point["y"]-line["y1"])/(line["y1"]-line["y2"]):
		return 0
	vx_rel = point["vx"]-line["vx"]
	vy_rel = point["vy"]-line["vy"]
	if line["x1"]-line["x2"] == 0:
		if vx_rel == 0:
			return False
		else:
			t = (point["x"]-line["x1"])/vx_rel
			y_intersect = point["y"] + t*vy_rel
			if (y_intersect-line["y1"])*(y_intersect-line["y2"]) <= 0:
				return t
	else:
		eqline = linear(line)
	if (vy_rel == 0 and vx_rel == 0) or vy_rel == eqline['m']*vx_rel:
		return False
	t = (point["y"]-line["y1"]-eqline['m']*(point["x"]-line["x1"]))/(eqline['m']*vx_rel-vy_rel)
	if t < 0 or t >= col_time:
		return False
	else:
		x_intersect = point["x"] + t*vx_rel
		if (x_intersect-line["x1"])*(x_intersect-line["x2"]) <= 0:
			return t
		else:
			return False

def ab_collision(obj,ast,col_time):
	#return the object right after collision. Asteroid is immovable.
	col_obj = naive_position(obj,col_time)
	if col_obj['x'] == ast['x']:
		alpha = pi/2
		col_obj['vx'] = obj["vx"]
		col_obj['vy'] = -obj["vy"]
	else:
		alpha = atan2(ast['y']-col_obj['y'],ast['x']-col_obj['x'])
		#relative tangental speed
		vt = obj["vy"]*cos(alpha) - obj["vx"]*sin(alpha)
		#relative normal speed. Reverse it.
		vn = -(obj["vx"]*cos(alpha) + obj["vy"]*sin(alpha))
		#convert back to xy system
		col_obj['vx'] = vn*cos(alpha) - vt*sin(alpha)
		col_obj['vy'] = vt*cos(alpha) + vn*sin(alpha)
	return col_obj

def bb_collision(obj1,obj2,col_time):
	#return the objects right after collision. Assume area = mass
	col_obj1 = naive_position(obj1,col_time)
	col_obj2 = naive_position(obj2,col_time)
	m1 = pi*col_obj1['bound']**2
	m2 = pi*col_obj2['bound']**2
	alpha = atan2(col_obj2['y']-col_obj1['y'],col_obj2['x']-col_obj1['x'])
	#set the frame of reference to original obj2's speed
	vx = obj1["vx"]-obj2["vx"]
	vy = obj1["vy"]-obj2["vy"]
	#relative tangental speed
	vt = vy*cos(alpha) - vx*sin(alpha)
	#relative normal speed
	vn = vx*cos(alpha) + vy*sin(alpha)
	#presume only normal speed is affected by ellastic collision.
	vn1 = vn*(m1-m2)/(m1+m2)
	vn2 = vn*2*m1/(m1+m2)
	#convert back to xy system
	col_obj1['vx'] = vn1*cos(alpha) - vt*sin(alpha) + obj2["vx"]
	col_obj1['vy'] = vt*cos(alpha) + vn1*sin(alpha) + obj2["vy"]
	
	col_obj2['vx'] = vn2*cos(alpha) + obj2["vx"]
	col_obj2['vy'] = vn2*sin(alpha) + obj2["vy"]
	return {'obj1':col_obj1,'obj2':col_obj2}

def soft_collision(obj,proj,col_time):
	#return the objects right after collision. Assume area = mass. Projectile is absorbed into target.
	col_obj = naive_position(obj,col_time)
	proj = naive_position(proj,col_time)
	M = pi*col_obj['bound']**2
	m = pi*proj['bound']**2
	obj['vx'] = (M*col_obj['x'] + m*proj['x'])/(M+m)
	obj['vy'] = (M*col_obj['y'] + m*proj['y'])/(M+m)
	return obj

def bl_collide(obj,line,col_time):
	#boundling circle vs line (incomplete, cannot detect collision time)
	# ax +y +c = 0
	eqline = linear(line)
	a_line = -eqline['m']
	c_line = -eqline['b']
	distance = fabs(a_line*obj["x"]+obj["y"]+c_line)/sqrt(a_line**2+1)
	if distance <= obj["bound"]:
		return 0
	vx_rel = obj["vx"]-line["vx"]
	vy_rel = obj["vy"]-line["vy"]
	#ax + y +c =0
	if vx_rel == 0:
		pass
	a_vel = -vy_rel/vx_rel
	c_vel = -a_vel*obj["x"]-obj["y"]
	x_intersect = (c_vel-c_line)/(a_line-a_vel)
	if (x_intersect-line["x1"])*(x_intersect-line["x2"]) <= 0:
		#y=(1/a)x +b
		#check if vel vector cut floated line r distance from first line
		#~ float_line = {"x1":,"y1":,"x2":,"y2":}
		return True
	else:
		min_line1 = fabs(a_vel*line["x1"]+line["y1"]+c_vel)/sqrt(a_vel**2+1)
		min_line2 = fabs(a_vel*line["x2"]+line["y2"]+c_vel)/sqrt(a_vel**2+1)
		if min_line1 <= obj["bound"] or min_line2 <= obj["bound"]:
			return True
		else:
			return False
