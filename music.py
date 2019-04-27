#pygame.mixer.music.load("/home/pi/circuito/semaforo.mp3")
import vlc
import sys
import os
from time import sleep

#~ from clasesna import *


#dir_path = os.path.dirname(os.path.realpath(__file__))
#file_name = 'semaforo.mp3'

class Sonidos():
	def __init__(self):
		self.path="/home/pi/circuito_v1/sonidos"
		#~ self.bgTask = BackgroundTask( self.sSemaforo )
		self.p = vlc.MediaPlayer(self.path + '/semaforo.mp3' )
		self.numRadio = 0
		self.urlRadios = ["http://audio-online.net:8012/live","http://audio-online.net:8006/live","http://audio-online.net:8004/live","http://audio-online.net:8006/live","http://audio-online.net:8005/live"]
		self.nomRadios = ["Loca Latino","Canal Trance","Canal Dance","Canal Remember","Canal House"]

	#~ def sSemaforo(self):

		#~ p.play()
		#~ sleep(5)
	
		#~ p.stop()
		
	def stopsonidos(self):
		self.p.stop()
		#~ try: self.bgTask.stop()
		#~ except: pass 
	def startsemaforo(self):
		self.p = vlc.MediaPlayer(self.path + '/semaforo.mp3' )
		self.p.play()
		
	def startpaso(self):
		self.p = vlc.MediaPlayer(self.path + '/w1.wav' )
		self.p.play()
		
	def startefecto1(self):
		self.p = vlc.MediaPlayer(self.path + '/ring05.wav' )
		self.p.play()
	
		#~ self.bgTask.start()
		#~ try: self.bgTask.start()
		#~ except: pass 
	def claxon(self):
		self.p = vlc.MediaPlayer(self.path + '/claxon.mp3' )
		self.p.play()
		
	def radio(self):
		if self.numRadio <= 3:
			self.numRadio = self.numRadio +1
		else:
			self.numRadio = 0
			
		self.p.stop()
		sleep(1)
		self.p = vlc.MediaPlayer(self.urlRadios[self.numRadio])
		self.p.play()
		return self.nomRadios[self.numRadio]
		

	
	
