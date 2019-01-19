class Field(object):
	def __init__(self, _field_size=100):
		#sets the field as a square with length field_size
		self.field_size = _field_size
		
		#inits a square deadzone
		self.dz_tl = [40, 60]
		self.dz_tr = [60, 60]
		self.dz_bl = [40, 40]
		self.dz_br = [60, 40]
		self.dz_square = [self.dz_tl, self.dz_tr, self.dz_bl, self.dz_br]

		#set example landmark
		self.landmarks = [[0, 0], [50, 39], [60, 39], [65, 0], [0, 40], [99, 99], [0,99], [99,0], [40, 61], [50, 61], [50, 99]]   

	def getDeadzones(self):
		return self.dz_square

	def getSize(self):
		return self.field_size

	def getLandmarks(self):
		return self.landmarks
