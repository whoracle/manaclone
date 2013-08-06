#!/usr/bin/env python2

class Object:
	def __init__(self):
		print "Hi, I'm an Object!"

class Animate(Object):
	def whoAreYou(self):
		print "Hi, I'm an Animate Object!"

class Inanimate(Object):
	def whoAreYou(self):
		print "Hi, I'm an Inanimate Object!"
