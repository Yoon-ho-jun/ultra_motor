import smbus
import time
import math

power_mgmt_1=0x6b
power_mgmt_2=0x6c

AFS_SEL = -1
FS_SEL = -1

def read_byte(adr):
    return bus.reaed_byte_data(address,adr)

def read_word(adr):
    high=bus.read_byte_data(address,adr)
    low =bus.read_byte_data(address,adr+1)
    val=(high<<8)+low
    return val

def read_signed_16_2c(adr):
    val=read_word(adr)
    if(val>=0x8000):
        return -((65535-val)+1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y,dist(x,z))
    return -math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z,dist(x,y))
    return -math.degrees(radians)

def adjust_gyro(val):
    ret=val*1.0

    if(0==val):
        return 0.0
    
    if(0 == FS_SEL):
        return val/131.0

    if(1 == FS_SEL):
        return val/65.5

    if(2 == FS_SEL):
        return val/32.8

    if(3 == FS_SEL):
        return val/16.4

    else:
        print ("Error : Invalid FS_SEK [", FS_SEL, "]")
    return ret

def adjust_accel(val):
    ret=val*1.0

    if(0==val):
        return 0.0
    
    if(0 == AFS_SEL):
        return val/16384.0

    if(1 == AFS_SEL):
        return val/8192.0

    if(2 == AFS_SEL):
        return val/4096.0

    if(3 == AFS_SEL):
        return val/2048.0

    else:
        print ("Error : Invalid FS_SEK [", AFS_SEL, "]")
    return ret

bus = smbus.SMBus(1)
address=0x68

bus.write_byte_data(address,power_mgmt_1,0)
print("gyro data")
print("---------")

AFS_SEL = read_signed_16_2c(0x1C)
FS_SEL = read_signed_16_2c(0x1B)
print ("AFS_SEL:",AFS_SEL,"FS_SEL",FS_SEL)

temper = read_signed_16_2c(0x41);

if(temper):
    temper = temper/340.0+36.53;

print("Temp : ",temper)

f=open('6050_1.dat','w')
index=0

try:
    while True:
        gyro_xout = adjust_gyro(read_signed_16_2c(0x43))
        gyro_yout = adjust_gyro(read_signed_16_2c(0x45))
        gyro_zout = adjust_gyro(read_signed_16_2c(0x47))

        accel_xout = adjust_accel(read_signed_16_2c(0x3b))
        accel_yout = adjust_accel(read_signed_16_2c(0x3d))
        accel_zout = adjust_accel(read_signed_16_2c(0x3f))

        x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout)
        y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout)
        z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout)

        print(index,"Accel:",accel_xout,accel_yout,accel_zout,"Rotate:",x_rotate,y_rotate,z_rotate);

        data="{} {} {} {} {} {} {}\n".format(index,accel_xout,accel_yout,accel_zout,x_rotate,y_rotate,z_rotate)
        f.write(data)
        time.sleep(0.05)
        index += 1
        
except KeyboardInterrupt:
    print ("Now Exit")
    f.close()
