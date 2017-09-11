    #include "Matrix.h" //include the declaration for matrix class
    #include "WS2812.h" // Include the library for the LEDs
 
    const byte LED_PIN = 6; // Defining the data pin connected to the LEDs
    const byte NUM_LEDS = 49; // Defing the number of LEDs

    WS2812 LED(NUM_LEDS); // Initalizing a WS2812 object  7 
    cRGB value; // Strut to store the RGB values for the LEDs

    //Constructor setup the LED, make pin 6 an OUTPUT
    Matrix::Matrix(){
        LED.setOutput(LED_PIN);
    }
 
    //<<destructor>>
    Matrix::~Matrix(){/*nothing to destruct*/}
 
    //Method to represent the commands passed in to it on the LEd matrix
    void Matrix::changeSequence(int matrix_size, int* myArray){
        // Looping through each coloum (7)     
        for(int coloum = 0; coloum < matrix_size; coloum++){
            //Looping the number accociated with that coloum, to turn on that many lights
            for(int row = 0; row < matrix_size; row++){
                //Turning on all of the blue lights
                if(row < myArray[coloum]){
                    turnOnLeds(coloum, row);
                }
                //Turning off every other light (Setting to Black)
                else{
                    turnOffLeds(coloum, row);
                }
            }       
        }
        LED.sync(); // Sends the required data to the LEDs to turn on
    }
 
    //Method to turn off the LEDs that shouldnot be on
    void Matrix::turnOnLeds(int coloum, int row){
            cRGB color = colorChooser(coloum); // Geting the color of the row that LED is on
	   
	     // If statement to handle the first colounm and the all the rest
            if(coloum == 0){
                LED.set_crgb_at(row, color); // Setting LED to the appropriate color
            }
        
            //For Lighting the other
            else{
                LED.set_crgb_at(row+7*coloum, color); // Setting LED to the appropriate color
            }   
    }
 
    //Method to tell what color each colounm should be
    cRGB Matrix::colorChooser(int coloum){
 	//Sub Bas 
        if(coloum == 0){
            value.b = 0; value.g = 255; value.r = 0;
        }
	// Bass
        else if(coloum == 1){
            value.b = 0; value.g = 255; value.r = 255;
        } 
	// Low Midrange   
        else if(coloum == 2){
            value.b = 0; value.g = 128; value.r = 255;
        }
	//Mid Range
        else if(coloum == 3){
            value.b = 0; value.g = 0; value.r = 255;
        }
	//Upper Midrange
        else if(coloum == 4){
            value.b = 204; value.g = 0; value.r = 204;
        }
	// Presence
        else if(coloum == 5){
            value.b = 204; value.g = 0; value.r = 102;
        }
	//Brilliance
        else if(coloum == 6){
            value.b = 255; value.g = 0; value.r = 0;
        }  
        return value; // Returning the colors for each frequency range
    }
    // Method to turn off the LEDs that should not be turned on
    void Matrix::turnOffLeds(int coloum, int row){
        //For turning off the first coloum
        if(coloum ==0){
            value.b = 0; value.g = 0; value.r = 0;
            LED.set_crgb_at(row,value);
            //leds[row] = CRGB::Black;
        }
        //For turning off the other
        else{
            value.b = 0; value.g = 0; value.r = 0;
            LED.set_crgb_at(row+7*coloum,value);
          //leds[row+7*coloum] = CRGB::Black;
        }
    }
