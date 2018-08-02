import serial
ser=serial.Serial(port='/dev/ttyTHS2',baudrate=115200)  # open serial port
ser.flushInput()
ser.flushOutput()
import time
record_FPS=10
print("connected to: " + ser.portstr)
import maestro
servo = maestro.Controller('/dev/ttyACM0')
servo.setRange(0,1000*4,2000*4)
servo.setSpeed(0,35)

servo.setRange(1,1000*4,2500*4)


while True:  
    command=ser.readline().decode('utf-8').rstrip().split('x')
    ch1=int(command[0])
    ch2=int(command[1])
    ch3=int(command[2])
    ch4=int(command[3])
    print(ch1,end=',')
    print(ch2,end=',')
    servo.setTarget(0,ch1*4)
    servo.setTarget(1,ch2*4)  #set servo to move to center position
    print(servo.getPosition(0),end='\n') #get the current position of servo 1
    print(servo.getPosition(1))
    #for c in ser.readline():
    #    line=[]
    #    
    #    line.append()
    #    print(chr(c),end='')
ser.close()
servo.close()
