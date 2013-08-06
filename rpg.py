#!/usr/bin/env python2

# We import our character library here
from libs import *
import pygame

class RPG:
	def __init__(self, xres=640, yres=480, zoom=1):
		pygame.init()
		
		self.zoomFactor = zoom
		self.screenWidth = xres * zoom
		self.screenHeight = yres * zoom
		self.spriteWidth = 24
		self.spriteHeight = 32
		
		self.window = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption("RPG Engine")
		self.screen = pygame.display.get_surface()
		
		self.scanlines = (0,0,0)
		self.mode_scanlines = False
		self.mode_help = True
		self.mode_info = False
		self.mode_hud = True
		self.mode_joystick = False

		if pygame.joystick.get_count() != 0:
			self.joystick = pygame.joystick.Joystick(0)
			self.joystick.init()

		self.fps = 5

		self.myPlayer = Actor.Player(0, self.fps, self.zoomFactor)
		self.myPlayer.whoAreYou()
		
		self.myConfig = FileHandlers.ConfigFile("dummy")
		
		self.maps = []
		self.scripts = []

		self.world = World.World(self.zoomFactor, "map001.map")
		self.collMask = pygame.mask.from_surface(self.world.mapColl[0], 127)
		self.collMasks = []
		self.collMasks.append(self.collMask)
		
		self.hud = Hud.Hud()
		
		self.hlpTxt = []
		self.hlpTxtPos = []
		
		self.txtBox = pygame.Surface((350,200))
		self.txtBox.set_alpha(50)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("h - Toggle this help text")
		self.helpText1.set_alpha(255)
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 10
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 30
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("t - Toggle status information")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 50
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("m - Toggle scanlines")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 70
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("f - Toggle fullscreen")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 90
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("j - Gamepad On/Off")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 110
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 130
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("w,a,s,d - Move around")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 150
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 170
		self.hlpTxtPos.append(self.helpTextPos1)
		
		self.helpText1, self.helpTextPos1 = self.prepareFont("q - Quit")
		self.hlpTxt.append(self.helpText1)
		self.helpTextPos1.centery = 10
		self.helpTextPos1.centery = 190
		self.hlpTxtPos.append(self.helpTextPos1)
		
		for i in range(0, len(self.hlpTxt)):
			self.txtBox.blit(self.hlpTxt[i], self.hlpTxtPos[i])

	def prepareFont(self, text, size=30):
		font = pygame.font.Font(None, int(size))
		helpText = font.render(str(text), 1, (10,10,10))
		helpTextPos = helpText.get_rect()
		
		return helpText, helpTextPos
	
	def getInfoTxt(self):
		text = "FPS: " + str(self.fps) + " | Zoom Factor: " + str(self.zoomFactor) + " | xres X yres: " + str(self.screenWidth / self.zoomFactor) + "x" + str(self.screenHeight / self.zoomFactor)
		font = pygame.font.Font(None, 30)
		statText = font.render(str(text), 1, (10,10,10))
		statTextPos = statText.get_rect()
		statTextPos.centerx = ( self.screenWidth / 2 )
		statTextPos.centery = ( self.screenHeight - 100 )
		
		return statText, statTextPos
	
	def getStatusTxt(self):
		text = "Pos X: " + str(self.myPlayer.posX) + " Pos Y: " + str(self.myPlayer.posY)# + "\nCollPosX: " + str(self.myPlayer.collX) + " CollPosY: " + str(self.myPlayer.collY)
		font = pygame.font.Font(None, 24)
		statText = font.render(str(text), 1, (10,10,10))
		statTextPos = statText.get_rect()
		statTextPos.centerx = 600
		statTextPos.centery = 10
		
		return statText, statTextPos

	def drawScanLines(self, screen):
		if self.mode_scanlines:
			for i in range(0, self.screenHeight):
				pygame.draw.line(screen, self.scanlines, (0, i * ( 2 * self.zoomFactor )), (self.screenWidth, (i * ( 2 * self.zoomFactor ))), self.zoomFactor)
	
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
	
	def run(self):
		running = 1
		
		posx = 0
		posy = 100
		dirx = 0
		diry = 0
		backgroundColor = (0,0,0)
		
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = 0
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_h:
						if self.mode_help == True:
							self.mode_help = False
						elif self.mode_help == False:
							self.mode_help = True
					elif event.key == pygame.K_m:
						if self.mode_scanlines == False:
							self.mode_scanlines = True
						elif self.mode_scanlines == True:
							self.mode_scanlines = False
					elif event.key == pygame.K_j:
						if self.mode_joystick == False:
							self.mode_joystick = True
						elif self.mode_joystick == True:
							self.mode_joystick = False
					elif event.key == pygame.K_t:
						if self.mode_info == False:
							self.mode_info = True
						elif self.mode_info == True:
							self.mode_info = False
					elif event.key == pygame.K_f:
						pygame.display.toggle_fullscreen()
					elif event.key == pygame.K_q:
						quit()
					elif event.key == pygame.K_SPACE:
						self.myPlayer.attack()
				if self.mode_joystick:
					if event.type == pygame.JOYBUTTONDOWN:
						if event.button == 1:
							self.myPlayer.attack()

			keysPressed = pygame.key.get_pressed()

			if self.mode_joystick:
				joyAxisX = self.joystick.get_axis(0)
				joyAxisY = self.joystick.get_axis(1)
				
				if joyAxisX != 0.0:
					if joyAxisX < 0.0:
						self.myPlayer.move("left", self.collMasks)
					elif joyAxisX > 0.0:
						self.myPlayer.move("right", self.collMasks)
				
				if joyAxisY != 0.0:
					if joyAxisY < 0.0:
						self.myPlayer.move("up", self.collMasks)
					elif joyAxisY > 0.0:
						self.myPlayer.move("down", self.collMasks)

			if keysPressed[pygame.K_w] == 1:
				if keysPressed[pygame.K_s] != 1:
					if self.myPlayer.posY > 0:
						self.myPlayer.move("up", self.collMasks)
						
			if keysPressed[pygame.K_s] == 1:
				if keysPressed[pygame.K_w] != 1:
					if self.myPlayer.posY + (self.myPlayer.height * 2) < self.screenHeight:
						self.myPlayer.move("down", self.collMasks)
						
			if keysPressed[pygame.K_a] == 1:
				if keysPressed[pygame.K_d] != 1:
					if self.myPlayer.posX > 0:
						self.myPlayer.move("left", self.collMasks)
						
			if keysPressed[pygame.K_d] == 1:
				if keysPressed[pygame.K_a] != 1:
					if self.myPlayer.posX + (self.myPlayer.width * 2) < self.screenWidth:
						self.myPlayer.move("right", self.collMasks)

			if posx == 0:
				dirx = 0
				self.myPlayer.horizFlip()
			if posx == (self.screenWidth - (self.spriteWidth * 2)):
				dirx = 1
				self.myPlayer.horizFlip()

			if dirx == 0:
				posx = posx + 1
			elif dirx == 1:
				posx = posx - 1
			if diry == 0:
				posy = posy
			elif diry == 1:
				posy = posy
			
			for layer in range(0, int(self.world.layers)):
				# layer = 0
				self.screen.blit(self.world.mapLow[layer], (self.world.posX,self.world.posY))
				self.screen.blit(self.world.mapColl[layer], (self.world.posX,self.world.posY))
				if self.myPlayer.currentLayer == layer:
					self.screen.blit(self.myPlayer.sprite, (self.myPlayer.posX, self.myPlayer.posY))
				self.screen.blit(self.world.mapHigh[layer], (self.world.posX,self.world.posY))

			if self.mode_help:
				self.screen.blit(self.txtBox, (0,0))
				for i in range(0, len(self.hlpTxt)):
					self.screen.blit(self.hlpTxt[i], self.hlpTxtPos[i])
			if self.mode_info:
				infoTxt, infoTxtPos = self.getInfoTxt()
				self.screen.blit(infoTxt,infoTxtPos)
			if self.mode_hud:
				self.screen.blit(self.hud.frames, self.hud.framePosition)
				self.screen.blit(self.hud.pcImg, self.hud.pcImgPosition)
			
			statusTxt, statusTxtPos = self.getStatusTxt()
			self.screen.blit(statusTxt,statusTxtPos)
			
			self.drawScanLines(self.screen)
			pygame.display.flip()
			self.screen.fill(backgroundColor)
			pygame.time.delay(self.fps)

if __name__ == "__main__":
	game = RPG(768, 768, 1)
	game.run()
