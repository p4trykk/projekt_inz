import numpy as np
from numpy import int16
import wavio
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.stats import norm
from scipy.signal import butter, lfilter, buttord, filtfilt


#Generowanie Brown noises: (jednorazowo)
def generate_brown_noise(duration, sample_rate=44100):
    num_samples = int(sample_rate * duration)
    samples = np.random.randn(num_samples)
    brown_samples = np.cumsum(samples)
    brown_samples = brown_samples - np.mean(brown_samples)
    brown_samples = brown_samples / np.max(np.abs(brown_samples))
    return brown_samples

duration1 = 30.0  
sample_rate1 = 44100
brown_noise = generate_brown_noise(duration1, sample_rate1)

# # Skalowanie
brown_noise_int = (brown_noise * np.iinfo(np.int16).max).astype(np.int16)

folder_path1 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\" 

file_name1 = "brown_noise.wav"
full_path1 = folder_path1 + file_name1
wavio.write(full_path1, brown_noise_int, sample_rate1)

# # Obliczenie widma
Y1 = np.fft.fft(brown_noise)
frequencies1 = np.fft.fftfreq(len(Y1), d=1.0/sample_rate1)

plt.figure()
plt.plot(frequencies1, 20 * np.log10(np.abs(Y1)))
plt.xscale('log')
plt.title("Widmo sygnału")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.xlim([20, sample_rate1 / 2])

plt.savefig(folder_path1 + "brown_noise_spectrum.png")

#Generowanie White noises: (jednorazowo)

duration = 60.0  # sekundy
sample_rate = 44100  # Hz

# # Generowanie szumu białego
num_samples = int(sample_rate * duration)
white_noise = np.random.randn(num_samples)
scaled_white_noise = np.int16(white_noise / np.max(np.abs(white_noise)) * 32767)

output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise.wav"
write(output_path, sample_rate, scaled_white_noise)

# # Obliczenie widma
Y = np.fft.fft(white_noise)
frequencies = np.fft.fftfreq(len(Y), 1.0/sample_rate)
positive_freq_idxs = np.where(frequencies > 0)
frequencies = frequencies[positive_freq_idxs]
magnitude = np.abs(Y[positive_freq_idxs])

plt.figure()
plt.plot(frequencies, 20 * np.log10(magnitude))
plt.xscale('log')
plt.title("Widmo sygnału szumu białego")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.xlim([20, sample_rate / 2])

spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise_spectrum.png"
plt.savefig(spectrum_image_path)

#Generowanie Pink noises: (jednorazowo)
def pink_noise(num_samples):
    # Filtr IIR
    b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
    a = np.array([1, -2.494956002, 2.017265875, -0.522189400])
    zi = np.random.randn(3)  # Początkowy stan filtru

    pink = np.array([np.random.randn() for _ in range(num_samples)])
    pink, _ = lfilter(b, a, pink, zi=zi*pink[0])
    pink = pink/np.max(np.abs(pink))  # Normalizacja
    
    return pink

duration = 60.0  # sekundy
sample_rate = 44100  # Hz
num_samples = int(sample_rate * duration)

# # Generowanie szumu różowego
pink_signal = pink_noise(num_samples)
scaled_pink_signal = np.int16(pink_signal / np.max(np.abs(pink_signal)) * 32767)

output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise.wav"
write(output_path, sample_rate, scaled_pink_signal)

# # Obliczenie widma
Y = np.fft.fft(pink_signal)
frequencies = np.fft.fftfreq(len(Y), 1.0/sample_rate)
positive_freq_idxs = np.where(frequencies > 0)
frequencies = frequencies[positive_freq_idxs]
magnitude = np.abs(Y[positive_freq_idxs])

plt.figure()
plt.plot(frequencies, 20 * np.log10(magnitude))
plt.xscale('log')
plt.title("Widmo sygnału szumu różowego")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.xlim([20, sample_rate / 2])

spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise_spectrum.png"
plt.savefig(spectrum_image_path)


#Generowanie Green noises: (jednorazowo)
def turn_green(signal, samp_rate):
    # wart. graniczne
    left = 1612 # Hz
    right = 2919 # Hz

    nyquist = (samp_rate/2)
    left_pass  = 1.1*left/nyquist
    left_stop  = 0.9*left/nyquist
    right_pass = 0.9*right/nyquist
    right_stop = 1.1*right/nyquist

    (N, Wn) = buttord(wp=[left_pass, right_pass],
                      ws=[left_stop, right_stop],
                      gpass=2, gstop=30, analog=0)
    (b, a) = butter(N, Wn, btype='band', analog=0, output='ba')
    return filtfilt(b, a, signal)

def to_integer(signal):
    # wart:-2^15 - 2^15 - 1.
    signal /= max(signal)
    return int16(signal*(2**15 - 1))

N = 48000 

duration = 60.0 # sekundy
num_samples = int(N * duration)

white_noise= norm.rvs(0, 1, num_samples) 
green = turn_green(white_noise, N)

output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise.wav"
write(output_path, N, to_integer(green))

Y = np.fft.fft(green)
frequencies = np.fft.fftfreq(len(Y), 1.0/N)
positive_freq_idxs = np.where(frequencies > 0)
frequencies = frequencies[positive_freq_idxs]
magnitude = np.abs(Y[positive_freq_idxs])

plt.figure()
plt.plot(frequencies, 20 * np.log10(magnitude))
plt.xscale('log')
plt.title("Widmo sygnału szumu zielonego")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Amplituda [dB]")
plt.xlim((1500, 3000))

spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise_spectrum.png"
plt.savefig(spectrum_image_path)