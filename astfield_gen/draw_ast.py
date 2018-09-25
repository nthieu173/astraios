#~ from tkinter import *
from math import *
import random
import time

#~ master = Tk()
#~ w = Canvas(master, width=1200, height=700)
#~ w.pack()

#random a tuple list from 0-x_bound and 0-y_bound. deprecated
def ran_plist(num_points,x_bound,y_bound):
	count = 0
	point_list = []
	while count < num_points:
		point_list.append((random.uniform(x_bound),random.uniform(y_bound)))
		count += 1
	return point_list

#Started as a more gentle way to change radius, side effect included variable radius and variable spokes.
def ast_plist_gentle(cen_x, cen_y, max_rad, min_rad, spokes, delta, delta_angle):
	spokes_list = []
	count = 0
	while count < spokes:
		#generate a new spoke point, randomized betweent the two dela_angle extremes
		spokes_list.append(2*count*pi/spokes+random.uniform(-delta_angle,delta_angle))
		count += 1
	point_list = []
	rad = random.randrange(min_rad,max_rad)
	for spoke in spokes_list:
		#randomly generate a delta radius, change radius compared to baseline with delta
		rdelta = random.uniform(-delta,delta)
		while rad+rdelta > max_rad or rad+rdelta <min_rad:
			rdelta = random.uniform(-delta,delta)
		rad += rdelta
		point_list.append([round(cen_x+rad*cos(spoke),9),round(cen_y+rad*sin(spoke),9)])
	return point_list

#Minor asteroid radius variable, variable spokes
def ast_plist_spiky(cen_x, cen_y, max_rad, min_rad, spokes):
	point_list = []
	p_angle = 2*pi/spokes
	count = 0
	while count < spokes:
		point_list.append((
						cen_x+random.uniform(min_rad,max_rad)*cos(count*p_angle),
						cen_y+random.uniform(min_rad,max_rad)*sin(count*p_angle)))
		count += 1
	return point_list

#No asteroid radius variable, regular spokes
def ast_plist_tame(cen_x, cen_y, max_rad, min_rad, spokes):
	point_list = []
	p_angle = 2*pi/spokes
	count = 0
	while count < spokes:
		rad = random.randrange(min_rad,max_rad)
		point_list.append((
						cen_x+rad*cos(count*p_angle),
						cen_y+rad*sin(count*p_angle)))
		count += 1
	return point_list

#create circle at point. Used for testing point distribution
def circle_all(point_list,nradius):
	for point in point_list:
		x,y=point
		w.create_oval(x-nradius,y-nradius,x+nradius,y+nradius,fill='red')

#check if point inputted had any within a radius in that other list, only check those close enough.
def dont_overlap(x_point,y_point,rad,point_list):
	check_list=[]
	for point in point_list:
		x,y=point
		if fabs(x - x_point) < rad*2 or fabs(y - y_point) < rad*2:
			if sqrt((x - x_point)**2+(y - y_point)**2) < rad*2:
				return False
	return True

#final iteration of random point list for asteroid distribution.
def noverlap_plist(num_points,rad,x_bound,y_bound):
	point_list=[]
	count = 0
	while count < num_points:
		x=random.randrange(x_bound)
		y=random.randrange(y_bound)
		if dont_overlap(x,y,rad,point_list):
			point_list.append((x,y))
			count += 1
	return point_list

#creating a list of list of point lists to draw an entire asteroid field
def ast_all():
	point_list=noverlap_plist(500,18,1200,1200)
	field_plist=[]
	for cen in point_list:
		x,y=cen
		field_plist.append(ast_plist_gentle(x,y,17,5,8,3,pi/8))
	return field_plist

def write_to_file():
	file = open('ast_out.txt', 'w')
	file.write(str(ast_all()))
	file.close()

write_to_file()

#~ mainloop()
