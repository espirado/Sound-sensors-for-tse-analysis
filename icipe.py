#!/usr/bin/env python

# Script for recording audio files using i2s sound sensor connected to a Raspberry Pi
#
# Usage: run from CRON every 10 minutes

import pyaudio
import wave
import sys
from datetime import datetime 

#get time and use it to stamp the audio files 
record_duration  = 100 # 10 secs

print("=====================ICIPE Insects Monitor==========================================")
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 50 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename =  '$audio_time_stamp.wav' 

 #'test1.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                    input_device_index = dev_index,input = True, \
                    frames_per_buffer=chunk)
print("recording")
print("===============================================================")

def writeFramesToFile(frames):
    wav_output_filename = getTimeStampFileName()
    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    print("written: %s" % wav_output_filename)

def getTimeStampFileName():
    dt = datetime.now()
    fname = dt.strftime("%Y%m%d%H%M%S")
    fname = "%s.wav" % fname
    return fname


while (True):
    frames = []

    # loop through stream and append audio chunks to frame array
    for sound_frame in range(0,int((samp_rate/chunk)*record_duration)):
        data = stream.read(chunk)
        frames.append(data)

    writeFramesToFile(frames)

# stop the stream, close it, and terminate the pyaudio instantiation
stream.stop_stream()
stream.close()
audio.terminate()

