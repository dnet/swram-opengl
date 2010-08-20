#!/usr/bin/env python

import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from threading import Thread, Lock, Event

class Camera:
	zoom = 1.0

class SwarmEntity:
	def __init__(self, line):
		parts = line.split()
		self.x = float(parts[0])
		self.y = float(parts[1])
		self.z = float(parts[2])

class Reader(Thread):
	lock = Lock()
	changed = Event()
	swarm_entities = []
	def run(self):
		print 'Waithing for data on stdin'
		while True:
			self.read_entities()

	def read_entities(self):
		entities = []
		while True:
			line = sys.stdin.readline()
			if 'done' in line:
				break
			try:
				entities.append(SwarmEntity(line))
			except:
				print 'Invalid line:', line
		self.done(entities)

	def done(self, entities):
		print 'Updating view'
		Reader.lock.acquire()
		Reader.swarm_entities = entities
		Reader.lock.release()
		Reader.changed.set()

def idle():
	if Reader.changed.isSet():
		Reader.changed.clear()
		glutPostRedisplay()

def display():
	glLoadIdentity()
	dist = 20.0 / Camera.zoom
	gluLookAt(dist, dist, dist, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
	axis()
	glColor3f(0.0, 1.0, 0.0)
	mySphere = gluNewQuadric()
	gluQuadricDrawStyle(mySphere, GLU_LINE)
	
	Reader.lock.acquire()
	for entity in Reader.swarm_entities:
		glPushMatrix()
		glTranslatef(entity.x, entity.y, entity.z)
		gluSphere(mySphere, 1.0, 12, 12)
		glPopMatrix()
	Reader.lock.release()
	
	glFlush()
	
def axis():
	glClear(GL_COLOR_BUFFER_BIT)
	
	glBegin(GL_LINES)
	glColor3f(0.3, 0.3, 0.3)
	glVertex3f(-10.0, 0.0, 0.0)
	glVertex3f(10.0, 0.0, 0.0)
	glVertex3f(0.0, -10.0, 0.0)
	glVertex3f(0.0, 10.0, 0.0)
	glVertex3f(0.0, 0.0, -10.0)
	glVertex3f(0.0, 0.0, 10.0)
	glEnd()

	biggest = 10
	x = 88
	y = 89
	z = 90
	r = range (0, (biggest + 1))
	for i in r:
		ascii = 48+i

		# x axis positive
		glRasterPos3f(i, 0.0, 0.0)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, x)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# x axis negative
		glRasterPos3f(-i, 0.0, 0.0)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, x)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)

		# y axis positive
		glRasterPos3f(0.0, i, 0.0)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, y)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# x axis negative
		glRasterPos3f(0.0, -i, 0.0)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, y)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)

		# z axis positive
		glRasterPos3f(0.0, 0.0, i)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, z)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# z axis negative
		glRasterPos3f(0.0, 0.0, -i)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, z)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
	
	glFlush()
	
def init():
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glColor3f(0.0, 0.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(30, 1.0, 0.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def mykeyb(key, x, y):
	if key == '+':
		Camera.zoom *= 1.2
	elif key == '-':
		Camera.zoom /= 1.2
	else:
		return
	print 'Zoom is now', Camera.zoom
	glutPostRedisplay()

def mymouse(but, stat, x, y):
	if stat == GLUT_DOWN:
		if but == GLUT_LEFT_BUTTON:
			print x, y, "Press right button to exit"
		else:
			sys.exit()
		
glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow('Swarm visualization')
glutDisplayFunc(display)
glutKeyboardFunc(mykeyb)
glutMouseFunc(mymouse)
glutIdleFunc(idle)

init()
rdr = Reader()
rdr.start()
glutMainLoop()
