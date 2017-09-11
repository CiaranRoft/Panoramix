import pylab as py
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import remez, lfilter
import wave
import struct

def plot_wave_data(wave_data, time, sample_rate):
    print 'Displaying Waveform ...'
    plt.subplot(211)
    plt.title('Left Channel')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (s)')
    plt.plot(time, wave_data)
    plt.axis('tight')
    
    print 'Displaying Spectrogram .....'
    plt.subplot(212)
    data, freqs, times, im = py.specgram(wave_data, Fs = sample_rate, NFFT = 1024,  noverlap = 128)
    plt.axis('tight')
    plt.show()#block = False)
    return data, times

# Method to extract WAV file data
def extract_wav_data(beat):
    spf = wave.open(beat,'r') # opening the WAV file
    sample_rate = spf.getframerate() #Extracting the sample rate
    sound_info = spf.readframes(-1) # Extract all of the raw amplitude values
    resize_shape = spf.getnframes() # Extract the total number of frames

    num_chans = spf.getnchannels() # Extracting the number of channels for the audio player
    samp_width = spf.getsampwidth() # Extracting the sample width from the WAV file
    
    #Convert from string the numpy array
    sound_info = py.fromstring(sound_info, 'Int16').reshape(resize_shape, 2)

    #Create a time vector space lineraly with size of the audio file to clean up plots
    time = py.np.linspace(0, len(sound_info)/float(sample_rate), num=len(sound_info))

    wav_data = sound_info[:, 0] # Taking one channel of audio
    spf.close()# Closing the WAV file
    return wav_data, time, sample_rate, num_chans, samp_width 

