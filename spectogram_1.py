import matplotlib.pyplot as plot
from scipy.io import wavfile
import numpy as np
import librosa, scipy
import librosa.display

#samplingFrequency, signalData = wavfile.read('/home/puru/Documents/Projects/Audio/librosa_code/Raga_Surabhi.wav')
signalData, samplingFrequency = librosa.load('/home/puru/Documents/Projects/Audio/librosa_code/Raga_Surabhi_3.wav')
plot.subplot(211)
plot.title('Spectrogram of a wav file with piano music')
plot.plot(signalData)

plot.xlabel('Sample')

plot.ylabel('Amplitude')
plot.subplot(212)

plot.specgram(signalData,Fs=samplingFrequency)

plot.xlabel('Time')

plot.ylabel('Frequency')


plot.show()