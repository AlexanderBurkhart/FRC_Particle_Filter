import math
import random
from field import Field

class Robot(object):
	#TODO: add noise to move and sense
	#set noise by random.gauss function by using random.gauss(0.0, (insert noise var))
	def __init__(self, x=0, y=0, randomPos=False):
		#init robot at a coordinate x, y
		#print("Initializing")
		self.field = Field(100)
		self.deadzones = self.field.getDeadzones()
		self.world_size = self.field.getSize()
		self.x = x
		self.y = y
		if randomPos:
        		self.x = random.random() * self.world_size
	    		self.y = random.random() * self.world_size
		self.orientation = random.random() * 2.0 * math.pi
	    	self.landmarks = self.field.getLandmarks()
		self.forward_noise = 0.0
		self.turn_noise = 0.0
		self.sense_noise = 0.0

	def move(self, fwd, heading):
		#TODO: Move robot forward a set number of units (fwd) rotate the robot a heading in radians
		self.orientation += heading + random.gauss(0.0, self.turn_noise)
		self.orientation %= 2*math.pi
 
	       	x_fwd = math.sin(self.orientation)*fwd + random.gauss(0.0, self.foward_noise)
        	y_fwd = math.cos(self.orientation)*fwd + random.gauss(0.0, self.foward_noise)

        	self.x += x_fwd
       		self.y += y_fwd
		self.x %= self.world_size
		self.y %= self.world_size
		
		rob = Robot()
		rob.set(self.x, self.y, self.orientation)
		rob.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
		return rob

	def set(self, new_x, new_y, new_orientation):
		self.x = new_x
		self.y = new_y
		self.orientation = new_orientation

	def getPos(self):
		#TODO: Return the position of the robot
		return [self.x, self.y]
	 
     	def lineLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
		uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
		uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

		if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
			return True
		return False

	def isColliding(self, x1, y1, x2, y2, rx1, ry1, rx2, ry2):
		left = self.lineLine(x1, y1, x2, y2, rx1, ry2, rx1, ry1)
		right = self.lineLine(x1, y1, x2, y2, rx2, ry2, rx2, ry1)
		top = self.lineLine(x1, y1, x2, y2 , rx2, ry2, rx1, ry2)
		bottom = self.lineLine(x1, y1, x2, y2, rx2, ry1, rx1, ry1)
	
		if left or right or top or bottom:
			return True
		return False

	def canSense(self, landmark):
		bl = self.deadzones[2]
		tr = self.deadzones[1]
		return not self.isColliding(landmark[0], landmark[1], self.x, self.y, tr[0], tr[1], bl[0], bl[1])

	def sense(self):
		dists = []
		for landmark in self.landmarks:
			if self.canSense(landmark): 
				dist = math.sqrt((self.x - landmark[0]) ** 2 + (self.y - landmark[1]) ** 2)
				dist += random.gauss(0.0, self.sense_noise)
				dists.append(dist)
			else:
				dists.append(-1)
		return dists

	def Gaussian(self, mu, sigma, x):
		return math.exp(-((mu-x) ** 2) / (sigma ** 2)/2.0) / math.sqrt(2.0 * math.pi * (sigma ** 2))

	def measurement_prob(self, measurement):
		prob = 1.0;
		for i in range(len(self.landmarks)):
			landmark = self.landmarks[i]
			dist = math.sqrt((self.x - landmark[0])**2 + (self.y - landmark[1]) ** 2)
			prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
		return prob

	def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
		#TODO: set noise to three vars called forward_noise, turn_noise, sense_noise as floats
		self.foward_noise = new_f_noise
		self.turn_noise = new_t_noise
		self.sense_noise = new_s_noise

	def eval(self, r, p):
		sum = 0.0
		for i in range(len(p)):
			dx = (p[i].x - r.x + (self.world_size/2.0)) % self.world_size - (self.world_size/2.0)
			dy = (p[i].y - r.y + (self.world_size/2.0)) % self.world_size - (self.world_size/2.0)
			err = math.sqrt(dx * dx + dy * dy)
			sum += err
		return sum / float(len(p))

	def __repr__(self):
		return "X: %f Y: %f Heading: %f" % (self.x, self.y, self.orientation)
