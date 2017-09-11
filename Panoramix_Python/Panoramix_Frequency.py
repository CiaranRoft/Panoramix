import numpy as np
# Gloal double variables to hold the maximum amplitude in a given frequency
largest_sub = 0.0
largest_bass= 0.0
largest_low = 0.0
largest_mid = 0.0
largest_up = 0.0
largest_pre = 0.0
largest_brill = 0.0

# Method to split the freq
def split_freq(data, time_slice):
    difference = float(format(((time_slice[1] - time_slice[0])*3),'.6f')) # calculating the amount of time to delay
    
    
    # Initializing the numpy arrays for each frequency range
    all_sub_bass = np.zeros((3, 363)) # Sub Bass 20 - 80Hz
    all_bass = np.zeros((4, 363)) # Bass 80 - 250Hz
    all_low_midrange = np.zeros((6, 363)) # Low Midrange 250 - 500Hz
    all_midrange = np.zeros((35, 363)) # Midrange 500 - 2000Hz
    all_upper_midrange = np.zeros((46, 363))# Upper Midrange 2 - 4kHz
    all_presence = np.zeros((47, 363)) # Presence 4 - 6kHz
    all_brilliance = np.zeros((372, 363))# Brilliance 6 - 20Hz

    '''
    Looping through every frequency range and seperating out each range in to its own numpy array.
    Multiple frequency ranges given to by Specgram fit into the the 7 real frequency bands.
    '''
    for number in range(0, 513):
        for x in range(0, len(data[0])):
            if(number < 3):
                all_sub_bass[number][x] = data[number][x] # Sub Bass
            elif(number < 7):
                all_bass[((number+1) %4)][x] = data[number][x] # Bass
            elif(number < 13):
                all_low_midrange[number - 7][x] = data[number][x] # Lower Midrange
            elif(number < 48):
                all_midrange[number - 13][x] = data[number][x] # Midrange
            elif(number < 94):
                all_upper_midrange[number - 48][x] = data[number][x] # Upper Midrange
            elif(number < 141):
                all_presence[number - 94][x] = data[number][x] # Presence
            elif(number < 513):
                all_brilliance[number - 141][x] = data[number][x] # Brilliance

    # Using the global variable for the largest amplitude in each frequency band
    global largest_sub, largest_bass, largest_low, largest_mid, largest_up, largest_pre, largest_brill
    
    # Storing the largest amplitude for each frequency band
    largest_sub = (find_largest(all_sub_bass) / 3)
    largest_bass = (find_largest(all_bass) / 2)
    largest_low = find_largest(all_low_midrange)
    largest_mid = find_largest(all_midrange)
    largest_up = find_largest(all_upper_midrange)
    largest_pre = find_largest(all_presence)
    largest_brill = find_largest(all_brilliance)
    
    '''  
    Defining a new array in the shape that suit the waiting time defined as difference.
    it takes samples in groups of three for how every many frequency ranges are being used
    '''
    time_sub_bass = np.zeros((121, 9))
    time_bass = np.zeros((121, 12))
    time_low_midrange = np.zeros((121, 18))
    time_midrange = np.zeros((121, 105))
    time_upper_midrange = np.zeros((121, 138))
    time_presence = np.zeros((121, 141))
    time_brilliance = np.zeros((121, 1116))

    #Loop to loop through each frequency range and store amplitude in groups of the for each specgram frequency range
    for i in range(3, 366, 3):
        time_sub_bass[(i /3) - 1] = all_sub_bass[:,(i-3):i].reshape(1,9)
        time_bass [(i /3) - 1] = all_bass[:,(i-3):i].reshape(1,12)
        time_low_midrange [(i /3) - 1] = all_low_midrange[:,(i-3):i].reshape(1,18)
        time_midrange [(i /3) - 1] = all_midrange[:,(i-3):i].reshape(1,105)
        time_upper_midrange [(i /3) - 1] = all_upper_midrange[:,(i-3):i].reshape(1,138)
        time_presence [(i /3) - 1] = all_presence[:,(i-3):i].reshape(1,141)
        time_brilliance [(i /3) - 1] = all_brilliance[:,(i-3):i].reshape(1,1116)
 
    # Sending all frequency range data to a method that chosses a random amplitude from from each row of frequency data array
    sub_bass_samples = take_sample(time_sub_bass)
    bass_samples = take_sample(time_bass)
    low_midrange_sampels = take_sample(time_low_midrange)
    midrange_samples=(time_midrange)
    upper_midrange_samples = take_sample(time_upper_midrange)
    presence_samples = take_sample(time_presence)
    brilliance_samples = take_sample(time_brilliance)

    # Command used to generate a command that the Arduino can understand based on the randomly chossen amplitude data
    commands = generate_commands(sub_bass_samples, bass_samples, low_midrange_sampels, midrange_samples, upper_midrange_samples, presence_samples, brilliance_samples)

    #Returning commands and time difference to Panoramix to use in transfer method
    return commands, difference

# Method to take in randomly chossen frequency data and generate a list of commands that the Arduino can understand
def generate_commands(sub_bass, bass, low_mid, mid, up_mid, pre, brill):
    # Initializing list for commands for each frequency range
    sub_commands = []
    bass_commands = []
    low_mid_commands = []
    mid_commands = []
    up_mid_commands = []
    pre_commands = []
    brill_commands = []

    '''
    Loop to loop through all the samples for each frequency range, and calls the check method to compares the largest amplitude value
    against each randomly chossen amplitude value and stores all the commands for each frequency range
    '''
    for i in range(0, len(sub_bass)):
        sub_commands.append(check(largest_sub,sub_bass[i]))
        bass_commands.append(check(largest_bass,bass[i]))
        low_mid_commands.append(check(largest_low,sub_bass[i]))
        mid_commands.append(check(largest_mid,bass[i]))
        up_mid_commands.append(check(largest_up,sub_bass[i]))
        pre_commands.append(check(largest_pre,bass[i]))
        brill_commands.append(check(largest_brill,sub_bass[i]))
        
    commands = [] # Initializing a list for the finished commands
    command = '' # Initializing a sting to build commands

    '''
    Loop to loop through the length of each frequency range list of commands, taking the same commands for each frequency range
    and building a string for the commands for all the frequency ranges for a particular time slice
    '''
    for x in range (0, 121):
        command = sub_commands[x] + bass_commands[x] + low_mid_commands[x] + mid_commands[x] + up_mid_commands[x] + pre_commands[x] + brill_commands[x]  # Building string
        commands.append(command) # Building full commands
        
    return commands # Returning full command list

# Method to compare the highest amplitude value in each frequency range against the randomly choosen amplitude vaules
def check(largest, number):
    command = '' # Initializing the sting command
    # If statements to determine the appropriate command based on comparing the largest amplitude values against all amplitude vaules
    if(number < (largest / 7)):
        command='0'
    elif(number < (largest / 7)*2):
        command='1'
    elif(number < (largest / 7)*3):
        command='2'
    elif(number < (largest / 7)*4):
        command='3'
    elif(number < (largest / 7)*5):
        command='4'
    elif(number < (largest / 7)*6):
        command='5'
    elif(number < largest):
        command='6'
    else:
        command= '7'
    return command # Returning the appropriate command

# Method to find the largest amplitude value for each frequency range
def find_largest(data_set):
    largest_sample = 0.0 # Initalizing variable to store the largest amplitude value
    # Loop to loop through the entire data set of amplitude values
    for sample in np.nditer(data_set):
        # If a larger values is found replace the old value with the new value
        if(float(sample) > largest_sample):
            largest_sample = float(sample)
    return largest_sample # Returning the largst amplitude value

# Method to take a random amplitude from each specgram frequency range that makes up the frequency range in question
def take_sample(frequency_range):
    from random import randint 
    samples = [] # Initializing a samples list

    # Loop to loop through all the amplitude values for specific time slice
    for sample in frequency_range:
        rand_int = randint(0, (len(frequency_range[0]) - 1)) # Generating the random number
        samples.append(sample[rand_int]) # Storing the amplitude value associated with the random number

    return samples # Returning the list of samples

#Method to transfer the list of commands to the Arduino 
def transfer(commands,duration):
    import time
    import serial
    print duration
    ser = serial.Serial("/dev/ttyACM0", 9600) # Oping serial port
    # Loop to loop through the entire list of commands
    for command in commands:
        ser.write(command) # Writting commands to the Arduino serial port one at a time 
        time.sleep(duration) # Waiting for the appropriate time bassed of time slice given by specgram
