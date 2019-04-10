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
    off = rate * 4095.0/100.0
    set_PWM(channel, on, int(off))

def a(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,3)

def b(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,3.5)

def c(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,4)

def d(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,4.5)

def e(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,5)

def f(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,5.5)

def g(start, end):  #left
        print("x");
        set_PWM_Duty(0,6)

def h(start, end):  #mid
        print("y");
        set_PWM_Duty(0,6.5)


def i(start, end):  #right
        print("z");
        set_PWM_Duty(0,7)

def j(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,7.5)


def k(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,8)

def l(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,8.5)

def m(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,9)

def n(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,9.5)

def o(start, end):
    for x in range(start,end):
        set_PWM_Duty(x,10)


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
        
            a(0,1)
            time.sleep(1)
            b(0,1)
            time.sleep(1)
            c(0,1)
            time.sleep(1)
            d(0,1)
            time.sleep(1)
            e(0,1)
            time.sleep(1)
            f(0,1)
            time.sleep(1)
            g(0,1)
            time.sleep(1)
            h(0,1)
            time.sleep(1)
            i(0,1)
            time.sleep(1)
            j(0,1)
            time.sleep(1)
            k(0,1)
            time.sleep(1)
            l(0,1)
            time.sleep(1)
            m(0,1)
            time.sleep(1)
            n(0,1)
            time.sleep(1)
            o(0,1)
            time.sleep(1)
            
    
except KeyboardInterrupt:
    print ("Servo driver Application End")
    set_PWM(0,0,0)
 
