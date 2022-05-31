                    #-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import fire
import math
import imu_code as imu
import math

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26

ENA = 16
ENB = 13

#Pump motor pin
IN5 = 2

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
    imu.MPU_Init()
    time.sleep(0.1)
    imu.calibrate()

    global currentA
    currentA = imu.gyroDelta()[1]

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
    global pwm_ENC
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN5, GPIO.OUT, initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENC = GPIO.PWM(IN5, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
    pwm_ENC.start(0)
  
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

#Pumo
def pump():
    GPIO.output(IN5, GPIO.HIGH)
    pwm_ENC.ChangeDutyCycle(50)

#Stop pump
def noPump():
    GPIO.output(IN5, GPIO.LOW)
    pwm_ENC.ChangeDutyCycle(0)
    
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
	
def getDistance():
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
  return ((ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3)/30.48

#Get current angle
def getCurrA():
  return currentA

#Set current angle
def setCurrA(arg):
  global currentA
  currentA = arg

def calcAngle(v, h):
  angle = 0
  if(v == 0):
    angle = -(h/abs(h)) * 90
  else:
    angle = abs(math.degrees(math.atan(h/v)))
    if(v < 0):
        angle += 90
    if(h > 0):
      angle = -1 * angle
  return angle

#Set angle  
def setAngle(ang):
  if(ang < getCurrA()):
    while(getCurrA() > ang):
      print("CA: " + str(getCurrA()))
      spin_right()
      setCurrA(getCurrA() + imu.gyroDelta()[1])
  elif(ang > getCurrA()):
    while(getCurrA() < ang):
      print("CA: " + str(getCurrA()))
      spin_left()
      setCurrA(getCurrA() + imu.gyroDelta()[1])
  brake()
  time.sleep(0.3)

#Water the surrounding plants
def waterPlants(currPos, mapArr):
  plantArr = []
  for dy in range(-1,2):
    for dx in range(-1,2):
      print(currPos[0])
      print(int(currPos[0])+dy)
      print(mapArr[int(currPos[0])+dy][int(currPos[1])+dx])
      print(int(mapArr[int(currPos[0])+dy][int(currPos[1])+dx]))
      if(int(mapArr[int(currPos[0])+dy][int(currPos[1])+dx]) == 1):
        plantArr.append([int(currPos[0])+dy, int(currPos[1])+dx])
  watered_plants = []
  for plant in plantArr:
    if(not(plant in watered_plants)):
         vertical = int(currPos[0])-plant[0]
         horizontal = plant[1]-int(currPos[1])
         angle = calcAngle(vertical, horizontal)
         print("A:"+str(angle))
         setAngle(angle)
         pump()
         time.sleep(0.2)
         watered_plants.append(plant)
         noPump()
  print(watered_plants)

def auto(umap,upath):
  init()
  fixPath = False
  umap = umap.split("N")
  for i in range(0,len(umap)):
    umap[i] = umap[i].replace("[","").replace("]","")split(",")
  upath = upath.split("N")
  for i in range(0,len(upath)):
    upath[i] = upath[i].replace("[","").replace("]","")split(",")
  
  currentPos = upath[0]
  time.sleep(0.2)

  for i in range(1, len(upath)):
    print("CP:"+str(currentPos[0])+","+str(currentPos[1]))
    vertical = int(currentPos[0])-int(upath[i][0])
    horizontal = int(upath[i][1])-int(currentPos[1])
    magnitude = math.sqrt((vertical**2) + (horizontal**2))
    angle = calcAngle(vertical, horizontal)
    print("V:"+str(vertical))
    print("H:"+str(horizontal))
    print("M:"+str(magnitude))
    print("A:"+str(angle))
    initialD = getDistance()
    print("ID:"+str(initialD))
    print("IA:"+str(getCurrA()))
    setAngle(angle)
    while((initialD-getDistance())<magnitude):
        print("Forward: " + str(getDistance()))
        run()
    currentPos = upath[i]
    time.sleep(0.3)
    waterPlants(currentPos, umap)
    time.sleep(0.3)

  brake()

if __name__ == '__main__':
  fire.Fire(auto)
  
  print("Ended")
  pwm_ENA.stop()
  pwm_ENB.stop()
  pwm_servo.stop()
  GPIO.cleanup() 
