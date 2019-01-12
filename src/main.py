from robot import Robot
import random

robot = Robot(10, 50)
print robot.getPos()

robot.set_noise(2.0, 0.1, 2.0)

T = 100
N = 1000
p = []
for i in range(N):
	x = Robot()
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

	avg_x = 0
	avg_y = 0	

	for i in range(N):
		particle = p[i].getPos()
		px = particle[0]
		py = particle[1]
		avg_x += px
		avg_y += py

	avg_p = [avg_x/N , avg_y/N]

	print "Actual Pos:[X: %f Y: %f] Particle Pos:[X: %f Y: %f]" % (robot.x, robot.y, avg_p[0], avg_p[1]) 
	#print robot.eval(robot,p)
#print p
