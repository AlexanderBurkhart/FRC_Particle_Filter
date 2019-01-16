from robot import Robot
import random

robot = Robot(0, 20)
print robot.getPos()

robot.set_noise(1.0, 0.1, 1.0)

T = 100
N = 1000
p = []
for i in range(N):
	x = Robot(True)
	x.set_noise(0.05, 0.05, 5.0)
	p.append(x)

for t in range(T):
	robot = robot.move(2, 0)
	dists = robot.sense()

	p2 = []
	for i in range(N):
		p2.append(p[i].move(2, 0))
	p = p2

	w = []
	for i in range(N):
		w.append(p[i].measurement_prob(dists))
	#print w

	p3 = []
	index = int(random.random() * N)
	beta = 0.0
	mw = max(w)
	for i in range(N):
		beta += random.random() * 2.0 * mw
		while beta > w[index]:
			beta -= w[index]
			index = (index + 1) % N
		p3.append(p[index])
	p = p3

	num_p = len(p)
	best_p = Robot()
	highest_weight = -1.0

	for i in range(num_p):
		p_weight = p[i].measurement_prob(dists)
		if p_weight > highest_weight:
			highest_weight = p_weight
			best_p = p[i] 
#	avg_x = 0
#	avg_y = 0	

#	for i in range(N):
#		particle = p[i].getPos()
#		px = particle[0]
#		py = particle[1]
#		avg_x += px
#		avg_y += py

#	avg_p = [avg_x/N , avg_y/N]

	print "Actual Pos:[X: %f Y: %f] Particle Pos:[X: %f Y: %f]" % (robot.x, robot.y, best_p.getPos()[0], best_p.getPos()[1]) 
	#print robot.eval(robot,p)
#print p
