#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <math.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>

#define PCA9685_MODE1 0x0
#define PCA9685_PRESCALE  0xFE

#define LED0_ON_L  0x6
#define LED0_ON_H  0x7
#define LED0_OFF_L  0x8
#define LED0_OFF_H  0x9

int dID = 0x40;	// This is the default address value of pca9685 
int fd = 0;	// i2c device handle
int Hz = 50;

void my_ctrl_c_handler(int sig){ // can be called asynchronously
	int x;

	printf ("Servo driver Application End\n"); 
	for( x  = 0; x < 8; x++)
		set_PWM(x, 0, 0);
	close(fd);
	exit(0);
}

char read_byte_2c(int addr)
{
	return (char)wiringPiI2CReadReg8(fd, addr) ;
}

void write_byte_2c(int addr, char val)
{
	wiringPiI2CWriteReg8(fd, addr, val) ;
	return;
}

void write_word_2c(int addr, short val)
{
	wiringPiI2CWriteReg8(fd, addr, val) ;
	wiringPiI2CWriteReg8(fd, addr + 1, val >> 8) ;
	return;
}

/*
Why frequency *0.9 ?
issue : https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library/issues/11
*/
void set_PWMFreq(float freq)
{
	float prescaleval, prescale;
	char oldmode, newmode, scale;

	freq *= 0.9;
	prescaleval = 25000000.0;
	prescaleval /= 4095;
	prescaleval /= freq;
	prescaleval -= 1;
	printf("Estimated pre-scale:%f\n", prescaleval);

	prescale = floor(prescaleval + 0.5);
	printf ("Final pre-scale:%f\n ", prescale);
	scale = (char)(int)prescale;
	oldmode = read_byte_2c(PCA9685_MODE1);
	newmode = (oldmode & 0x7F) | 0x10 ;
	write_byte_2c(PCA9685_MODE1, newmode);
	write_byte_2c(PCA9685_PRESCALE, scale);
	write_byte_2c(PCA9685_MODE1, oldmode);
	delay(5);
	write_byte_2c(PCA9685_MODE1, oldmode | 0xa1);
}

void set_PWM(int channel, short on, short off)
{
	on = on & 0xFFFF;
	off = off & 0xFFFF;
	write_word_2c(LED0_ON_L+4*channel,on) ;
	write_word_2c(LED0_ON_L+4*channel + 2,off) ;

}
// PWM Length ����
void set_PWM_Length(int channel, double rate)
{
  float pulse, off;
  int on;  
  pulse = 1000.0 / Hz; //perhaps 20ms
  off = rate * 4095 / pulse;
  on = 0;
  set_PWM(channel, on, (int)off);
}

// angle ���� (SG90�� ��� �뷫... 0��=0.6ms ... 180��=2.5ms)
void set_angle(int channel, double rate)
{
  double val;	
  val = 0.6 + rate * 1.9 / 180.0;
  set_PWM_Length(channel, val);
}

////////////////////////////////////////////////////////////

void Left(int start, int end, float v, float v1)
{
	int x;
	for( x  = start; x < end; x++){
		if(x==0)
			set_angle(x, v);
		else if(x==1)	
			set_angle(x, v1);

	}
}			

////////////////////////////////////////////////////////////
double FixDouble(double a, int n)
{
	return ((int)(a*pow(10.0, n)))/pow(10.0, n);
}

int main(){

int i;
float avg[30];
float avg1[30];
float j,k;
char buf[128];
FILE *fp;

signal(SIGINT, my_ctrl_c_handler);	//Ctrl + C Handler
	if((fd=wiringPiI2CSetup(dID))<0){
		printf("error opening i2c channel\n\r");
		return 0;
	}

	write_byte_2c(PCA9685_MODE1, 0);
	set_PWMFreq(Hz); //50Hz

fp = fopen("6050_1.dat","r");

for(i=0; i<30; i++){
	
	fscanf(fp,"%d %f %f\n",&i,&j,&k);
	
	
	
	avg[i]=FixDouble(j, 1);
	avg1[i]=FixDouble(k, 1);
		
	
	printf("%g %g \n",avg[i],avg1[i]);
	Left(0,1,j,k);
	sleep(1);

}

	fclose(fp);
	close(fd);
	printf ("Servo driver Application End\n"); 
	set_PWM(0, 0, 0);
	return 0;
	
}

//gcc -o av -lwiringPi -lm av.c
