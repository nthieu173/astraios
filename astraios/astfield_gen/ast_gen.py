from math import *
import random

#~ def ast_field():
	

def field_plist(num_points,rad,x_lim,y_lim):
	point_list=[]
	count = 0
	while count < num_points:
		print(count,end="\r")
		x=random.uniform(0,x_lim)
		y=random.uniform(0,y_lim)
		if dont_overlap(x,y,rad,point_list):
			point_list.append((x,y))
			count += 1
	return point_list

def dont_overlap(x_point,y_point,rad,point_list):
	check_list=[]
	for point in point_list:
		x,y=point
		if fabs(x - x_point) < 2*rad or fabs(y - y_point) < 2*rad:
			if sqrt((x - x_point)**2+(y - y_point)**2) < 2*rad:
				return False
	return True

def ast_plist(min_rad, max_rad, spokes, delta_ang):
	spoke_ang_list = []
	count = 0
	while count < spokes:
		spoke_ang_list.append(2*count*pi/spokes+random.uniform(-delta_ang,delta_ang))
		count += 1
	ast_plist = []
	rad = random.randrange(min_rad,max_rad)
	for spoke in spoke_ang_list:
		rad_change = random.uniform(-rad/3,rad/3)
		while rad + rad_change > max_rad or rad + rad_change < min_rad:
			rad_change += random.uniform(-rad/3,rad/3)
		rad += rad_change
		ast_plist.append({"x":round(rad*cos(spoke),9),"y":round(rad*sin(spoke),9)})
	return ast_plist

#~ print(ast_plist(7,120,8,pi/8))

def ast_combined(field_tuple,ast_tuple):
	num_points, rad, x_bound, y_bound = field_tuple
	max_rad, min_rad, spokes, delta_rad, delta_ang = ast_tuple
	field = field_plist(num_points, rad, x_bound, y_bound)
	ast_field = []
	count = 0
	for ast in field:
		count += 1
		cen_x,cen_y = ast
		ast_field.append({"cen":{"x":cen_x,"y":cen_y},"plist":ast_plist(min_rad, max_rad, spokes, delta_rad, delta_ang)})
		print(count,end="\r")
	return ast_field
#~ print(ast_combined((100,60,10**6,10**6),(55,15,8,10,pi/8)))
#~ print(ast_field((100,50,1200,1200),(50,20,8,10,pi/8)))
