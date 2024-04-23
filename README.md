# AudioSpectra
<p align="center"><img width=50.5% src="https://github.com/p4trykk/projekt_inz/blob/main/images/logo_app.png"></p>

AudioSpectra is a desktop application designed for the analysis, playback, and processing of audio files. The project was created as part of an engineering thesis by Patryk Klytta in Sielsian University of Technology to handle audio signals in the context of digital signal processing.

## Introduction

The AudioSpectra application allows you to:

- Play audio files in WAV and MP3 formats
- Analyze the frequency components of sound using spectrum plots
- Implement audio filters such as bandpass and notch filters
- Save processed audio files to Google Drive.

## ADHD and ADD characteristic

The AudioSpectra project focuses particularly on the subtype of ADHD known as ADD (Attention Deficit Disorder). It's worth noting that according to the current classification, ADHD terminology has undergone some changes in recent years. In the DSM-5 (Diagnostic and Statistical Manual of Mental Disorders), the term ADD has been replaced with the more detailed term Predominantly Inattentive Presentation, which refers to cases where a deficit in attention is the predominant symptom. While typical ADHD includes a spectrum of symptoms related to attention, impulsivity, and hyperactivity, ADD represents one variant of ADHD, primarily focusing on attention deficit.

Therapy for individuals with ADD often focuses on developing attention-focusing strategies, organization, and planning. People with ADD experience difficulties in maintaining attention on tasks, particularly those requiring planning and organization, which negatively affects their ability to work or learn effectively. In cases where hyperactivity is not the predominant problem, behavioral therapy and education can play a key role. The decision to focus on supporting individuals with ADD specifically arises from the need to consider differences in diagnosis and to tailor therapeutic approaches to their specific needs. Modification of sound stimulation may be directly related to improving the quality of life for individuals with ADD.

The use of sound, particularly ambient noise, has been studied as a potential tool to help individuals with attention deficits. Research suggests that certain types of background noise, such as white noise or nature sounds, can improve focus and attention in individuals with ADHD or ADD. These sounds can help mask distracting noises and create a more conducive environment for concentration.


## Requirements

To run the application, you'll need Python 3.x and the necessary libraries listed in the _requirements.txt_ file. You can install them using the following command:

```
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies.
4. Run the main.py file to start the application.

```
python main.py
```
## Features

- Playback: Easily play audio files with support for WAV and MP3 formats
- Spectrum Analysis: Visualize the frequency components of audio signals using spectrum plots
- Filter Implementation: Apply various audio filters, including bandpass and notch filters, to modify audio signals
- Cloud Integration: Save processed audio files securely to Google Drive for easy access and sharing.

![Screenshot of the main screen app.](https://github.com/p4trykk/projekt_inz/blob/main/images/main_screen2.png)

## Application Structure

The AudioSpectra application follows a modular structure, with key components including:

### Graphical User Interface (GUI)
The GUI provides an intuitive interface for users to interact with the application. It includes buttons for playback control, spectrum analysis plots, and filter selection.

```python
# Example code snippet for GUI initialization
def create_widgets(self):
```

### Audio Playback
The application supports playback of audio files in WAV and MP3 formats using the _pygame.mixer_ module.
```python
def play_selected_file(self, event):
    # Load selected file
    # Play audio using pygame.mixer
```

### Spectrum Analysis
Spectrum analysis allows users to visualize the frequency components of audio signals using matplotlib.
```python
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    # Design filter coefficients
    # Apply filter to input data
```
<img src="https://github.com/p4trykk/projekt_inz/blob/main/images/film_instrukta_Patryk_Klytta-ezgif.com-crop.gif" width=100%>

### Google Drive API
The integration with Google Drive and its API enhances the functionality of the AudioSpectra application by providing users with seamless access to cloud storage and collaboration features. By leveraging the Google Drive API, users can easily save and retrieve audio files directly from their Google Drive accounts, facilitating convenient storage and sharing of data.

The integration with Google Drive offers several benefits:
- Data Backup and Synchronization: Users can securely store their audio recordings and analysis results in Google Drive, ensuring data integrity and accessibility across multiple devices. This feature provides peace of mind by offering automatic backup and synchronization of files.
- Collaborative Workflows: The collaborative features of Google Drive enable users to share audio files and analysis reports with collaborators or team members. This fosters collaboration and enables real-time feedback and discussion on audio projects.
- Integration with Other Google Services: The integration with Google Drive complements other Google services, such as Google Docs, Sheets, and Slides. Users can easily incorporate audio files into their documents, presentations, or spreadsheets, enhancing the richness of their content.

Overall, the integration with Google Drive enhances the functionality and versatility of the AudioSpectra application, empowering users to manage their audio projects more effectively and collaborate seamlessly with others.
  

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.


## License

This project is licensed under the [MIT License](https://www.mit.edu/~amini/LICENSE.md).

art. 74 ust. 1 Ustawa o prawie autorskim i prawach pokrewnych, [Zakres ochrony programów komputerowych](https://lexlege.pl/ustawa-o-prawie-autorskim-i-prawach-pokrewnych/art-74/)




