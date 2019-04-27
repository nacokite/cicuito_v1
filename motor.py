import RPi.GPIO as GPIO



class Motor:
    PINA1= 02
    PINA2= 03
    PINVEL = 04
    PINLUZ = 16
    PINIR  = 17
    pwm = ""
    stluz = 0
    
    
    def __init__(self):
        self._sensorir_ = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)


        GPIO.setup(self.PINA1, GPIO.OUT) 
        GPIO.setup(self.PINA2, GPIO.OUT)
        GPIO.setup(self.PINVEL, GPIO.OUT)
        GPIO.setup(self.PINLUZ,GPIO.OUT)
        GPIO.setup(self.PINIR, GPIO.IN, pull_up_down=GPIO.PUD_UP) #sensor ir
        

        self.pwm=GPIO.PWM(self.PINVEL,500)
        self.pwm.start(0)
        
    def _getsensorir1(self):
        self._sensorir1_=GPIO.input(self.PINIR) 
        return self._sensorir1_
        
    def luzcircuito(self ):

        if self.stluz == 0:
          GPIO.output(self.PINLUZ,True)
          self.stluz = 1
        else:
          GPIO.output(self.PINLUZ,False)
          self.stluz = 0
             
       
    def motorsetvel (self, velocidad):
        self.pwm.ChangeDutyCycle(velocidad)
        GPIO.output(self.PINVEL, True)
   
    def dirdelante(self):
        
        GPIO.output(self.PINA1, True)
        GPIO.output(self.PINA2, False)
        
    def diratras(self):
       
        GPIO.output(self.PINA1, False)
        GPIO.output(self.PINA2, True)
       
    def parar(self):
        self.pwm.ChangeDutyCycle(0)
        GPIO.output(self.PINVEL, False)
        
        
