import numpy as np
from scipy.signal import butter, lfilter
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage, HORIZONTAL
import tkinter as tk
import tkinter.ttk as ttk
import pygame
import os
import customtkinter as ctk
from PIL import Image, ImageTk
import webbrowser
import pyaudio
import padasip as pa
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


pygame.mixer.init()


def save_to_drive(filename):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  
    drive = GoogleDrive(gauth)
    file_drive = drive.CreateFile({'title': filename})
    file_drive.SetContentFile(filename)
    file_drive.Upload()
    print(f'{filename} zostal zapisany na Dysku Google.')
    

def butter_bandstop_filter(data, lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    y = lfilter(b, a, data)
    return y

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
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



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Spectra")
        self.configure(bg=tkinter_hex)
        pygame.mixer.init()
        self.info_text = None
        self.create_widgets()
        self.output_file = None
        self.stream = None
        self.lms_filter = pa.filters.FilterLMS(n=100, mu=0.01, w="random")
        self.p = None
        self.state('zoomed') 

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.file_for_menu_1 = os.path.join(base_path, "szumy", "brown_noise.wav")
        self.file_for_menu_2 = os.path.join(base_path, "szumy", "white_noise.wav")
        self.file_for_menu_3 = os.path.join(base_path, "szumy", "pink_noise.wav")
        self.file_for_menu_4 = os.path.join(base_path, "szumy", "green_noise.mp3")
        self.file_for_menu_1_widmo = os.path.join(base_path, "szumy", "brown_noise_spectrum.png")
        self.file_for_menu_2_widmo = os.path.join(base_path, "szumy", "white_noise_spectrum.png")
        self.file_for_menu_3_widmo = os.path.join(base_path, "szumy", "pink_noise_spectrum.png")
        self.file_for_menu_4_widmo = os.path.join(base_path, "szumy", "green_noise_spectrum.png")

        self.auto_refresh()


    def create_widgets(self):
        self.play_icon = PhotoImage(file="icons/play_icon.png")
        self.pause_icon = PhotoImage(file="icons/pause_icon.png")

        base_path = os.path.dirname(os.path.abspath(__file__))
        
        logo_path = os.path.join(base_path, "icons", "audio-editing2.png")
        original_logo = Image.open(logo_path)
        resized_logo = original_logo.resize((100, 100)) 
        self.app_logo = ImageTk.PhotoImage(resized_logo)
        self.logo_label = tk.Label(self, image=self.app_logo, bg=tkinter_hex)
        self.logo_label.grid(row=0, column=0, padx=10, pady=(0,5))

        self.app_name_label = tk.Label(self, text="AudioSpectra", font=("PT Sans", 24), bg=tkinter_hex)
        self.app_name_label.grid(row=0, column=1, pady=(0,5), sticky='w')

        self.start_noise_cancelling_button = ctk.CTkButton(self, text="Start", command=self.start_noise_cancelling)
        self.start_noise_cancelling_button.grid(row=0, column=2, padx=5, pady=(0,5), sticky="e")

        self.stop_noise_cancelling_button = ctk.CTkButton(self, text="Stop", command=self.stop_noise_cancelling)
        self.stop_noise_cancelling_button.grid(row=0, column=3, padx=(5, 10), pady=(0,5), sticky="w")

        self.save_to_drive_button = ctk.CTkButton(self, text="Dysk Google", command=self.save_files_to_drive)
        self.save_to_drive_button.grid(row=0, column=2, padx=(705,5), pady=(0,5), sticky='w')
        
        self.play_button = tk.Button(self, image=self.play_icon, command=self.play, 
                                    bg=tkinter_hex, relief="flat")
        self.play_button.grid(row=4, column=0, pady=(10,15), padx=(100, 10), sticky="ws")

        self.pause_button = tk.Button(self, image=self.pause_icon, command=self.pause, 
                                    bg=tkinter_hex, relief="flat")
        self.pause_button.grid(row=4, column=1, pady=(10,15), sticky="ws")

        self.volume_slider = ctk.CTkSlider(self, from_=0, to=100, command=self.update_volume, width=100)
        self.volume_slider.set(pygame.mixer.music.get_volume())  
        self.volume_slider.grid(row=4, column=3, pady=(0,0))
        self.volume_slider.bind("<Enter>", self.show_volume)  
        self.volume_slider.bind("<Leave>", self.hide_volume)

        style = ttk.Style()
        style.configure("custom.Horizontal.TProgressbar", foreground='#000437')
        
        self.progressbar = ttk.Progressbar(self, length=1000, style="custom.Horizontal.TProgressbar")
        self.progressbar.grid(row=4, column=2, sticky="w")

        self.figure = Figure(figsize=(9, 6), dpi=100, facecolor=(0.94, 0.94, 0.94))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(row=2, column=1, columnspan=3, rowspan=2, padx=(20,0))  
        
        menu_frame = tk.Frame(self, bg="#F0F0F0")
        menu_frame.grid_propagate(False)
        menu_frame.config(width=150, height=500) 

        menu_frame.grid(row=2, column=0, sticky="nsew", padx=(10,0))

        self.menu_button_1 = ctk.CTkButton(menu_frame, text="Szum czerwony", command=self.menu_command_1, corner_radius=10, width=30, hover_color='#100d33', font=("PT Sans", 14))
        self.menu_button_1.pack(fill="x", pady=(5,12))  

        self.menu_button_2 = ctk.CTkButton(menu_frame, text="Szum biały", command=self.menu_command_2, corner_radius=10, width=30, hover_color='#100d33', font=("PT Sans", 14))
        self.menu_button_2.pack(fill="x", pady=(5,12))

        self.menu_button_3 = ctk.CTkButton(menu_frame, text="Szum różowy", command=self.menu_command_3, corner_radius=10, width=30, hover_color='#100d33', font=("PT Sans", 14))
        self.menu_button_3.pack(fill="x", pady=(5,12))

        self.menu_button_4 = ctk.CTkButton(menu_frame, text="Szum zielony", command=self.menu_command_4, corner_radius=10, width=30, hover_color='#100d33', font=("PT Sans", 14))
        self.menu_button_4.pack(fill="x", pady=(5,12))

        self.file_listbox = tk.Listbox(menu_frame, bg="#F0F0F0", fg="#000000", height=15, width=30, font=("PT Sans", 8))
        self.file_listbox.config(relief="solid", highlightbackground="#1F6AA5", highlightthickness=2, selectbackground="#1F6AA5")
        self.file_listbox.pack(fill="x", pady=(5,12))
        self.file_listbox.bind('<<ListboxSelect>>', self.play_selected_file_with_progress)
        self.update_file_list()

        self.settings_box = ctk.CTkButton(self, width=150, height=410, corner_radius=10,  text="")
        self.settings_box.grid(row=2, column=0, columnspan=2, sticky="ne", pady=(5,0))
        self.settings_box.configure(state="disabled")
        
        self.filter_label = tk.Label(self, text="Wybierz filtr:", font=("PT Sans", 12), bg="#1F6AA5", fg="#F0F0F0")
        self.filter_label.grid(row=2, column=0, columnspan=2, sticky="ne", pady=(10, 5), padx=(0,25))

        self.filter_button_1 = ctk.CTkButton(self, text="Mowa ludzka", command=lambda: self.set_filter_function(self.butter_bandpass_filter_1), corner_radius=10, width=120, hover_color='#100d33', font=("PT Sans", 14), bg_color="#1F6AA5", border_width=1)
        self.filter_button_1.grid(row=2, column=0, columnspan=2, padx=(0,14), pady=(60,5), sticky="ne")

        self.filter_button_2 = ctk.CTkButton(self, text="Ruch uliczny", command=lambda: self.set_filter_function(self.butter_bandpass_filter_2), corner_radius=10, width=120, hover_color='#100d33', font=("PT Sans", 14), bg_color="#1F6AA5", border_width=1)
        self.filter_button_2.grid(row=2, column=0, columnspan=2, padx=(0,14), pady=(100,5), sticky="ne")

        self.filter_button_3 = ctk.CTkButton(self, text="Odkurzacz", command=lambda: self.set_filter_function(self.butter_bandpass_filter_3), corner_radius=10, width=120, hover_color='#100d33', font=("PT Sans", 14), bg_color="#1F6AA5", border_width=1)
        self.filter_button_3.grid(row=2, column=0, columnspan=2, padx=(0,14), pady=(140,5), sticky="ne")

        self.filter_button_4 = ctk.CTkButton(self, text="Kosiarka", command=lambda: self.set_filter_function(self.butter_bandpass_filter_4), corner_radius=10, width=120, hover_color='#100d33', font=("PT Sans", 14), bg_color="#1F6AA5", border_width=1)
        self.filter_button_4.grid(row=2, column=0, columnspan=2, padx=(0,14), pady=(180,5), sticky="ne")

        self.filter_button_5 = ctk.CTkButton(self, text="Szum wiatru", command=lambda: self.set_filter_function(self.butter_bandpass_filter_5), corner_radius=10, width=120, hover_color='#100d33', font=("PT Sans", 14), bg_color="#1F6AA5", border_width=1)
        self.filter_button_5.grid(row=2, column=0, columnspan=2, padx=(0,14), pady=(220,5), sticky="ne")
        
        if not self.info_text:
            self.info_text = ctk.CTkButton(self, width=200, height=150, corner_radius=10)
            self.info_text.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(10,0))
            # self.info_text.configure(bg_color="#1F6AA5", text_color="#F0F0F0", corner_radius=10, font=("PT Sans", 14))
        self.info_text.grid_remove()
    
    def save_files_to_drive(self):
        current_directory = os.getcwd()
        relative_folder_path = "doDrivea"
        folder_path = os.path.join(current_directory, relative_folder_path)
        for file_name in os.listdir(folder_path):
            full_file_path = os.path.join(folder_path, file_name)
            save_to_drive(full_file_path) 


    def start_noise_cancelling(self):

        CHUNK = 1024 #ilosc probek w 1 przebiegu
        WIDTH = 2 #bajty/probke (2=l.calkowite)
        CHANNELS = 2 #kanaly audio, 2 = stereo
        RATE = 44100 #probkowanie

        self.p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            filtered_data = self.apply_filter(audio_data, RATE)  # Zastosuj filtr LMS
            return (filtered_data.astype(np.int16).tobytes(), pyaudio.paContinue)


        self.stream = self.p.open(format=self.p.get_format_from_width(WIDTH),
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        output=True,
                        stream_callback=callback)

        self.stream.start_stream()

    def stop_noise_cancelling(self):
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()

    def set_filter_function(self, filter_function):
        self.filter_function = filter_function

    def butter_bandpass_filter_1(self, data, RATE): #mowa ludzka
        lowcut = 50.0
        highcut = 5000.0
        y_filtered = butter_bandstop_filter(data, lowcut, highcut, RATE, order=6)
        return y_filtered

    def butter_bandpass_filter_2(self, data, RATE): #ruch uliczny (heavy trucks)
        lowcut = 50.0
        highcut = 6000.0
        y_filtered = butter_bandstop_filter(data, lowcut, highcut, RATE, order=6)
        return y_filtered

    def butter_bandpass_filter_3(self, data, RATE): #odkurzacz
        lowcut = 200.0
        highcut = 10000.0
        y_filtered = butter_bandstop_filter(data, lowcut, highcut, RATE, order=6)
        return y_filtered
    
    def butter_bandpass_filter_4(self, data, RATE): #kosiarka
        lowcut = 3500.0
        highcut = 20000.0
        y_filtered = butter_bandpass_filter(data, lowcut, highcut, RATE, order=6)
        return y_filtered
    
    def butter_bandpass_filter_5(self, data, RATE): #szum wiatru
        lowcut = 50.0
        highcut = 20000.0
        y_filtered = butter_bandstop_filter(data, lowcut, highcut, RATE, order=6)
        return y_filtered

    def apply_filter(self, audio_data, RATE):
        return self.filter_function(audio_data, RATE)

        
    def auto_refresh(self):
        self.update_file_list()
        self.after(10000, self.auto_refresh)

    def hide_plot(self):
        if self.figure.axes:
            for ax in self.figure.axes:
                ax.remove()
            self.canvas.draw()

    def show_volume(self, event=None):
        if not hasattr(self, 'tooltip'):  
            self.tooltip = tk.Toplevel(self)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.configure(bg="#D4D4D4", padx=10, pady=5)  
            tk.Label(self.tooltip, text="Dźwięk", bg="#D4D4D4").pack()

        x, y, _, _ = self.volume_slider.bbox("insert")  
        x += self.volume_slider.winfo_rootx() + 20  
        y += self.volume_slider.winfo_rooty() + 20  
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.deiconify()

    def hide_volume(self, event=None):
        if hasattr(self, 'tooltip'):  
            self.tooltip.withdraw()


    def update_lowcut_value(self, value):
        self.lowcut = round(float(value))
        self.lowcut_scale.set(self.lowcut)
        self.lowcut_value_label.configure(text=f"{value}")


    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)  
        base_path = os.path.dirname(os.path.abspath(__file__))
        samples_path = os.path.join(base_path, "zapisane_probki")
        
        for file in os.listdir(samples_path):
            if file.endswith(".wav"):
                self.file_listbox.insert(tk.END, file)

    def play_selected_file(self, event):
        clicked_file = self.file_listbox.get(self.file_listbox.curselection())
        base_path = os.path.dirname(os.path.abspath(__file__))
        path_to_clicked_file = os.path.join(base_path, "zapisane_probki", clicked_file)
        
        pygame.mixer.music.load(path_to_clicked_file)
        pygame.mixer.music.play()

    def play_selected_file_with_progress(self, event):
        clicked_file = self.file_listbox.get(self.file_listbox.curselection())
        base_path = os.path.dirname(os.path.abspath(__file__))
        path_to_clicked_file = os.path.join(base_path, "zapisane_probki", clicked_file)
        
        pygame.mixer.music.load(path_to_clicked_file)
        pygame.mixer.music.play()
        self.hide_plot()
        
        duration_ms = pygame.mixer.Sound(path_to_clicked_file).get_length() * 1000
        self.progressbar["maximum"] = duration_ms
        self.progressbar["value"] = 0
        self.after(100, self.update_progressbar, duration_ms)

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

    def open_webpage_brownNoise(self, event):
        webbrowser.open("https://www.nytimes.com/interactive/2022/09/23/well/mind/brown-noise.html")

    def open_webpage_whiteNoise(self, event):
        webbrowser.open("https://en.wikipedia.org/wiki/White_noise")

    def open_webpage_pinkNoise(self, event):
        webbrowser.open("https://en.wikipedia.org/wiki/Pink_noise")
    
    def open_webpage_greenNoise(self, event):
        webbrowser.open("https://www.bettersleep.com/blog/benefits-of-green-noise/")
        

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
        self.info_text.configure(text="Kliknij tutaj aby uzyskać więcej informacji.", cursor="hand2")
        self.info_text.bind("<Button-1>", self.open_webpage_brownNoise)

    def menu_command_2(self):
        self.output_file = self.file_for_menu_2
        spectrum_path = self.file_for_menu_2_widmo
        imgWidmo = Image.open(spectrum_path)
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
        self.info_text.configure(text="Kliknij tutaj aby uzyskać więcej informacji.", cursor="hand2")
        self.info_text.bind("<Button-1>", self.open_webpage_whiteNoise)

    def menu_command_3(self):
        self.output_file = self.file_for_menu_3
        spectrum_path = self.file_for_menu_3_widmo
        imgWidmo = Image.open(spectrum_path)
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
        self.info_text.configure(text="Kliknij tutaj aby uzyskać więcej informacji.", cursor="hand2")
        self.info_text.bind("<Button-1>", self.open_webpage_pinkNoise)

    def menu_command_4(self):
        self.output_file = self.file_for_menu_4
        spectrum_path = self.file_for_menu_4_widmo
        imgWidmo = Image.open(spectrum_path)
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
        self.info_text.configure(text="Kliknij tutaj aby uzyskać więcej informacji.", cursor="hand2")
        self.info_text.bind("<Button-1>", self.open_webpage_greenNoise)

if __name__ == "__main__":
    app = Application()
    app.mainloop()