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
