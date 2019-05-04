#!/usr/bin/env python
import smbus
import time
import math
import sys
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER=17
GPIO_ECHO=27


GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
GPIO.setup(GPIO_ECHO,GPIO.IN)

PCA9685_MODE1=0x0
PCA9685_PRESCALE=0xFE

LED0_ON_L=0x6
LED0_ON_H=0x7
LED0_OFF_L=0x8
LED0_OFF_H=0x9

def read_byte(adr):
    return bus.read_byte_data(address,adr)
def write_byte_2c(adr,val):
    return bus.write_byte_data(address,adr,val)
def write_word_2c(adr,val):
    bus.write_byte_data(address,adr,val)
    bus.write_byte_data(address,adr+1, (val >> 8))
def set_PWMFreq(freq):
    freq *=0.9
    prescaleval = 25000000.0
    prescaleval /= 4095
    prescaleval /= freq
    prescaleval -= 1;

    prescale = math.floor(prescaleval + 0.5)

    oldmode = read_byte(PCA9685_MODE1)
    newmode = (oldmode&0x7F) | 0x10
    write_byte_2c(PCA9685_MODE1,newmode)
    write_byte_2c(PCA9685_PRESCALE,int(prescale))
    time.sleep(0.005)
    write_byte_2c(PCA9685_MODE1,oldmode | 0xa1)
def set_PWM(channel,on,off):
    on = on & 0xFFFF
    off = off & 0xFFFF
    write_word_2c(LED0_ON_L+4*channel,on)
    write_word_2c(LED0_ON_L+4*channel+2,off)
def set_PWM_Duty(channel,rate):
    on = 0
    off = rate*41
    set_PWM(channel, on, int(off))

def left(start, end):
    print("left 8.5");  '4 motor op'  #motor 1 left
    for x in range(start,end):
        set_PWM_Duty(x,8.5)

def left_l(start, end):
    print("left 8");  '4 motor op'
    for x in range(start,end):
        set_PWM_Duty(x,8.0)

def left_ll(start, end):
    print("left 7.5");  '4 motor op'
    for x in range(start,end):
        set_PWM_Duty(x,7.5)

def mid(start, end):
    print("mid 7");  
    for x in range(start,end):
        set_PWM_Duty(x,7.0)

def right_rr(start, end):
    print("right 6.5");
    for x in range(start,end):
        set_PWM_Duty(x,6.5)

def right_r(start, end):
    print("right 6.0");
    for x in range(start,end):
        set_PWM_Duty(x,6.0)

def right(start, end):
    print("right 5.5");
    for x in range(start,end):
        set_PWM_Duty(x,5.5)

def left_curve(start, end):   
    print("left_curve");
    for x in range(start,end):
        set_PWM_Duty(x,2.5)

def right_curve(start, end):
    print("right_curve");
    for x in range(start,end):
        set_PWM_Duty(x,11.0)

def up_left(start, end):
    print("up_left");
    for x in range(start,end):
        set_PWM_Duty(x,11.0)

def up_right(start, end):
    print("up_right");
    for x in range(start,end):
        set_PWM_Duty(x,3.0)


def move(dir):

    if(dir==1):

        mid(0,8)
        time.sleep(0.05)
        
        left(0,1)
        left(2,3)
        right(4,5)
        left(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        left_l(0,1)
        left_l(2,3)
        right_r(4,5)
        left_l(6,7)
        right(1,2)
        left(3,4)
        right(5,6)
        mid(7,8)
        time.sleep(0.05)

        left_l(0,1)
        left_l(2,3)
        right_r(4,5)
        left_l(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        mid(0,8)
        time.sleep(0.05)

        right_r(0,1)
        right_r(2,3)
        left_l(4,5)
        right_r(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        right_rr(0,1)
        right_rr(2,3)
        left_ll(4,5)
        right_rr(6,7)
        right(1,2)
        left(3,4)
        right(5,6)
        mid(7,8)
        time.sleep(0.05)

        right(0,1)
        right(2,3)
        left(4,5)
        right(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        right_r(0,1)
        right_r(2,3)
        left_l(4,5)
        right_r(6,7)
        right(1,2)
        left(3,4)
        right(5,6)
        mid(7,8)
        time.sleep(0.05)

        right_rr(0,1)
        right_rr(2,3)
        left_ll(4,5)
        right_rr(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        mid(0,8)
        time.sleep(0.05)

        left_ll(0,1)
        left_ll(2,3)
        right_rr(4,5)
        left_ll(6,7)
        left(1,2)
        right(3,4)
        left(5,6)
        right(7,8)
        time.sleep(0.05)

        left_l(0,1)
        left_l(2,3)
        right_r(4,5)
        left_l(6,7)
        right(1,2)
        left(3,4)
        right(5,6)
        mid(7,8)
        time.sleep(0.05)

    elif(dir==2):           #left_curve turn_right 1

        mid(0,7)
        time.sleep(0.05)

        mid(7,8)
        left_curve(8,9)
        time.sleep(0.05)
        left_curve(0,1)
        mid(1,2)
        left_curve(2,3)
        mid(3,4)
        left_curve(4,5)
        mid(5,6)
        left_curve(6,7)
        
        time.sleep(2)

    elif(dir==3):            #turn_right 2

        right_curve(6,7)   # head
        mid(4,5)
        time.sleep(0.05)
        for i in range (0,6):
            mid(i,i+1)
        mid(7,9)
        time.sleep(5)

    elif(dir==4):           #right_curve turn_left 1

        mid(0,7)
        time.sleep(0.05)

        right_curve(0,1)
        mid(1,2)
        right_curve(2,3)
        mid(3,4)
        right_curve(4,5)
        mid(5,6)
        right_curve(6,7)
        mid(7,8)
        right_curve(8,9)
        time.sleep(2)

    elif(dir==5):            #left 2

        left_curve(6,7)  #head
        mid(4,5)
        time.sleep(0.05)
        for i in range (0,6):
            mid(i,i+1)

        mid(7,9)
        time.sleep(5)

    elif(dir==6):            #up and cam
        mid(0,9)
        time.sleep(0.5)
        
        right(5,6)
        os.system('raspistill -t 1 -o 1.jpg')
        time.sleep(0.5)
        right_rr(6,7)
        os.system('raspistill -t 1 -o 2.jpg')
        time.sleep(0.5)
        right_r(6,7)
        os.system('raspistill -t 1 -o 3.jpg')
        time.sleep(0.5)
        mid(6,7)
        os.system('raspistill -t 1 -o 4.jpg')
        time.sleep(0.5)
        left_l(6,7)
        os.system('raspistill -t 1 -o 5.jpg')
        time.sleep(0.5)
        left_ll(6,7)
        os.system('raspistill -t 1 -o 6.jpg')
        time.sleep(0.5)
        mid(6,7)
        
        os.system("echo 'image' | ssmtp -s -a '/ultra_motor/4.jpg' -- 'a01043327120@gmail.com'")
        
    elif(dir==7):

        mid(0,9)
        time.sleep(0.05)
        
        
        
        
bus = smbus.SMBus(1)
address = 0x40

try:
    bus.write_byte_data(address,PCA9685_MODE1,0)
    set_PWMFreq(50)
    set_PWM(0,0,2048)
except IOError:
    print ("Perhaps there's no i2c device, run i2cdetect -y 1 for device connection!")
    pass

start_x=0
start_y=0

try:
    while True:
        move(6)
        move(7)
        '''
        end_x=input('x 좌표를 입력하시오 :')
        end_y=input('y 좌표를 입력하시오 :')
        
         
        
        if(start_x==start_y and end_x==end_y):

            stop=0
            start=0
            GPIO.output(GPIO_TRIGGER,False)
            time.sleep(2)

            GPIO.output(GPIO_TRIGGER,True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER,False)

            while GPIO.input(GPIO_ECHO)==0:
                start = time.time()

            while GPIO.input(GPIO_ECHO)==1:
                stop=time.time()
            
            elasped = stop-start

            if(stop and start):
            
                distance = (elasped * 34000.0)/2
                print("Distance : %.1f cm" % distance)

                if(distance < 30):
                    move(2) # change deg

                else:
                    #left 45 deg
                    move(1) #go_straight
                    if(light < 10):
                        move(7) #stop
                        #turn left 45 deg
                        start_x=end_x
                        start_y=end_y
        
        elif(start_x != end_x and start_y = end_y):
            move(1) #go_straight
            if(light < 10):
                move(7) #stop
                #turn left 180 deg
                start_x=end_x
                start_y=end_y
                

        elif(start_x != end_x and start_y != end_y):
            #right 45 deg
            move(1) #go_straight
                if(light < 10):
                move(7) #stop
                #turn right 45 deg
                start_x=end_x
                start_y=end_y

        elif(start_x == end_x and start_y != end_y):
            if(start_x == start_y):
                #turn left 90 deg
                move(1) #go_straight
                    if(light < 10):
                    move(7) #stop
                    #turn right 90 deg
                    start_x=end_x
                    start_y=end_y

            elif(start_x == start_y):
                #turn right 90 deg
                move(1) #go_straight
                    if(light < 10):
                    move(7) #stop
                    #turn left 90 deg
                    start_x=end_x
                    start_y=end_y
             '''   
            
except KeyboardInterrupt:
    
    print ("Servo driver Application End")
    set_PWM(0,0,0)
    GPIO.cleanup()

GPIO.cleanup()
 
