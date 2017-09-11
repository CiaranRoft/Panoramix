'''
Programmer: Ciaran Roft
Date: 21/02/2017
Description: Program that takes in a data set in the form of a numpy array, along with the sample rate of that data set
             By finding the average of N data points in the data set, it then generates Arduino usable commands designed
             to control an LED matrix
'''

# A method to generate commands for an Arduino based on a list of commands and the largest average in that list
def make_command(averages, largest):
    commands = [] # A list to hold the commands
    # Loop to loop through the list of averages and sorts them based on how close they are to the MAX
    for avg in averages:
        if(int(avg) < (largest / 7)):
            commands.append('1111111')
        elif(avg < (largest / 7)*2):
            commands.append('2222222')
        elif(avg < (largest / 7)*3):
            commands.append('3333333')
        elif(avg < (largest / 7)*4):
            commands.append('4444444')
        elif(avg < (largest / 7)*5):
            commands.append('5555555')
        elif(avg < (largest / 7)*6):
            commands.append('6666666')
        elif(avg < largest):
            commands.append('7777777')
        else:
            commands.append('0000000')
            
    return commands # Returning commands

# Method to return the largest average in a list
def largest_avg(averages):
    largest = 0 # Initializing
    # Looping through the list of averages
    for avg in averages:
        # If a new number is larger than the largest, make that the new larges
        if(avg > largest):
            largest = avg
    return largest # Retunr the largest average

# Method to that takes arguments of numpy array of data and the sample rate of the data
# Will retun a numpy array of commands to send Arduino
def build_commands_avg(data, rate):
    N = rate/20 # The number of numbers in each average
    print N
    lines = [] # List to store N numbers to find the average
    all_avgs = [] # List to store all of the averages of the data set
    
    import numpy as np # importing numpy
    # For loop to loop through the number of data point in the data set passed into it
    for line in np.nditer(data):
        number = abs(int(line)) #Taking the absolute value of each data point
        lines.append(number) # Appending each data point to the list
        # If statement to check if lines list has N elements
        if len(lines) > N:
            avg = sum(lines)/N # Finding the average of the lines list
            all_avgs.append(avg) # Appending that average to the all_avgs list
            lines = [] # Emptying the lines array, to gather another N elements       

    big_avg = largest_avg(all_avgs) # Finding the largest average in the all_avgs list
    commands_list = make_command(all_avgs, big_avg) # Sending the all averages list and the largest average to a method to generate commands for the Arduino
    return commands_list # Returning the list of commands

# Methodto build commands bassed of randomly choosen data and sampel rate of data
def build_commands_rand(data, rate):
    N = rate/20 # The celling for the random number
    print N
    lines = [] # List to store all the amplitude samples
    all_samples = [] # List to store all of the randomly choosen samples
    import numpy as np
    from random import randint
    # Loop to loop through all of the data
    for line in np.nditer(data):
        number = abs(int(line)) # getting the absolute value of amplitude
        lines.append(number) # appending each amplitude value to list

        # If statement to break data up into sample_rate/20 chunks
        if len(lines) > N:
            rand_int = randint(0, N) # Generating random number
            sample = lines[rand_int] # Storeing randomly selected amplitude values 
            all_samples.append(sample) # Appending randomly choosen value to a list
            lines = [] # emptying list
            
    big_sample = largest_avg(all_samples) # Finding the largest amplitude value in list
    commands_list = make_command(all_samples, big_sample) # Sending all the randomly chossen samples and the biggest sample to method to determind appropriate commands
    return commands_list # Returning commands list so that transfer method can send commands to Arduino

