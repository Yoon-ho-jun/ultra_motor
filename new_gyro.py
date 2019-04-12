import smbus
import math
import time

power_mgmt_1=0x6b
power_mgmt_2=0x6c

def read_byte(addr,adr):
    return bus.read_byte_data(addr, adr)

def read_word(addr,adr):
    high = bus.read_byte_data(addr,adr)
    low=bus.read_byte_data(addr,adr+1)
    val=(high<<8)+low
    return val

def read_signed_16_2c(addr,adr):
     val = read_word(addr,adr)
     if (val >= 8000):
      return -((65535-val)+1)

     else:
       return val


def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y,dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(z,dist(x,y))
    return math.degrees(radians)


bus = smbus.SMBus(1)
address=0x68

bus.write_byte_data(address,power_mgmt_1,0)
bus.write_byte_data(address+1,power_mgmt_1,0)

f=open('6050_2.dat','w')
index=0
 
try:
   while True:
        gyro_xout = read_signed_16_2c(address,0x43)
        gyro_yout = read_signed_16_2c(address,0x45)
        gyro_zout = read_signed_16_2c(address,0x47)

        accel_xout = read_signed_16_2c(address,0x3b)
        accel_yout = read_signed_16_2c(address,0x3d)
        accel_zout = read_signed_16_2c(address,0x3f)

        gyro_xout1 = read_signed_16_2c(address+1,0x43)
        gyro_yout1 = read_signed_16_2c(address+1,0x45)
        gyro_zout1 = read_signed_16_2c(address+1,0x47)

        accel_xout1 = read_signed_16_2c(address+1,0x3b)
        accel_yout1 = read_signed_16_2c(address+1,0x3d)
        accel_zout1 = read_signed_16_2c(address+1,0x3f)

        x_rotate = get_x_rotation(accel_xout, accel_yout, accel_zout)+90
        y_rotate = get_y_rotation(accel_xout, accel_yout, accel_zout)
        z_rotate = get_z_rotation(accel_xout, accel_yout, accel_zout)

        x_rotate1 = get_x_rotation(accel_xout1, accel_yout1, accel_zout1)+90
        y_rotate1 = get_y_rotation(accel_xout1, accel_yout1, accel_zout1)
        z_rotate1 = get_z_rotation(accel_xout1, accel_yout1, accel_zout1)

    #print(index,"Accel:",accel_xout,accel_yout,accel_zout,"Rotate:",x_rotate,y_rotate,z_rotate);

    #data="{} {} {} {} {} {} {}\n".format(index,accel_xout,accel_yout,accel_zout,x_rotate,y_rotate,z_rotate)
       

        print(index,"X:",x_rotate);
        print(index,"X1:",x_rotate1);
        print("-----------------------")
        
        data="{} {} {}\n".format(index,x_rotate,x_rotate1)
        
        f.write(data)
        time.sleep(0.03)
        index += 1
        
except KeyboardInterrupt:
    print ("Now Exit")
    f.close()
