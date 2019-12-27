# sampling a sine wave programmatically
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

plt.style.use('ggplot')
# sampling information
Fs = 44100 # sample rate
T = 1/Fs # sampling period
t = 0.1 # seconds of sampling
N = Fs*t # total points in signal
# signal information
freq = 100 # in hertz, the desired natural frequency
omega = 2*np.pi*freq # angular frequency for sine waves
t_vec = np.arange(N)*T # time vector for plotting
y = np.sin(omega*t_vec)+np.sin((omega/2)*t_vec)
D_left = np.abs(librosa.stft(y, center=False))
D = np.abs(librosa.stft(y))
librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
#librosa.display.specshow(D, y_axis='log', x_axis='time')
#plt.plot(t_vec,y)
plt.title('Power spectrogram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
#plt.show()