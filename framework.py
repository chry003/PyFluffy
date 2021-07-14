"""
TODO: 
	[]	finish move func
	[done]	set input event for multiple keys
"""

#####################################################
#						Import						#
#####################################################
import pygame, math, random, sys
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

OBJECTS = []

DEFAULT_KEYS = {
				"right": {
						"keystrokes": [K_RIGHT, K_d],
						"keystrength": -1
					},
				"left": {
						"keystrokes": [K_LEFT, K_a],
						"keystrength": 1
					},
				"down": {
						"keystrokes": [K_DOWN, K_s],
						"keystrength": -1
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

#####################################################
#						Entity						#
#####################################################

class Entity(object):

	def __init__(self, vec2, width, height, entityType, entityName):
		self.vec2 = vec2
		self.width = width
		self.height = height
		self.entityType = entityType
		self.entityName = entityName
		self.physics = PhysicsObject(vec2, width, height) # phy obj
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

#####################################################
#						Physics						#
#####################################################

class PhysicsObject(object):
	def __init__(self, vec2, width, height):
		self.vec2 = vec2
		self.width = width
		self.height = height
		self.rect = pygame.Rect(self.vec2.x, self.vec2.y, self.width, self.height)
		self.collision = None
		self.collideMask = []

	def move(self, movement):
		self.collision = Collision(self, movement)
		return self.collision.FindRectRectCollision(), Vector2(self.vec2.x, self.vec2.y)

	def isOnFloor(self):
		if self.collision.bottom: return True
		return False

class Collision(object):
	
	top = False
	bottom = False
	left = False
	right = False

	def __init__(self, physicsObject, movement):
		self.physicsObject = physicsObject
		self.movement = movement # Vec2
		self.collisionLevel = 50

	def FindRectRectCollision(self):
		collision = []

		if len(self.physicsObject.collideMask) > 0: #if it has collision mask
			pass

		else: # otherwise collide with static objects
			for object in OBJECTS:
				if object["rect"].colliderect(self.physicsObject.rect) and object["type"] == "static": collision.append(object)


		self.physicsObject.vec2.x += self.movement.x
		self.physicsObject.rect.x += self.movement.x

		for block in collision:
			# print(abs(block["rect"].top - self.physicsObject.rect.bottom))
			if abs(block["rect"].left - self.physicsObject.rect.right) < self.collisionLevel and self.movement.x > 0:
				self.physicsObject.rect.right = block["rect"].left + 1
				self.right = True

			if abs(block["rect"].right - self.physicsObject.rect.left) < self.collisionLevel and self.movement.x < 0:
				self.physicsObject.rect.left = block["rect"].right - 1
				self.left = True

		self.physicsObject.vec2.y += self.movement.y
		self.physicsObject.rect.y += self.movement.y

		for block in collision:
			# print(abs(block["rect"].top - self.physicsObject.rect.bottom))
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

	def clamp(self, a, b):

		if a > b: return b
		return a

	def __repr__(self):
		return f"<Vector2({self.x, self.y})>"

	def __add__(self, other):
		return Vector2(self.x + other.x, self.y + other.y)

	def __mul__(self, other):
		# if isinstance(other, float): return Vector2(self.x * other, self.y * other)
		return Vector2(self.x * other.x , self.y * other.y)

def fpsLock(fps):
	return clock.tick(fps)

#####################################################
#						Test						#
#####################################################

def main():
	window = Window(800, 600, "Test Framework")
	player = Entity(Vector2(100, 100), 100, 200, "dynamic", "player")
	floor = Entity(Vector2(50, 500), 600, 50, "static", "player")

	inputEvent = Input(DEFAULT_KEYS)
	movement = Vector2()

	delta = fpsLock(60) / 1000

	def playerDraw():
		movement.y += 10 * delta
		movement.y = movement.clamp(movement.y, 2)

		player.draw(window.screen)
		player.physics.move(movement)

	while True:
		window.screen.fill((255, 255, 255))
		playerDraw()
		floor.draw(window.screen)
		window.update()
		fpsLock(60)


if __name__ == '__main__':
	main()