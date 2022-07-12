"""
TODO: 
	[]	finish move func
	[done]	set input event for multiple keys
"""

#####################################################
#						Import						#
#####################################################
import pygame, math, random, sys, time
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

OBJECTS = []

DEFAULT_KEYS = {
				"right": {
						"keystrokes": [K_RIGHT, K_d],
						"keystrength": 1
					},
				"left": {
						"keystrokes": [K_LEFT, K_a],
						"keystrength": 1
					},
				"down": {
						"keystrokes": [K_DOWN, K_s],
						"keystrength": 1
					},
				"up": {
						"keystrokes": [K_UP, K_w],
						"keystrength": 1
					}
				}

#####################################################
#						Window						#
#####################################################

class Window(object):

	def __init__(self, width, height, title):
		self.width = width
		self.height = height
		self.title = title

		self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
		pygame.display.set_caption(self.title)

	def update(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		return pygame.display.update()


#####################################################
#						Input						#
#####################################################

class Input(object):

	def __init__(self, setInputEvents):
		self.inputKey = setInputEvents

	def isKeyPressed(self, key):
		keys = pygame.key.get_pressed()

		for keystroke in self.inputKey[key]["keystrokes"]: 
			if keys[keystroke]: return True
		return False

	def getKeyPressed(self):

		keys = pygame.key.get_pressed()
		keyPressed = []

		for inputEvent in self.inputKey:
			for keystroke in self.inputKey[inputEvent]["keystrokes"]: 
				if keys[keystroke] and inputEvent not in keyPressed: keyPressed.append(inputEvent)

		return keyPressed

	def getActionStrength(self, key):

		keys = pygame.key.get_pressed()
		actionStrength = 0
		try:
			for keystroke in self.inputKey[key]["keystrokes"]: 
				if keys[keystroke]: actionStrength = self.inputKey[key]["keystrength"]
		except:
			actionStrength = 1

		return actionStrength


#####################################################
#						Entity						#
#####################################################

class Entity(object):

	def __init__(self, point, width, height, entityType, entityName):
		self.point = point
		self.width = width
		self.height = height
		self.entityType = entityType
		self.entityName = entityName
		self.physics = PhysicsObject(point, width, height) # phy obj
		self.collisionShape2D = self.physics.rect # collision shape for a obj!
		self.color = (0, 0, 0) # Black
		self.sprite = None # obj sprite

		OBJECTS.append({
			"id": len(OBJECTS) - 1,
			"layerName": self.entityName,
			"rect": self.physics.rect,
			"type": self.entityType
		})

	def draw(self, surface):
		return pygame.draw.rect(surface, self.color, self.collisionShape2D)

	def __repr__(self):
		return f"<Entity({self.point}, {self.width}, {self.height}, {self.entityType}, {self.entityName}, {self.physics})>"

#####################################################
#						Physics						#
#####################################################

class PhysicsObject(object):
	def __init__(self, point, width, height):
		self.point = point
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.point.x, self.point.y, self.width, self.height)
		self.collision = None
		self.collideMask = []
		self.movement = Vector2()

	def move(self, movement):
		self.collision = Collision(self, movement)
		return self.collision.FindRectRectCollision(), Vector2(self.point.x, self.point.y)

	def isOnFloor(self):
		if self.collision.bottom: return True
		return False

	def jump(self, gravity, speed, delta, inputEvent, jumpKey):

		# m.x = (inputEvent.getActionStrength("right") - inputEvent.getActionStrength("left")) * 5
		# v = Vector2(
		# 		v.x,
		# 		-10 * 500 if inputEvent.isKeyPressed("up") and player.physics.isOnFloor() else 10 * 5
		# 	)

		# m.y = clamp(m.y, 5)
		# m.y = clamp(m.y, -10)

		# m.y = m.y + delta * v.y
		# v.y = v.y + delta * g.y

		velocity = speed["up"] if inputEvent.isKeyPressed(jumpKey) and self.isOnFloor() else speed["down"]
		self.movement.y = clamp(self.movement.y, speed["down"] / 100 * 10)
		self.movement.y = clamp(self.movement.y, speed["up"] / 100 * 30)

		# main formula
		self.movement.y = self.movement.y + delta * velocity
		velocity = velocity + delta * gravity

		return self.movement

class Collision(object):
	
	top = False
	bottom = False
	left = False
	right = False

	def __init__(self, physicsObject, movement):
		self.physicsObject = physicsObject
		self.movement = movement # point
		self.collisionLevel = 50

	def FindRectRectCollision(self):
		collision = []

		if len(self.physicsObject.collideMask) > 0: #if it has collision mask
			pass

		else: # otherwise collide with static objects
			for object in OBJECTS:
				if object["rect"].colliderect(self.physicsObject.rect) and object["type"] == "static": collision.append(object)


		self.physicsObject.point.x += self.movement.x
		self.physicsObject.rect.x += self.movement.x

		for block in collision:
			# print(abs(block["rect"].top - self.physicsObject.rect.bottom))

			# if block["rect"].width < self.collisionLevel: self.collisionLevel = block["rect"].width * 2

			if abs(block["rect"].left - self.physicsObject.rect.right) < self.collisionLevel and self.movement.x > 0:
				self.physicsObject.rect.right = block["rect"].left + 1
				self.right = True

			if abs(block["rect"].right - self.physicsObject.rect.left) < self.collisionLevel and self.movement.x < 0:
				self.physicsObject.rect.left = block["rect"].right - 1
				self.left = True

		self.physicsObject.point.y += self.movement.y
		self.physicsObject.rect.y += self.movement.y

		for block in collision:
			# print(abs(block["rect"].top - self.physicsObject.rect.bottom))

			# if block["rect"].width < self.collisionLevel: self.collisionLevel = block["rect"].width * 2

			if abs(block["rect"].top - self.physicsObject.rect.bottom) < self.collisionLevel and self.movement.y > 0:
				self.physicsObject.rect.bottom = block["rect"].top + 1
				self.bottom = True

			if abs(block["rect"].bottom - self.physicsObject.rect.top) < self.collisionLevel and self.movement.y < 0:
				self.physicsObject.rect.top = block["rect"].bottom - 1
				self.top = True

		# print(self)

		return self

	def __repr__(self):
		return f"<rect(top={self.top}, bottom={self.bottom}, left={self.left}, right={self.right})>"

class Vector2(object):

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	@property
	def ZERO(self):
		return Vector2(0, 0)

	def __repr__(self):
		return f"<Vector2({self.x, self.y})>"

	def __add__(self, other):
		if isinstance(other, float): return Vector2(self.x + other, self.y + other)
		return Vector2(self.x + other.x, self.y + other.y)

	def __mul__(self, other):
		if isinstance(other, float) or isinstance(other, int): return Vector2(self.x * other, self.y * other)
		return Vector2(self.x * other.x , self.y * other.y)

class Point(object):

	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):
		return f"<Point({self.x, self.y})>"

	def __add__(self, other):
		if isinstance(other, float): return Vector2(self.x + other, self.y + other)
		return Point(self.x + other.x, self.y + other.y)

	def __mul__(self, other):
		if isinstance(other, float): return Vector2(self.x * other, self.y * other)
		return Point(self.x * other.x , self.y * other.y)

def fpsLock(fps):
	return clock.tick(fps)

def clamp(a, b):

	if b > 0:
		if a > b: return b
	elif b < 0:
		if a < b: return b
	return a


#####################################################
#						Test						#
#####################################################

def main():
	window = Window(800, 600, "Test Framework")
	player = Entity(Point(100, 100), 100, 200, "dynamic", "player")
	floor = Entity(Point(0, 600), 1300, 100, "static", "world")
	block = Entity(Point(600, 550), 30, 30, "static", "world")
	inputEvent = Input(DEFAULT_KEYS)

	def playerDraw(delta):
		m = Vector2(
			(inputEvent.getActionStrength("right") - inputEvent.getActionStrength("left")) * 10,
			player.physics.jump(3, {"down": 100, "up": -3000}, delta, inputEvent, "up").y
		)

		player.physics.move(m)
		player.draw(window.screen)

	while True:
		window.screen.fill((255, 255, 255))
		playerDraw(fpsLock(120) / 1000)
		floor.draw(window.screen)
		block.draw(window.screen)

		rect = pygame.Rect(10, 10, 10, 10)
		# print(rect.height)

		window.update()
		fpsLock(120)


if __name__ == '__main__':
	main()
