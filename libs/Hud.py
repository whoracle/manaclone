#!/usr/bin/env python2

import pygame

class Hud:
	def __init__(self):
		self.framePosition = (540,900)
		self.pcImgPosition = (548,912)	# Versatz ist: x + 12, y + 18
		self.frames = pygame.image.load("sprites/hud/frame.png").convert_alpha()
		self.pcImg = pygame.transform.rotozoom(pygame.image.load("sprites/hud/pcimg.png").convert_alpha(),0,1.5)
		#self.hpBar = pygame.image.load("sprites/hud/hpbar.png").convert_alpha()
		#self.mpBar = pygame.image.load("sprites/hud/mpbar.png").convert_alpha()
		#self.strBar = pygame.image.load("sprites/hud/strbar.png").convert_alpha()
