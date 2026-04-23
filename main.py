import speech_recognition as sr#This is our speech recognition library
import pyttsx3#This is our text to speech library
import sounddevice as sd
import numpy as np

def listen_command(duration):
    sample_rate = 44100
    samples = duration * sample_rate
    recording = sd.rec(int(samples), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    return recording

def speak_command(result):
    engine.say(result)
    engine.runAndWait()#This is the command to make the engine speak the result

def process_audio(recording):
    Audio_bytes = recording.tobytes()
    Audio_data = sr.AudioData(Audio_bytes, 44100, 2)
    r = sr.Recognizer()
    try:
        text = r.recognize_google(Audio_data)
    except sr.UnknownValueError:
        text = "Sorry, I didn't understand that."
    except Exception as e:
        text = f"An error occurred: {str(e)}"
    return text


if __name__ == "__main__":
    r = sr.Recognizer()#This is the basic command to recognize the speech and convert it into text
    engine = pyttsx3.init()#This initializezes our pytss3 which is a text-to-speech engine
