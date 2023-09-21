import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter, buttord, filtfilt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Button, filedialog, PhotoImage, Scale, HORIZONTAL, messagebox
import tkinter as tk
import tkinter.ttk as ttk
import pygame
import time
import os
import customtkinter as ctk
from customtkinter import CTkImage
import threading
from scipy.fftpack import fft, ifft
from scipy.signal import hilbert
import wavio
from PIL import Image, ImageTk
from scipy.io.wavfile import write
from scipy.stats import norm
from numpy import int16
import tkinter.font as tkFont

pygame.mixer.init()

#Generowanie Brown noises: (jednorazowo)
# def generate_brown_noise(duration, sample_rate=44100):
#     num_samples = int(sample_rate * duration)
#     samples = np.random.randn(num_samples)
#     brown_samples = np.cumsum(samples)
#     brown_samples = brown_samples - np.mean(brown_samples)
#     brown_samples = brown_samples / np.max(np.abs(brown_samples))
#     return brown_samples

# duration1 = 30.0  
# sample_rate1 = 44100
# brown_noise = generate_brown_noise(duration1, sample_rate1)

# # Skalowanie
# brown_noise_int = (brown_noise * np.iinfo(np.int16).max).astype(np.int16)

# # Podaj ścieżkę do folderu, w którym chcesz zapisać plik
# folder_path1 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\" 

# file_name1 = "brown_noise.wav"
# full_path1 = folder_path1 + file_name1
# wavio.write(full_path1, brown_noise_int, sample_rate1)

# # Obliczenie widma
# Y1 = np.fft.fft(brown_noise)
# frequencies1 = np.fft.fftfreq(len(Y1), d=1.0/sample_rate1)

# plt.figure()
# plt.plot(frequencies1, 20 * np.log10(np.abs(Y1)))
# plt.xscale('log')
# plt.title("Widmo sygnału")
# plt.xlabel("Częstotliwość [Hz]")
# plt.ylabel("Amplituda [dB]")
# plt.xlim([20, sample_rate1 / 2])

# # Zapisz wykres do pliku
# plt.savefig(folder_path1 + "brown_noise_spectrum.png")

#Generowanie White noises: (jednorazowo)

# duration = 60.0  # sekundy
# sample_rate = 44100  # Hz

# # Generowanie szumu białego
# num_samples = int(sample_rate * duration)
# white_noise = np.random.randn(num_samples)
# scaled_white_noise = np.int16(white_noise / np.max(np.abs(white_noise)) * 32767)

# # Zapis do pliku
# output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise.wav"
# write(output_path, sample_rate, scaled_white_noise)

# # Obliczenie widma
# Y = np.fft.fft(white_noise)
# frequencies = np.fft.fftfreq(len(Y), 1.0/sample_rate)
# positive_freq_idxs = np.where(frequencies > 0)
# frequencies = frequencies[positive_freq_idxs]
# magnitude = np.abs(Y[positive_freq_idxs])

# # Wykres widma
# plt.figure()
# plt.plot(frequencies, 20 * np.log10(magnitude))
# plt.xscale('log')
# plt.title("Widmo sygnału szumu białego")
# plt.xlabel("Częstotliwość [Hz]")
# plt.ylabel("Amplituda [dB]")
# plt.xlim([20, sample_rate / 2])

# # Zapis wykresu do pliku
# spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise_spectrum.png"
# plt.savefig(spectrum_image_path)

#Generowanie Pink noises: (jednorazowo)
# def pink_noise(num_samples):
#     # Filtr IIR
#     b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
#     a = np.array([1, -2.494956002, 2.017265875, -0.522189400])
#     zi = np.random.randn(3)  # Początkowy stan filtru

#     pink = np.array([np.random.randn() for _ in range(num_samples)])
#     pink, _ = lfilter(b, a, pink, zi=zi*pink[0])
#     pink = pink/np.max(np.abs(pink))  # Normalizacja
    
#     return pink

# # Parametry
# duration = 60.0  # sekundy
# sample_rate = 44100  # Hz
# num_samples = int(sample_rate * duration)

# # Generowanie szumu różowego
# pink_signal = pink_noise(num_samples)
# scaled_pink_signal = np.int16(pink_signal / np.max(np.abs(pink_signal)) * 32767)

# # Zapis do pliku
# output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise.wav"
# write(output_path, sample_rate, scaled_pink_signal)

# # Obliczenie widma
# Y = np.fft.fft(pink_signal)
# frequencies = np.fft.fftfreq(len(Y), 1.0/sample_rate)
# positive_freq_idxs = np.where(frequencies > 0)
# frequencies = frequencies[positive_freq_idxs]
# magnitude = np.abs(Y[positive_freq_idxs])

# # Wykres widma
# plt.figure()
# plt.plot(frequencies, 20 * np.log10(magnitude))
# plt.xscale('log')
# plt.title("Widmo sygnału szumu różowego")
# plt.xlabel("Częstotliwość [Hz]")
# plt.ylabel("Amplituda [dB]")
# plt.xlim([20, sample_rate / 2])

# # Zapis wykresu do pliku
# spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise_spectrum.png"
# plt.savefig(spectrum_image_path)


#Generowanie Green noises: (jednorazowo)
# def turn_green(signal, samp_rate):
#     # start and stop of green noise range
#     left = 1612 # Hz
#     right = 2919 # Hz

#     nyquist = (samp_rate/2)
#     left_pass  = 1.1*left/nyquist
#     left_stop  = 0.9*left/nyquist
#     right_pass = 0.9*right/nyquist
#     right_stop = 1.1*right/nyquist

#     (N, Wn) = buttord(wp=[left_pass, right_pass],
#                       ws=[left_stop, right_stop],
#                       gpass=2, gstop=30, analog=0)
#     (b, a) = butter(N, Wn, btype='band', analog=0, output='ba')
#     return filtfilt(b, a, signal)

# def to_integer(signal):
#     # Take samples in [-1, 1] and scale to 16-bit integers,
#     # values between -2^15 and 2^15 - 1.
#     signal /= max(signal)
#     return int16(signal*(2**15 - 1))

# N = 48000 # samples per second

# duration = 60.0 # seconds
# num_samples = int(N * duration)

# white_noise= norm.rvs(0, 1, num_samples) 
# green = turn_green(white_noise, N)

# # Zapisz szum do pliku .wav
# output_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise.wav"
# write(output_path, N, to_integer(green))

# # Obliczenie widma
# Y = np.fft.fft(green)
# frequencies = np.fft.fftfreq(len(Y), 1.0/N)
# positive_freq_idxs = np.where(frequencies > 0)
# frequencies = frequencies[positive_freq_idxs]
# magnitude = np.abs(Y[positive_freq_idxs])

# # Wykres widma
# plt.figure()
# plt.plot(frequencies, 20 * np.log10(magnitude))
# plt.xscale('log')
# plt.title("Widmo sygnału szumu zielonego")
# plt.xlabel("Częstotliwość [Hz]")
# plt.ylabel("Amplituda [dB]")
# plt.xlim((1500, 3000))

# # Zapisz wykres do pliku .png
# spectrum_image_path = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise_spectrum.png"
# plt.savefig(spectrum_image_path)


def butter_bandstop_filter(data, lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    y = lfilter(b, a, data)
    return y

def butter_highpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

matplotlib_rgb = (0.94, 0.94, 0.94)

tkinter_rgb = tuple(int(x * 255) for x in matplotlib_rgb)

tkinter_hex = rgb_to_hex(tkinter_rgb)


LIGHT_MODE = {
    "bg": "#EDEDED",
    "btn_bg": "#D4D4D4",
    "btn_active": "#B5B5B5",
    "text": "#000000",
}

DARK_MODE = {
    "bg": "#2D2D2D",
    "btn_bg": "#3F3F3F",
    "btn_active": "#5F5F5F",
    "text": "#FFFFFF",
}


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Filter")
        self.configure(bg=tkinter_hex)
        pygame.mixer.init()
        self.info_text = None
        self.create_widgets()
        self.output_file = None
        self.state('zoomed') 
        self.file_for_menu_1 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\brown_noise.wav"
        self.file_for_menu_2 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise.wav"
        self.file_for_menu_3 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise.wav"
        self.file_for_menu_4 = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise.wav"
        self.file_for_menu_1_widmo = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\brown_noise_spectrum.png"
        self.file_for_menu_2_widmo = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\white_noise_spectrum.png"
        self.file_for_menu_3_widmo = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\pink_noise_spectrum.png"
        self.file_for_menu_4_widmo = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\szumy\\green_noise_spectrum.png"
    

    def create_widgets(self):
        self.play_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\play_icon.png")  
        self.pause_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\pause_icon.png")  
  
        original_logo = Image.open("C:\\Users\\pklyt\\Desktop\\studia\\inz\\logo.png")
        resized_logo = original_logo.resize((100, 100))  # Assuming you want the logo to be 50x50 pixels
        self.app_logo = ImageTk.PhotoImage(resized_logo)
        self.logo_label = tk.Label(self, image=self.app_logo, bg=tkinter_hex)
        self.logo_label.grid(row=0, column=0, padx=10, pady=(0,5))

        self.app_name_label = tk.Label(self, text="AudioSpectra", font=("Arial", 24), bg=tkinter_hex)
        self.app_name_label.grid(row=0, column=1, pady=(0,5), sticky="w")

        self.input_button = ctk.CTkButton(self, text="Select input file", command=self.select_input, 
                                    corner_radius=10, hover_color='#100d33')
        self.input_button.grid(row=0, column=2, padx=5, pady=(0,5), sticky="e")  

        self.filter_button = ctk.CTkButton(self, text="Filter", command=self.filter, 
                                    corner_radius=10, hover_color='#100d33')
        self.filter_button.grid(row=0, column=3, padx=(5, 10), pady=(0,5), sticky="w")

        self.play_button = tk.Button(self, image=self.play_icon, command=self.play, 
                                    bg=tkinter_hex, relief="flat")
        self.play_button.grid(row=4, column=0, pady=(10,15), padx=(100, 10), sticky="w")

        self.pause_button = tk.Button(self, image=self.pause_icon, command=self.pause, 
                                    bg=tkinter_hex, relief="flat")
        self.pause_button.grid(row=4, column=1, pady=(10,15), sticky="w")

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.update_volume, width=100)
        self.volume_slider.set(pygame.mixer.music.get_volume())  
        self.volume_slider.grid(row=4, column=3, pady=(0,0))

        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", foreground='#000437')
        
        self.progressbar = ttk.Progressbar(self, length=1000, style="custom.Horizontal.TProgressbar")
        self.progressbar.grid(row=4, column=2, sticky="w")

        self.figure = Figure(figsize=(12, 6), dpi=100, facecolor=(0.94, 0.94, 0.94))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2, column=1, columnspan=3, rowspan=2)  
        
        menu_frame = tk.Frame(self, bg="#F0F0F0")
        menu_frame.grid_propagate(False)
        menu_frame.config(width=200, height=500)  # Ustaw wymiary zgodnie z własnymi potrzebami

        menu_frame.grid(row=2, column=0, sticky="nsew", padx=(10,0))

        self.menu_button_1 = ctk.CTkButton(menu_frame, text="Brown noise", command=self.menu_command_1, corner_radius=10, width=30, hover_color='#100d33')
        self.menu_button_1.pack(fill="x", pady=(5,12))  

        self.menu_button_2 = ctk.CTkButton(menu_frame, text="White noise", command=self.menu_command_2, corner_radius=10, width=30, hover_color='#100d33')
        self.menu_button_2.pack(fill="x", pady=(5,12))

        self.menu_button_3 = ctk.CTkButton(menu_frame, text="Pink noise", command=self.menu_command_3, corner_radius=10, width=30, hover_color='#100d33')
        self.menu_button_3.pack(fill="x", pady=(5,12))

        self.menu_button_4 = ctk.CTkButton(menu_frame, text="Green noise", command=self.menu_command_4, corner_radius=10, width=30, hover_color='#100d33')
        self.menu_button_4.pack(fill="x", pady=(5,12))

        if not self.info_text:
            self.info_text = tk.Label(self, bg="#F0F0F0", wraplength=300, justify='left', anchor='nw')
            self.info_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(10,0))
        self.info_text.grid_remove()


    def plot_frequency(self, data, fs):
        fft = np.fft.fft(data)
        frequencies = np.abs(fft)
        freqs = np.fft.fftfreq(len(data), 1/fs)
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.plot(freqs[:len(data)//2], frequencies[:len(data)//2], color='#000441')  
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Frequency Spectrum')
        self.canvas.draw()

    def select_input(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        fs, data = wav.read(self.input_file)
        self.plot_frequency(data, fs)
        if self.info_text:
            self.info_text.grid_remove()

    def filter(self):
        fs, data = wav.read(self.input_file)

        initial_rms = np.sqrt(np.mean(data**2))

        lowcut = 300.0  
        nyq_rate = fs / 2.0
        low = lowcut / nyq_rate
        b, a = butter(6, low, btype='low')
        y_filtered = lfilter(b, a, data)

        analytic_signal = hilbert(y_filtered)
        amplitude_envelope = np.abs(analytic_signal)

        Y = fft(y_filtered)
        freqs = np.fft.fftfreq(len(Y), 1/fs)
        mask = np.where(freqs > 0)
        desired_spectrum = np.ones_like(freqs)
        desired_spectrum[mask] = 1 / np.sqrt(freqs[mask])
        new_Y = Y * desired_spectrum[:, np.newaxis]  
        new_y = np.real(ifft(new_Y))

        mixed_signal = data + new_y
        current_rms = np.sqrt(np.mean(mixed_signal**2))
        scaling_factor = initial_rms / current_rms
        mixed_signal *= scaling_factor

        self.plot_frequency(mixed_signal, fs)

        output_folder = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\zapisane_probki"
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.output_file = os.path.join(output_folder, f'output_{current_time}.wav')
        wav.write(self.output_file, fs, mixed_signal.astype(np.int16))

        self.figure.set_size_inches(12, 6)
        self.canvas.get_tk_widget().config(width=1200, height=600)


        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load(self.output_file)

        tk.messagebox.showinfo("Filtering", "Filtering finished!")


    def play(self):
        if self.output_file is not None:  
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()

            duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  
            self.progressbar["maximum"] = duration_ms  

            self.progressbar["value"] = 0


            self.after(100, self.update_progressbar, duration_ms)

    def pause(self):
        pygame.mixer.music.pause()

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume)/100)

    def update_progressbar(self, duration_ms):
        if pygame.mixer.music.get_busy():  
            elapsed_time_ms = pygame.mixer.music.get_pos() 
            self.progressbar["value"] = elapsed_time_ms

            self.after(100, self.update_progressbar, duration_ms)
        else:
            self.progressbar["value"] = 0

    def menu_command_1(self):
        self.output_file = self.file_for_menu_1
        spectrum_path = self.file_for_menu_1_widmo
        imgWidmo = Image.open(spectrum_path)
        # imgWidmo = ImageTk.PhotoImage(imgWidmo)
        for ax in self.figure.axes:
            ax.remove()
        ax = self.figure.add_axes([0,0,1,1])
        ax.imshow(imgWidmo)
        ax.axis('off')
        self.canvas.draw()
        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  
        self.progressbar["maximum"] = duration_ms 
        self.progressbar["value"] = 0
        self.after(100, self.update_progressbar, duration_ms)
        self.info_text.grid()
        self.info_text.config(text="Tutaj umieść informacje na temat szumu czerwonego.")


    def menu_command_2(self):
        self.output_file = self.file_for_menu_2
        spectrum_path = self.file_for_menu_2_widmo
        imgWidmo = Image.open(spectrum_path)
        # imgWidmo = ImageTk.PhotoImage(imgWidmo)
        for ax in self.figure.axes:
            ax.remove()
        ax = self.figure.add_axes([0,0,1,1])
        ax.imshow(imgWidmo)
        ax.axis('off')
        self.canvas.draw()
        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  
        self.progressbar["maximum"] = duration_ms 
        self.progressbar["value"] = 0
        self.after(100, self.update_progressbar, duration_ms)
        self.info_text.grid()
        self.info_text.config(text="Tutaj umieść informacje na temat szumu białego.")

    def menu_command_3(self):
        self.output_file = self.file_for_menu_3
        spectrum_path = self.file_for_menu_3_widmo
        imgWidmo = Image.open(spectrum_path)
        # imgWidmo = ImageTk.PhotoImage(imgWidmo)
        for ax in self.figure.axes:
            ax.remove()
        ax = self.figure.add_axes([0,0,1,1])
        ax.imshow(imgWidmo)
        ax.axis('off')
        self.canvas.draw()
        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  
        self.progressbar["maximum"] = duration_ms 
        self.progressbar["value"] = 0
        self.after(100, self.update_progressbar, duration_ms)
        self.info_text.grid()
        self.info_text.config(text="Tutaj umieść informacje na temat szumu różowego.")

    def menu_command_4(self):
        self.output_file = self.file_for_menu_4
        spectrum_path = self.file_for_menu_4_widmo
        imgWidmo = Image.open(spectrum_path)
        # imgWidmo = ImageTk.PhotoImage(imgWidmo)
        for ax in self.figure.axes:
            ax.remove()
        ax = self.figure.add_axes([0,0,1,1])
        ax.imshow(imgWidmo)
        ax.axis('off')
        self.canvas.draw()
        pygame.mixer.music.load(self.output_file)
        pygame.mixer.music.play()
        duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  
        self.progressbar["maximum"] = duration_ms 
        self.progressbar["value"] = 0
        self.after(100, self.update_progressbar, duration_ms)
        self.info_text.grid()
        self.info_text.config(text="Tutaj umieść informacje na temat szumu zielonego.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()