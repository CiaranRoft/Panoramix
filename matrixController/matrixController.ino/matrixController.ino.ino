/*
 * Programmer : Ciaran Roft 
 * Date : 12/03/2017
 * Description : An arduino to take in command via the serial port and use a user defined library to display commands on an 7 X 7 WS2812B LED matrix
 */
 
#include <Matrix.h>  // USer made library written specifically for Panoramix 7 X 7 LED matrix

#define NUM_LEDS 49 // Defining the number of LEDs
#define MYSIZE 7 // Defining the length of each command
int myInts[MYSIZE]; // Creating an array of ints to store command
int count = 0; // Counter variable to determine when each command is ended

Matrix matrix; // Initializing matrix object

void setup() {
  Serial.begin(9600); // Starting serial communication
}

void loop() {
  //Send data whenb data is recieved
  while(Serial.available() > 0){
    //Read the incomming command and store in the array of commands
    myInts[count] = (Serial.read() - 48); // Minus 48 because '1' ASCII table is 49
    //Serial.print(myInts[count]); // Printing each of the commands to the serial port
    count = count + 1; 

    //Only execute when there is a value for each frequency range(colounm)
    if(count == MYSIZE){
      Serial.print("\n"); 
      matrix.changeSequence(MYSIZE, myInts); // Calling the method to change the LEDs based on commands
      count = 0; // Reset count to 0 for getting the next commands
    }
  }
}
