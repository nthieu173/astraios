import os
import django
import json
os.environ['DJANGO_SETTINGS_MODULE'] = 'astraios.settings'
django.setup()
from asteroid_field.models import Asteroid

center_x = 3000
center_y = 3000
scale = 20
screen_x = 1200
screen_y = 1200
max_rad = 120
min_x = center_x - (screen_x/scale)*2
max_x = center_x + (screen_x/scale)*2
min_y = center_y - (screen_x/scale)*2
max_y = center_y + (screen_x/scale)*2
offset_x = center_x - screen_x/scale/2
offset_y = center_y + screen_y/scale/2

def delete_all():
	response = input("Sure?(y)")
	if response.lower() == "y":
		Asteroid.objects.all().delete()
		print("Deleted all.")
		return None
	print("Aborted")

def center_asteroid():
	for asteroid in Asteroid.objects.filter(x__gte = min_x, x__lte = max_x, y__gte = min_y, y__lte = max_y):
		print('name',asteroid.name)
		print('x:',asteroid.x)
		print('y:',asteroid.y)
		print('plist:',json.loads(asteroid.plist.replace("'",'"')))
		print("---")
	print("Total",len(Asteroid.objects.filter(x__gte = min_x, x__lte = max_x, y__gte = min_y, y__lte = max_y)),"asteroids.")

print("Options:")
print("1: center_asteroid()")
print("2: delete_all()")
print("3: exit")
while True:
	option = input("Choose a number(1-3): ")
	if option == "1": center_asteroid()
	elif option == "2": delete_all()
	elif option == "3": break
	else: print("Invalid option.")
