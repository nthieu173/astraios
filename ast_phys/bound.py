from math import *

def bb_collide(obj1,obj2,col_time):
	x_rel = obj1["x"]-obj2["x"]
	y_rel = obj1["y"]-obj2["y"]
	vx_rel = obj1["vx"]-obj2["vx"]
	vy_rel = obj1["vy"]-obj2["vy"]
	d_now = sqrt((x_rel)**2+(y_rel)**2)
	if d_now < obj1["bound"] + obj2["bound"]:
		return True
	elif vx_rel == 0 and vy_rel == 0:
		return False
	else:
		t_min = -(x_rel*vx_rel+y_rel*vy_rel)/(vx_rel**2+vy_rel**2)
		if t_min < 0 or t_min >= col_time:
			return False
		elif sqrt((x_rel+vx_rel*t_min)**2+(y_rel+vy_rel*t_min)**2) < obj1["bound"] + obj2["bound"]:
			return True
		else:
			return False

def pl_collide(point,line,col_time):
	vx_rel = point["vx"]-line["vx"]
	vy_rel = point["vy"]-line["vy"]
	m = (line["y1"]-line["y2"])/(line["x1"]+line["x2"])
	b = line["y1"]-m*line["x1"]
	if (point["x"]-line["x1"])*(point["x"]-line["x2"]) <= 0 and (point["y"]-line["y1"])*(point["y"]-line["y2"]) <= 0 and (point["x"]-line["x1"])/(line["x1"]-line["x2"]) == (point["y"]-line["y1"])/(line["y1"]-line["y2"]):
		return True
	elif (vy_rel == 0 and vx_rel == 0) or vy_rel/vx_rel == m:
		return False
	else:
		t = (point["y"]-line["y1"]-m*(point["x"]-line["x1"]))/(m*vx_rel-vy_rel)
		if t < 0 or t >= col_time:
			return False
		else:
			x_intersect = point["x"] + t*vx_rel
			y_intersect = point["y"] + t*vy_rel
			if (x_intersect-line["x1"])*(x_intersect-line["x2"]) <= 0 and (y_intersect-line["y1"])*(y_intersect-line["y2"]) <= 0:
				return True
			else:
				return False

obj_1 = {"bound":1,"x":0,"y":0,"vx":4,"vy":4}
obj_2 = {"bound":1,"x":10,"y":0,"vx":0,"vy":3}
point = {"x":0,"y":0,"vx":-1,"vy":5}
line = {"x1":5,"y1":0,"x2":0,"y2":5,"vx":0,"vy":0}

print(pl_collide(point,line,100))
