#!/usr/bin/env python2

import pygame
import os

class Actor(pygame.sprite.Sprite):
	def __init__(self, charID, fps, zoom):
		pygame.sprite.Sprite.__init__(self)
		
		self.charID = charID
		self.spritePath = "sprites"
		self.spriteFile = "transSprite.png"
		self.sprite = ""
		self.currentLayer = 0
		self.width = 24
		self.height = 32
		self.fps = fps
		self.dirX = 0
		self.dirY = 0
		self.posX = 180
		self.posY = 350

		self.stepSize = 2.0 + (float(zoom) / float(5))
		
		self._images = self.loadSpriteFile()
		
		self._start = pygame.time.get_ticks()
		self._delay = 1000 / self.fps
		self._lastUpdate = 0
		self._frame = 0
		
		self._angle = 0
		self._scale = zoom
		
		self.sprite = pygame.transform.rotozoom(self._images[0], self._angle, self._scale)
		self.collMask = pygame.mask.from_surface(self._images[0], 127)
		
		self.update(pygame.time.get_ticks())
	
	def move(self, direction, collMasks):
		for mask in collMasks:
			dxpos = mask.overlap_area(self.collMask, (int(self.posX+self.stepSize+1),int(self.posY)))
			dypos = mask.overlap_area(self.collMask, (int(self.posX),int(self.posY+self.stepSize+1)))
			dxneg = mask.overlap_area(self.collMask, (int(self.posX-self.stepSize-2),int(self.posY)))
			dyneg = mask.overlap_area(self.collMask, (int(self.posX),int(self.posY-self.stepSize-1)))
			if dxpos != 0 or dypos != 0 or dxneg != 0 or dyneg != 0:
				break
		
		if direction == "up" and dyneg == 0:
				self.dirY = 1
				self.posY = self.posY - self.stepSize
		elif direction == "down" and dypos == 0:
				self.dirY = 0
				self.posY = self.posY + self.stepSize
		elif direction == "left" and dxneg == 0:
				self.dirX = 1
				self.posX = self.posX - self.stepSize
		elif direction == "right" and dxpos == 0:
				self.dirX = 0
				self.posX = self.posX + self.stepSize
		self.update(pygame.time.get_ticks())
	
	def update(self, time):
		if time - self._lastUpdate > self._delay:
			self._frame += 1
			if self._frame >= len(self._images): self._frame = 0

			if self.dirX == 0:
				self.sprite = pygame.transform.rotozoom(self._images[self._frame], self._angle, self._scale)
			elif self.dirX == 1:
				self.sprite = pygame.transform.flip(pygame.transform.rotozoom(self._images[self._frame], self._angle, self._scale),True,False)
			self._lastUpdate = time
			
			self.collMask = pygame.mask.from_surface(self._images[self._frame], 127)
	
	def horizFlip(self):
		if self.dirX == 0:
			self.dirX = 1
		elif self.dirX == 1:
			self.dirX = 0

	def vertFlip(self):
		if self.dirY == 0:
			self.dirY = 1
		elif self.dirY == 1:
			self.dirY = 0

	def loadSpriteFile(self):
		images = []
		
		masterImage = pygame.image.load(os.path.join(self.spritePath, self.spriteFile)).convert_alpha()
		masterWidth, masterHeight = masterImage.get_size()
		
		for i in xrange(int(masterWidth)/self.width):
			images.append(masterImage.subsurface((i*self.width, 0, self.width, self.height)))
		
		return images
	
	def loadDataFromConfigFile(self):
		print "loading character data from file"
		
class Enemy(Actor):
	def whoAreYou(self):
		print "Hi, I'm also an Enemy!\n"

class Player(Actor):
	def whoAreYou(self):
		print "Hi, I'm also a Player!\n"
	
	def attack(self):
		print "Attacking the air! Wooohoooo!"
