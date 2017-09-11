# Importing the library used to play library
import alsaaudio 

#method to play Audio track take in argument such as No. channels, sample rate and width of the WAV file
def play_audio(beat, channels, sample_rate, samp_width):
    
    device = alsaaudio.PCM(card = 'default') #Setting the audio device to the default audio device of computer
    # Print method to display the WAV file being played and the information extracted
    print('\nPlaying : %s \nNo Channels : %d \nSample Rate : %d \nSample Width: %d\n' % (beat, channels,
                                               sample_rate, samp_width))
    # Set attributes
    device.setchannels(channels) # Setting the channel of the default audio device to the channels of the WAV file
    device.setrate(sample_rate) # Setting the sample rate of the default audio device to the sample rate of the WAV file
    
    # If statement to set the format of the default audio device based of the sample width of the WAV file
    # 8bit is unsigned in wav files
    if samp_width == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif samp_width == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif samp_width == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif samp_width == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    import wave
    f = wave.open(beat, 'rb') # Opening the WAV file
    device.setperiodsize(320) # The peiods the default audio device will use when playing the WAV file
    data = f.readframes(320) # Reading in the same amoutnt of frames as the period size

    # Loop to loop through the entire WAV file
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(320)

    f.close() # Closing the WAV file
    return
