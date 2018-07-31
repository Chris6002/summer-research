import serial
ser=serial.Serial(port='/dev/ttyTHS2',baudrate=115200)  # open serial port
ser.flushInput()
ser.flushOutput()
import time
record_FPS=10
print("connected to: " + ser.portstr)


while True:  
    command=ser.readline().decode('utf-8').rstrip().split('x')
    ch1=int(command[0])
    ch2=int(command[1])
    ch3=int(command[2])
    ch4=int(command[3])
    print(ch1,end=',')
    print(ch2,end=',')
    print(ch3,end=',')
    print(ch4)
    #for c in ser.readline():
    #    line=[]
    #    
    #    line.append()
    #    print(chr(c),end='')
ser.close()
