#!/usr/bin/env python2

import pygame

def load_sound(name):
	class No_Sound:
		def play(self): pass

	if not pygame.mixer or not pygame.mixer.get_init():
		return No_Sound()

	fullname = os.path.join('data', name)
	if os.path.exists(full_name) == False:
		sound = pygame.mixer.Sound(fullname)
	else:
		print 'File does not exist:', fullname
		return No_Sound

	return sound
