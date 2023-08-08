import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import butter, lfilter
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

pygame.mixer.init()

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

# Używamy tego samego koloru co w obiekcie Figure
matplotlib_rgb = (0.94, 0.94, 0.94)

# Przeskalowanie wartości zmiennoprzecinkowych do zakresu 0-255
tkinter_rgb = tuple(int(x * 255) for x in matplotlib_rgb)

# Użycie funkcji rgb_to_hex do konwersji na format hex
tkinter_hex = rgb_to_hex(tkinter_rgb)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Filter")
        self.configure(bg=tkinter_hex)
        pygame.mixer.init()
        self.create_widgets()
        self.output_file = None
        self.state('zoomed') 

    def create_widgets(self):
        self.play_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\play_icon.png")  
        self.pause_icon = PhotoImage(file="C:\\Users\\pklyt\\Desktop\\studia\\inz\\pause_icon.png")  

        self.input_button = ctk.CTkButton(self, text="Select input file", command=self.select_input, 
                                    corner_radius=10)
        self.input_button.grid(row=0, column=0, columnspan=4, pady=10)  # Zmieniony columnspan na 4

        self.filter_button = ctk.CTkButton(self, text="Filter", command=self.filter, 
                                    corner_radius=10)
        self.filter_button.grid(row=1, column=0, columnspan=4, pady=10)  # Zmieniony columnspan na 4

        self.play_button = tk.Button(self, image=self.play_icon, command=self.play, 
                                    bg=tkinter_hex, relief="flat")
        self.play_button.grid(row=3, column=0, pady=10, padx=(100, 10))

        self.pause_button = tk.Button(self, image=self.pause_icon, command=self.pause, 
                                    bg=tkinter_hex, relief="flat")
        self.pause_button.grid(row=3, column=1, pady=10)

        self.volume_slider = Scale(self, from_=0, to=100, orient=HORIZONTAL, command=self.update_volume)
        self.volume_slider.set(pygame.mixer.music.get_volume())  
        self.volume_slider.grid(row=3, column=3, pady=(0,15))

        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", foreground='#000437')
        
        self.progressbar = ttk.Progressbar(self, length=1000, style="custom.Horizontal.TProgressbar")
        self.progressbar.grid(row=3, column=2, padx=15)

        self.figure = Figure(figsize=(12, 6), dpi=100, facecolor=(0.94, 0.94, 0.94))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2, column=1, columnspan=3)  # Zmieniony columnspan na 4
        
        # Create a menu frame
        menu_frame = tk.Frame(self, bg="#F0F0F0")
        menu_frame.grid(row=2, column=0, sticky="nsew", padx=(10,0))

        # Create buttons for the menu
        self.menu_button_1 = tk.Button(menu_frame, text="Menu 1", command=self.menu_command_1)
        self.menu_button_1.pack(fill="x")

        self.menu_button_2 = tk.Button(menu_frame, text="Menu 2", command=self.menu_command_2)
        self.menu_button_2.pack(fill="x")

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
        self.plot_frequency(high_passed_data, fs)
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

            duration_ms = pygame.mixer.Sound(self.output_file).get_length() * 1000  # Get length of audio file in milliseconds
            self.progressbar["maximum"] = duration_ms  # Set length of progressbar to length of audio

            # Reset progressbar; necessary in case this is not the first file that was played
            self.progressbar["value"] = 0

            # Start updating progressbar
            self.after(100, self.update_progressbar, duration_ms)

    def pause(self):
        pygame.mixer.music.pause()

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(int(volume)/100)

    def update_progressbar(self, duration_ms):
        if pygame.mixer.music.get_busy():  # If a song is currently playing
            # Update progress bar
            elapsed_time_ms = pygame.mixer.music.get_pos()  # Get current position of song
            self.progressbar["value"] = elapsed_time_ms

            # Schedule to update progress bar again in 100 ms
            self.after(100, self.update_progressbar, duration_ms)
        else:
            # Reset progress bar
            self.progressbar["value"] = 0

    def menu_command_1(self):
        # Do something when menu 1 is selected
        pass

    def menu_command_2(self):
        # Do something when menu 2 is selected
        pass

if __name__ == "__main__":
    app = Application()
    app.mainloop()