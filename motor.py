#!/usr/bin/env python
import smbus
import time
import math

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
    bus.write_byte_data(address,adr + 1, (val >> 8))
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
    off = rate * 41
    set_PWM(channel, on, int(off))

def five(start, end):
    print("left")
    for x in range(start,end):
        set_PWM_Duty(x,5)
        
def seven(start, end):
    print("middle")
    for x in range(start,end):
        set_PWM_Duty(x,7)

def nine(start, end):
    print("right")
    for x in range(start,end):
        set_PWM_Duty(x,9)


bus = smbus.SMBus(1)
address = 0x40

try:
    bus.write_byte_data(address,PCA9685_MODE1,0)
    set_PWMFreq(50)
    set_PWM(0,0,2048)
except IOError:
    print ("Perhaps there's no i2c device, run i2cdetect -y 1 for device connection!")
    pass

try:
    while True:

            seven(0,3)
            time.sleep(0.7)

        #for x in range(0,10):
            nine(0,1)
            seven(1,2)
            five(2,3)
            time.sleep(3)
        
            nine(0,2)
            nine(2,3)
            time.sleep(3)
    
except KeyboardInterrupt:
    print ("Servo driver Application End")
    set_PWM(0,0,0)
 
