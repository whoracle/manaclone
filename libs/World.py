#!/usr/bin/env python2

import pygame, os

class World:
	def __init__(self, zoom, filename):
		self._scale = zoom
		self._angle = 0
		self.posX = 0
		self.posY = 0
		self.filename = filename
		self.img ="map001.png"
		self.retData = []
		
		self.layerLow = []
		self.layerColl = []
		self.layerHigh = []
		
		self.mapLow = []
		self.mapColl = []
		self.mapHigh = []
		
		self.mapData = self.readMapFile()
		self.loadedLayers = self.loadLayer(self.mapData[2])
		
	def readMapFile(self):
		file = open("maps/" + str(self.filename),'r')
		sep = "="

		# load general settings for the map here
		for line in file:
			if line.rpartition(sep)[0] == "name":
				self.name = line.rpartition(sep)[2].strip("\n")
			if line.rpartition(sep)[0] == "script":
				self.script = line.rpartition(sep)[2].strip("\n")
			if line.rpartition(sep)[0] == "width":
				self.width = line.rpartition(sep)[2].strip("\n")
			if line.rpartition(sep)[0] == "height":
				self.height = line.rpartition(sep)[2].strip("\n")
			if line.rpartition(sep)[0] == "layers":
				self.layers = line.rpartition(sep)[2].strip("\n")
			if line.rpartition(sep)[0] == "tilesize":
				self.tilesize = line.rpartition(sep)[2].strip("\n")

			# load exits here
			# Still to implement

			# load layers here
			if line.rpartition(sep)[0] == "maplayer":
				low = line.rpartition(sep)[2].strip("\n") + "_low.png"
				coll = line.rpartition(sep)[2].strip("\n") + "_coll.png"
				high = line.rpartition(sep)[2].strip("\n") + "_high.png"

				self.layerLow.append(low)
				self.layerColl.append(coll)
				self.layerHigh.append(high)

		# build and return our gathered data
		self.retData.append(self.name)
		self.retData.append(self.script)
		self.retData.append(self.layers)
		self.retData.append(self.width)
		self.retData.append(self.height)
		self.retData.append(self.tilesize)
				
		return self.retData

	def loadLayer(self, layerCount):
		# for now, this loads just one layer.
		# add logic to load n later
		self.mapX, self.mapY = pygame.image.load("maps/" + self.layerLow[0]).convert_alpha().get_size()
		for layer in range(0, int(layerCount)):
			self.mapLow.append(pygame.image.load("maps/" + self.layerLow[layer]).convert_alpha())
			self.mapColl.append(pygame.image.load("maps/" + self.layerColl[layer]).convert_alpha())
			self.mapHigh.append(pygame.image.load("maps/" + self.layerHigh[layer]).convert_alpha())

		if self._scale != 1:
			self.mapImg = pygame.transform.rotozoom(self.mapImg, self._angle, self._scale)
