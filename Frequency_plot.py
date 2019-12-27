import librosa, scipy
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.style as ms
import numpy as np
from scipy.io import wavfile
from scipy.signal import kaiserord, lfilter, firwin, freqz, spectrogram
ms.use('seaborn-muted')

y, sr = librosa.load('/home/puru/Documents/Projects/Audio/librosa_code/Raga_Surabhi_3.wav')
X = scipy.fft(y)
X1 = np.fft.fftshift(scipy.fft(y))
X_mag = np.absolute(X1)
f2 = np.linspace(-sr/2, sr/2, len(X_mag)) # frequency variable
plt.figure()
#plt.subplot(211)
plt.plot(f2, X_mag) # magnitude spectrum
plt.xlabel('Frequency (Hz)')
#plt.show()
plt.figure()
plt.subplot(121)
powerSpectrum, freqenciesFound, time, imageAxis = plt.specgram(y, Fs=sr)
plt.xlabel('Time')
plt.ylabel('Frequency')
tup =[]
x = [i for i in freqenciesFound]
#print(powerSpectrum.shape,len(time))
for i in range(1,len(freqenciesFound)):
    if(freqenciesFound[i]/freqenciesFound[i-1] == (3/2)):
        tup.append((freqenciesFound[i-1],freqenciesFound[i]))
#plt.plot(freqenciesFound)

#print(tup)
#print(f)
nyq_rate = sr / 2.0

# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.  We'll design the filter
# with a 5 Hz transition width.
width = 5.0/nyq_rate

# The desired attenuation in the stop band, in dB.
ripple_db = 60.0

# Compute the order and Kaiser parameter for the FIR filter.
N, beta = kaiserord(ripple_db, width)

# The cutoff frequency of the filter.
cutoff_hz = 2000.0

# Use firwin with a Kaiser window to create a lowpass FIR filter.
taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

# Use lfilter to filter x with the FIR filter.
filtered_x = lfilter(taps, 1.0, y)
delay = 0.5 * (N-1) / sr
plt.subplot(122)
powerSpectrum, freqenciesFound1, time, imageAxis = plt.specgram(filtered_x, Fs=sr)
plt.show()
print(freqenciesFound1)