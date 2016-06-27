from gopigo import *
import RPi.GPIO as GPIO
from time import sleep
from time import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def Read():
        try:
                Trig=7
                Echo = 25
                GPIO.setup(Echo,GPIO.IN)
                GPIO.setup(Trig, GPIO.OUT, initial=GPIO.LOW)
                GPIO.output(Trig,GPIO.HIGH)
                sleep(0.00001)
                GPIO.output(Trig,GPIO.LOW)
                start = time()
                while GPIO.input(Echo)==0:
                        continue
                start = time()
                while GPIO.input(Echo)==1:
                        continue
                endtime=time()
                time_passed = endtime-start;
                result = (time_passed*340/2)*100
                return result
        except:
                print 'problem here Time Elapsed :{},Total Result :{}'.format(time_passed,result)
def ReadAverage():
        try:
                val1 = Read()
                val2 = Read()
                val3 = Read()
                return (val1+val2+val3)/3
        except:
                print 'Got it: v1:{},v2:{},v3:{}'.format(val1,val2,val3)
                
def Move(val):
        #val*=10
        #if val>0:
        #        val*=10
        val = val/5
        if val ==0:
                stop()
                return
        if val>255:
                val = 255

        if val<-255:
                val = -255
        #print val
        set_speed(int(abs(val)))
        if val>0:
                fwd()
        elif val<0:
                bwd()
        sleep(0.1)
        
def TestReader():
        for i in range(10):
                print 'Average :===> ',ReadAverage()
                sleep(0.1)
def StopEveryThing():
        stop()
'''
#TestReader()
print ReadAverage()

Move(0)
Move(255)
print ReadAverage()
Move(-255)
print ReadAverage()
stop()
'''
