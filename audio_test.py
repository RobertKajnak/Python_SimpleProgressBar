# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 22:38:45 2018

@author: Hesiris
"""
import numpy as np
import wave
import os

frequency = 440.0
duration = 2

samplerate = 44100
samplewidth = 2 #16 bits, therefore 2 bytes
duration *= samplewidth

samples = samplerate*duration
raw_audio = np.zeros(samples,dtype=np.int16)
offset = 2**14
amplitude = (2**15)*0.794328 #-2DB -- it doesn't need to be super-precise

for i in range(samples):
    raw_audio[i]=amplitude*np.sin(np.pi*2*frequency*i/samplerate)
    
    
import matplotlib.pyplot as plt
plt.plot(raw_audio[:1500])

filename = '__temp_success_tune.wav';
g = wave.open(filename,'wb')

g.setnchannels(1)
g.setsampwidth(samplewidth)
g.setframerate(samplerate)
g.setnframes(samples)
g.writeframes(raw_audio)
g.close()


os.system('powershell -c (New-Object Media.SoundPlayer \'%s\').PlaySync();'%filename)

os.remove(filename)
#$path= "\\remote\C$\windows\System32\WindowsPowerShell\v1.0\powershell.exe"
#if(test-path $path){(ls $path).VersionInfo}