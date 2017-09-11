import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600) # Opeing serial port
# Method to send commands to the Arduino at a certain rate
def transfer(commands):
    # Loop through all list of commands
    for command in commands:
        ser.write(command)# Writting the commands to the Arduino
        time.sleep(0.05)# Waiting for set time to stay acurate to sample rate
    
