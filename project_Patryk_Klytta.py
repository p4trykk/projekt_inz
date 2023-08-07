import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Button, filedialog, PhotoImage, Scale, HORIZONTAL
import tkinter as tk
import pygame
import time
import os

def butter_bandstop_filter(data, lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    y = lfilter(b, a, data)
    return y

# def butter_lowpass_filter(data, cutoff, fs, order=5):
#     nyq = 0.5 * fs
#     normal_cutoff = cutoff / nyq
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     y = lfilter(b, a, data)
#     return y

def butter_highpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y


def plot_frequency(data, fs, figure):
    fft = np.fft.fft(data)
    frequencies = np.abs(fft)
    freqs = np.fft.fftfreq(len(data), 1/fs)
    figure.clf()
    ax = figure.add_subplot(111)
    ax.plot(freqs[:len(data)//2], frequencies[:len(data)//2])  
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Amplitude')
    ax.set_title('Frequency Spectrum')

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Filter")
        self.geometry("800x600")
        pygame.mixer.init()
        self.create_widgets()
        self.output_file = None

    def create_widgets(self):
        self.play_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\play_icon.png")  # Zastąp nazwę pliku swoją ikoną
        self.play_icon = self.play_icon.subsample(2, 2)  # Skaluj obraz do 1/2 oryginalnego rozmiaru
        self.pause_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\pause_icon.png")  # Zastąp nazwę pliku swoją ikoną
        self.pause_icon = self.pause_icon.subsample(2, 2)  # Skaluj obraz do 1/2 oryginalnego rozmiaru
        self.input_button = tk.Button(self, text="Select input file", command=self.select_input)
        self.input_button.pack()
        self.filter_button = tk.Button(self, text="Filter", command=self.filter)
        self.filter_button.pack()
        self.play_button = tk.Button(self, image=self.play_icon, command=self.play)
        self.play_button.pack(side='left')  # Umieszcza przycisk po lewej stronie
        self.pause_button = tk.Button(self, image=self.pause_icon, command=self.pause)
        self.pause_button.pack(side='left')  # Umieszcza przycisk po lewej stronie
        self.figure = Figure(figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()
        self.volume_slider = Scale(self, from_=0, to=1, orient=HORIZONTAL, resolution=0.01, command=self.update_volume)
        self.volume_slider.set(pygame.mixer.music.get_volume())  # Ustaw wartość początkową na aktualną głośność
        self.volume_slider.pack()

    def select_input(self):
        self.input_file = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
        # Wczytanie pliku
        fs, data = wav.read(self.input_file)
        # Wykres częstotliwości dla oryginalnego dźwięku
        plot_frequency(data, fs, self.figure)
        self.canvas.draw()  # Odświeżenie wykresu

    def filter(self):
        # Wczytanie pliku
        fs, data = wav.read(self.input_file)

        # Ustalenie częstotliwości, które chcemy odfiltrować
        lowcut = 4000.0  # Dolna granica zakresu do odfiltrowania
        highcut = 20000.0  # Górna granica zakresu do odfiltrowania

        # Filtracja sygnału
        filtered_data = butter_bandstop_filter(data, lowcut, highcut, fs)

        # Wzmocnienie wysokich częstotliwości
        high_passed_data = butter_highpass_filter(filtered_data, 1500, fs)

        # Wykres częstotliwości dla przefiltrowanego i niskoprzepustowego dźwięku
        plot_frequency(high_passed_data, fs, self.figure)
        self.canvas.draw()  # Odświeżenie wykresu

        # Zapisanie przefiltrowanych danych do nowego pliku
        # Zapisanie przefiltrowanych danych do nowego pliku
        output_folder = "C:\\Users\\pklyt\\Desktop\\studia\\inz\\zapisane_probki"  # ścieżka do katalogu, w którym chcesz zapisać plik
        current_time = time.strftime("%Y%m%d-%H%M%S")
        self.output_file = os.path.join(output_folder, f'output_{current_time}.wav')
        wav.write(self.output_file, fs, high_passed_data.astype(np.int16))

        # Zatrzymaj odtwarzanie i usuń obecnie załadowany plik
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # Załaduj nowy plik do odtworzenia
        pygame.mixer.music.load(self.output_file)

        tk.messagebox.showinfo("Filtering", "Filtering finished!")

    def play(self):
        if self.output_file is not None:  # Jeśli plik wyjściowy istnieje
            pygame.mixer.music.load(self.output_file)
            pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

if __name__ == "__main__":
    app = Application()
    app.mainloop()