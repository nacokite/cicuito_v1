# encoding: utf8
from __future__ import unicode_literals
import sys
import os
import vlc
try:
    import tkinter as tk
    from tkinter import messagebox
except:
    import Tkinter as tk
    import tkMessageBox as messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

import pygubu

from clasesna import *
from time import sleep      
from motor import Motor
from music import Sonidos
from db import DB

from xbox import Joystick
         
button_delay = 0.1
ROJO='#ff0000'
VERDE='#86FF23'

accOn = False
a=0

class Myapp:
    accJ1=0
    joy = Joystick(0)
    joy2 = Joystick(1)
    def __init__(self, master):
        self.master = master
        self.db = DB() 
        self.db.abrir()
        self.mot = Motor()
        self.son = Sonidos()
        self.texto = ""
        self.pilotoAuto = False
        self.motstop = True
        self.nvueltajug1 =0
        self.tmpvueltajug1 = ""
        self.pasoj1= False
        self.accJ1= 0
        self.grabavuelta = False
        self.playvuelta = False

        
        master.title( "circuito" )
        master.geometry("800x600")
        self.builder = builder = pygubu.Builder()
        fpath = os.path.join(os.path.dirname(__file__),"pantalla.ui")
        builder.add_from_file(fpath)
        
        
        mainwindow = builder.get_object('frmpal', master)
        self.lsttmp2 = lbox = builder.get_object('lsttiempos')
        
        self.cargapilotos()
        self.cargacoches()
      
      
        
        self.timerms_=0
        self.timers_=0
        self.timerm_=0
        
        
        #~ self.bgTask = BackgroundTask( self.myLongProcess )
        #~ self.timer =BackgroundTask (self.onTimer)
        
        #~ self.timer = TkRepeatingTask( self.master, self.onTimer, 1)
        #~ self.xbTask =BackgroundTask (self.procesoMandoXbox )
        

        builder.connect_callbacks(self)
        self.timer = TkRepeatingTask( self.master, self.onTimer, 1)
        self.xbTask =BackgroundTask (self.procesoMandoXbox )
        
    def cargapilotos(self):
        self.lstpiloto = self.builder.get_object('lstpiloto')
        pilotos = self.db.recuperar_todos("usuarios")
        for row in pilotos:
             self.lstpiloto.insert(tk.END, row) 
             
    def cargacoches(self):
        self.lstcoches =self.builder.get_object('lstcoches')
        coches = self.db.recuperar_todos("coches")
        for row in coches:
             self.txt= str(row[0]) + " " + str(row[1])
             self.lstcoches.insert(tk.END, self.txt)     
             
    def close( self ) :
        print "close"
        try: self.xbTask.stop()
        except: pass
        try: self.timer.stop()
        except: pass            
        self.master.quit()        
 
              
    def onTimerClicked( self ):
        #~ print "onTimerClicked"
        #~ self.timer.start() 
        try: self.timer.start()
        except: pass      
          
    def onTimerstop( self ):
        #~ print "onTimerstiop"
        self.timer.stop()
         
        
    def onTimerclear( self ):
        #~ print "onTimerclear"
        self.timerms_=0
        self.timers_=0
        self.timerm_=0
        labelt = self.builder.get_object('lbltiempo1')
        labelt.configure(text="00:00:000")

    def pasojug1(self):
        a = self.mot._getsensorir1()
        if a == 0:
            if self.pasoj1 == False:
                self.nvueltajug1=self.nvueltajug1+1
                labelv = self.builder.get_object('lblvuelta1')
                self.v= str(self.nvueltajug1).zfill(2)
                labelv.configure(text=self.v)
                self.lstinserTiempo()
                #~ self.onTimerstop()
                self.son.startpaso()
                
                self.onTimerclear()
                #~ self.timer.start()
                self.pasoj1 = True
                #self.onTimerClicked() 
        #~ else:
            #~ self.pasoj1=False
    
    def lstinserTiempo(self):
         
        # Populate the listbox
        #lbox.select_clear(tk.END)
        self.lbox = self.builder.get_object('lsttiempos')
        self.text= "v: " + str(self.nvueltajug1) + ">> " + str(self.tmpvueltajug1)
        self.lbox.insert(tk.END, self.text)        
            
    def onTimer( self ):
        #~ print "onTimer"  
        
        self.pasojug1()
        
        self.timerms_+=1
        if self.timerms_ >= 1000:
            self.timerms_=0
            self.pasoj1=False
            self.timers_=self.timers_+1
            if self.timers_ >= 60:
                self.timers_=0
                self.timerm_=self.timerm_+1
                if self.timerm_ >= 60:
                    self.timerm_=0
        #~ self.timerCountLabelVar.set( str(self.timerCounter_) ) 
        labelt = self.builder.get_object('lbltiempo1')
        self.crono=str(self.timerm_).zfill(2)+":"+str(self.timers_).zfill(2)+":"+str(self.timerms_).zfill(2)
        labelt.configure(text=self.crono)
        self.tmpvueltajug1 = self.crono
        self.master.update()
        
          
             
    def procesoMandoXbox(self, isRunningFunc=None ):
        #~ self.joy = xbox.Joystick()
        
        #~ label = self.builder.get_object('lblconectar')
        #~ label.configure(text="Xbox Conectada") 
        #~ label = self.builder.get_object('lblledcon')
        #~ label.configure(background=VERDE) 
        
        self.accOn = False
        while True:
            try:
                if not isRunningFunc() :
                    self.onMyLongProcessUpdate( "Stopped!" )
                    return
            except : pass 

            #~ print self.joy2.rightTrigger()
            
            if self.joy.dpadUp() == True:
                self.onMyLongProcessUpdate("arriba")
                self.mot.dirdelante()
                self.motstop= False
            if self.joy.dpadDown() == True:
                self.onMyLongProcessUpdate("abajo")
                self.mot.diratras()
                self.motstop= False
            if self.joy.A() == True:
                self.mot.parar()
                self.motstop= True
            if self.joy.Y() == True:
                self.chkluzclick() #luz
            if self.joy.Start() == True:
                self.son.startsemaforo()
            if self.joy.Back() == True:
                self.grabavuelta = True
                self.texto=""                 
                self.onMyLongProcessUpdate("Grabando vuelta")
            if self.joy.B() == True:
                self.grabavuelta = False
                datos=(1,1,self.texto + "X00X00X00")
                self.db.grabavuelta(datos)              
                self.onMyLongProcessUpdate("Stop grabado de vuelta OK")  
            
            if self.joy.X() == True:
                self.son.stopsonidos()
                sleep(button_delay)
                nomradio=self.son.radio()
                self.onMyLongProcessUpdate(nomradio)    
            if self.joy.rightBumper() == 1:
                #~ self.son.stopsonidos()
                self.son.claxon()
                sleep(button_delay)
                
            if self.joy.leftBumper() == 1:
                if self.playvuelta == False:
                    dat=(1,1)#aqui ira piloto y coche
                    self.cur=self.db.getfvueltagrabada(dat)
                    a=self.cur[0][0]
                    self.datvuelta=a.split('X')
                    self.playvuelta = True
                    self.cont=0
                    print (self.datvuelta)
                    self.onMyLongProcessUpdate("Vuelta cargada")
                else:
                    self.playvuelta= False
                    self.onMyLongProcessUpdate("Vuelta auto stop")
                            
                sleep(button_delay)
                
            #~ if int(self.joy.leftTrigger ) >1:
                
                          
            if self.playvuelta == True:
                b=len(self.datvuelta)
                if self.cont < b:
                    vel=self.datvuelta[self.cont]
                    if vel <> '':
                        self.mot.motorsetvel(int(vel))
                        self.progresupdate (int(vel))
                    self.cont=self.cont+1
                    if self.cont == b:
                        self.playvuelta == False
                        
                    sleep(button_delay)
                
            
            if self.pilotoAuto == False:
                if self.playvuelta == False:
                    if self.motstop == False:
                        a=(self.joy.rightTrigger() * 100) 
                        self.mot.motorsetvel(int(a))
                        self.progresupdate (int(a))
                        if self.grabavuelta == True:
                            self.texto =self.texto + "X" + str(int(a)).zfill(2)
                            #~ datos=(1,1,self.texto)
                            #~ self.db.grabavuelta(datos,pw)
                            
                        sleep(button_delay)
            #~ self.master.update()
            
        #~ self.joy.close()
             
            
  
    def btnconectarClick(self):
        print ("no implementado wii")
        #~ try: self.xbTask.start()
        #~ except: pass
    
    def btnluzciruitoclick(self):
        self.mot.luzcircuito(1)
        
    def onMyLongProcessUpdate( self, status ) :
        lblcon = self.builder.get_object('lblconectar')
        lblcon.configure(text=str(status)) 
        #self.statusLabelVar.set( str(status) )
        


    def onStopClicked( self ) :
        self.onMyLongProcessUpdate( "desconectado" ) 
        try: self.timer.stop()
        except: pass
        #try: self.timer.stop()
        #except: pass 
    def chkgrabarvuelta(self):
        if self.grabavuelta == False:
            self.grabavuelta = True
        else:
            self.grabavuelta = False
            
    def chkluzclick(self):
        
        self.mot.luzcircuito()
        #self.son.startsemaforo()
        #~ self.son.startefecto1()
        #~ self.joy = xbox.Joystick()
        #~ self.son.stopsonidos()
        #~ self.son.radio()
    
    def btnXboxconect(self):
        #~ self.joy = xbox.Joystick()
        try: self.xbTask.start()
        except: pass
                
        label = self.builder.get_object('lblconectar')
        label.configure(text="Xbox Conectada") 
        label = self.builder.get_object('lblledcon')
        label.configure(background=VERDE) 
    #~ def passbtnXboxconect2(self):
        #~ try: self.xbTask.start()
        #~ except: pass
    
        
    def progresupdate(self, v):
        pgr = self.builder.get_object('pgr1')
        pgr.configure(value=int(v))      
        lblvel = self.builder.get_object('lblvel')
        lblvel.configure(text=str(v)) 
          
    def on_scale1_changed(self, event):
        if self.pilotoAuto == True:
            scale = self.builder.get_object('scale1')
            v=scale.get()
            self.progresupdate(int(v))
            self.mot.motorsetvel(int(v))
    
    def chkpilotoautomatico(self):
        if self.pilotoAuto == True:
            scale = self.builder.get_object('scale1')
            self.progresupdate(0)
            self.mot.motorsetvel(0)
            scale.set(0)
            self.pilotoAuto = False
        else:
            self.pilotoAuto = True
            
    
        
        
        
            




if __name__ == '__main__':
    root = tk.Tk()
  
    app = Myapp(root)
    root.mainloop()

