                    #-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Definition of RGB module pin
LED_R = 22
LED_G = 27
LED_B = 24

#Definition of servo pin
ServoPin = 23
currCycle = 0

#Definition of ultrasonic module pin
EchoPin = 0
TrigPin = 1                    

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

#Drive keys
drive_keys = ["w", "s", "a", "d", "q", "e"]

def init():
    #RGB pins
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)

    GPIO.output(LED_R, GPIO.HIGH)
    GPIO.output(LED_G, GPIO.HIGH)
    GPIO.output(LED_B, GPIO.LOW)
    print("Initializing...")
  
    #Motor pins
    global pwm_ENA
    global pwm_ENB
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
  
    #Servo pin
    global pwm_servo
    GPIO.setup(ServoPin, GPIO.OUT)
    pwm_servo = GPIO.PWM(ServoPin, 50)
    pwm_servo.start(0)

    #Ultrasonic pins
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)

    #Key variable
    global key
  

#advance
def run():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#back
def back():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#turn left
def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#turn right
def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#turn left in place
def spin_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#turn right in place
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)

#Servo control
def turnTo(cycle):
  global currCycle
  if(not(cycle == currCycle)):
    pwm_servo.ChangeDutyCycle(cycle)
    GPIO.output(ServoPin, GPIO.HIGH)
    currCycle = cycle
    
#Ultrasonic function
def Distance():
  GPIO.output(TrigPin,GPIO.LOW)
  time.sleep(0.000002)
  GPIO.output(TrigPin,GPIO.HIGH)
  time.sleep(0.000015)
  GPIO.output(TrigPin,GPIO.LOW)

  t3 = time.time()
  while not GPIO.input(EchoPin):
      t4 = time.time()
      if (t4 - t3) > 0.03 :
          return -1
  t1 = time.time()
  while GPIO.input(EchoPin):
    t5 = time.time()
    if(t5 - t1) > 0.03 :
      return -1
        
  t2 = time.time()
  time.sleep(0.01)
  return ((t2 - t1)* 340 / 2) * 100
	
def Distance_test():
  num = 0
  ultrasonic = []
  while num < 5:
    distance = Distance()
    while int(distance) == -1 :
      distance = Distance()
    while (int(distance) >= 500 or int(distance) == 0) :
      distance = Distance()
    ultrasonic.append(distance)
    num = num + 1
    time.sleep(0.01)
  distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3
  print ("Average Distance: %f"%(distance) )

def press(key):
    #Motor control
    print(key)
    if(key == "w"):
      run()
    elif(key == "s"):
      back()
    elif(key == "a"):
      left()
    elif(key == "d"):
      right()
    elif(key == "q"):
      spin_left()
    elif(key == "e"):
      spin_right()
    

    #Servo control
    if(key == "z"):
      pwm_servo.turnTo(2)
    elif(key == "x"):
      pwm_servo.turnTo(7)
    elif(key == "c"):
      pwm_servo.turnTo(12)

    
def release(key):
  if(key in drive_keys):
    brake()
  #Ultrasonic
  Distance_test()

if __name__ == '__main__':
  init()
  #print("Complete")    
  listen_keyboard(
    on_press=press,
    on_release=release,
  )
  print("Ended")
  pwm_ENA.stop()
  pwm_ENB.stop()
  pwm_servo.stop()
  GPIO.cleanup() 