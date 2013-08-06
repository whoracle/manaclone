#!/usr/bin/env python2

from . import Actor

class Enemy(Actor.Actor):
	def whoAreYou(self):
		print "Hi, I'm also an Enemy!\n"