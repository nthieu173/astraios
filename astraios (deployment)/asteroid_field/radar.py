import json
from . import models

class ScreenCoordinate:
	def __init__(self,screen_x,screen_y,ast_bound,ship_bound):
		self.x = screen_x
		self.y = screen_y
		self.ship_bound = ship_bound
		self.ast_bound = ast_bound
	def set_view(self,x,y,s):
		self.off = self.offset(x,y,s)
		self.filt = {'ship':self.ship_filt(x,y,s),'ast':self.ast_filt(x,y,s)}
	def offset(self,x,y,s):
		return {'x':x - self.x/(s*2),
				'y':y + self.y/(s*2)}
	def ship_filt(self,x,y,s):
		return {'min':{'x':x - (self.x/(s*2) + self.ship_bound),
						'y':y - (self.y/(s*2) + self.ship_bound)},
				'max':{'x':x + (self.x/(s*2) + self.ship_bound),
						'y':y + (self.y/(s*2) + self.ship_bound)}}
	def ast_filt(self,x,y,s):
		return {'min':{'x':x - (self.x/(s*2) + self.ast_bound),
						'y':y - (self.y/(s*2) + self.ast_bound)},
				'max':{'x':x + (self.x/(s*2) + self.ast_bound),
						'y':y + (self.y/(s*2) + self.ast_bound)}}

def neighbor_ship(x,y,s):
	ship_list = []
	for ship in models.Ship.objects.filter(x__gte = screen.filt['ship']['min']['x'],
											x__lte = screen.filt['ship']['max']['x'],
											y__gte = screen.filt['ship']['min']['y'],
											y__lte = screen.filt['ship']['max']['y']):
		ship_list.append({"name":ship.name,
						"x":(ship.x-screen.off['x']),
						"y":(screen.off['y']-ship.y),
						"o":ship.orientation})
	return ship_list

def neighbor_ast(x,y,s):
	ast_list = []
	for asteroid in models.Asteroid.objects.filter(x__gte = screen.filt['ast']['min']['x'],
													x__lte = screen.filt['ast']['max']['x'],
													y__gte = screen.filt['ast']['min']['y'],
													y__lte = screen.filt['ast']['max']['y']):
		ast_list.append({"cen":{"x":(asteroid.x-screen.off['x']),"y":(screen.off['y']-asteroid.y)},
					"plist":json.loads(asteroid.plist.replace("'",'"'))})
	return ast_list

screen = ScreenCoordinate(1200,1200,120,2) 
