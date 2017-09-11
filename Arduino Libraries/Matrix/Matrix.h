    #ifndef Matrix_H
    #define Matrix_H

    #include <Arduino.h> // Including the standard arduino header file
    #include <WS2812.h> // Including he library for the LEDs

    // Defining a Matrix class 
    class Matrix{
    public:
	    Matrix(); // Constructor
	    ~Matrix(); // Deconstructor
	    void changeSequence(int matrix_size, int* myArray); // Method to change the LEDs based on the commands passed in
	    void turnOnLeds(int coloum, int row); // Method to turn of the specified LEDs
	    cRGB colorChooser(int coloum); // Method that sets the colour of the LEDs
	    void turnOffLeds(int coloum, int row); // Method to turn off the any LEDs that should not be on
    };

    #endif
