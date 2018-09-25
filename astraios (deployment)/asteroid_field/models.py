from django.db import models
import json
from datetime import datetime

class Asteroid(models.Model):
	name = models.CharField(max_length=254)
	bound = models.FloatField("Bounding radius")
	x = models.FloatField("X coordinate")
	y = models.FloatField("Y coordinate")
	plist = models.CharField("Point list", max_length=510)
	def __str__(self):
		return self.name

class Ship(models.Model):
	name = models.CharField(max_length=254)
	health = models.IntegerField("Current health")
	max_health = models.IntegerField("Maximum health")
	fuel = models.IntegerField("Current fuel")
	max_fuel = models.IntegerField("Maximum fuel")
	isp = models.FloatField("Specific impulse")
	rcs = models.FloatField("Reaction control impulse")
	orientation = models.FloatField("Orientation")
	bound = models.FloatField("Bounding radius")
	x = models.FloatField("X coordinate")
	y = models.FloatField("Y coordinate")
	vx = models.FloatField("X velocity")
	vy = models.FloatField("Y velocity")
	ix = models.FloatField("X impulse",default=0)
	iy = models.FloatField("Y impulse",default=0)
	created_date = models.DateTimeField(default=datetime.now)
	last_modified = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return self.name

class Projectile(models.Model):
	p_type = models.CharField("Projectile type", max_length=255)
	bound = models.FloatField("Bounding radius", default=0.025)
	dmg = models.FloatField("Damage")
	x = models.FloatField("X coordinate")
	y = models.FloatField("Y coordinate")
	vx = models.FloatField("X velocity")
	vy = models.FloatField("Y velocity")
	ix = models.FloatField("X impulse",default=0)
	iy = models.FloatField("Y impulse",default=0)
	created_date = models.DateTimeField(default=datetime.now)
	last_modified = models.DateTimeField(default=datetime.now)
	def __str__(self):
		return self.p_type
