#!/usr/bin/env python2

class FileHandler:
	def __init__(self, path):
		self.path = path
	
	def openFile(self):
		try:
			file = open(self.path)
		
			return file
		except:
			return false
	
	def readFile(self):
		try:
			self.file.read()
		
			return file
		except:
			return false
	
	def writeFile(self, data):
		try:
			print "writing to file here"
			
			return true
		except:
			return false

class ConfigFile(FileHandler):
	def readConfigValues(self):
		print "Reading config file for file " + str(self.path)

class MapFile(FileHandler):
	def __init__(self, path):
		FileHandler.__init__(FileHandler(path), path)
		print "Reading a map now..."

	def readMap(self):
		print "Reading a map now..."

class ScriptFile(FileHandler):
	def readScript(self):
		print "Reading a script file now..."
