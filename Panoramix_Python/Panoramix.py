'''
Programmer: Ciaran Roft
Date: 21/02/2017
Description: A prograqm that is the main runner of Panoramix, it is in charge of calling all of the nessesary method to extract the WAV file
             information. It is also responsible for controlling the multithreading that takes place in order to play the WAV file at the
             same time that the Arduino is send command to control the LEDs. Panoramix can send amplitude values and frequency vaules to the Arduino
'''

beat = 'beat.wav'

# Calling the method to extract information from a WAV file
from PanoramixAnalyser import extract_wav_data as extract
amp_data, time, sample_rate, channels, samp_width  = extract(beat)

# Method to plot the Waveform and Spectrogram, Returns frequency data, and the time slices of the data
from PanoramixAnalyser import plot_wave_data as plot
freq_data, time_slice = plot(amp_data, time, sample_rate) 


# Calling the method to generate commands by using the averages
from GenerateCommands import build_commands_rand as build
amp_commands = build(amp_data, sample_rate)

# Method to generate the commands based on the frequency
from Panoramix_Frequency import split_freq as split
freq_commands, difference = split(freq_data, time_slice)

#Import user defined library to transfer commands :Frequency
from Panoramix_Frequency import transfer as freq_transfer 

#Import user defined library to transfer commands to the Arduino:Amplitude
from Transfer import transfer as amp_transfer 

from threading import Thread #Importing pythons multithreading module

'''
The led_thread starts the thread to comunicate commands to the Arduino
The target method is either of the transer method, and the arguments passed to it is a numpy array of string commands,
and when using frequency you must pass in the appropriate waiting time
'''
led_thread = Thread(
    target = freq_transfer, 
    args = [freq_commands, difference],
    )

#Importing usrer library to play WAV files
from PlayAudio import play_audio as play

'''
The player_thread starts the thread that controls the playing of WAV files
The target method is play, and the argument passed to it is the name of the WAV file to be played
'''
player_thread = Thread(
    target = play,
    args = [beat, channels, sample_rate, samp_width],
    )

led_thread.start() # Starting the led_thread
player_thread.start() # Starting the player_thread

