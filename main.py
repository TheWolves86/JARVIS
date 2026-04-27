import speech_recognition as sr#This is our speech recognition library
import pyttsx3#This is our text to speech library
import sounddevice as sd
import numpy as np
import time
from dotenv import load_dotenv
import os
import requests
import queue
import threading

stop_program = False

def handle_command(text):#It's a sample brain for now
    text = text.lower()
    if 'hello' in text:
        return "How r u"
    elif 'open' in text:
        return "I cant do that yet"
    elif 'explain' in text:
        return "I dont have my brain yet"
    elif "stop" in text:
        return ""
    else:
        return "wait and put my brain"



def listen_command(duration):#This command will listen to you
    sample_rate = 44100
    samples = duration * sample_rate#This is formula to claculate the number of smaples
    recording = sd.rec(int(samples), samplerate=sample_rate, channels=1, dtype='int16')#this is the command to record
    sd.wait()#Use this as it is necessary
    return recording



def speak_command(result):#Instead of using pyttsx3,i used windows powershell as pyttsx3 was buggy and not working
    result = result.replace('"', '')
    os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{result}\');"')#This is a command that i had to take from chatgpt.

def process_audio(recording):#This is the the used to process the audio to convert it into text
    Audio_bytes = recording.tobytes()#This is used to convert into bytes
    Audio_data = sr.AudioData(Audio_bytes, 44100, 2)#This is also necessary as it creates audio data
    try:#We used this as sometimes it may not understand what we said and give us an error
        text = r.recognize_google(Audio_data)
    except sr.UnknownValueError:
        text = "Sorry, I didn't understand that."
    except Exception as e:
        text = f"An error occurred: {str(e)}"
    return text


if __name__ == "__main__": 
    r = sr.Recognizer()#This is the basic command to recognize the speech and convert it into text
    #This initializezes our pytss3 which is a text-to-speech engine
    print("Listening for a clap...")
    threshold = 10000
    clap_count = 0
    last_clap_time = 0
    while True:
        start_func = listen_command(1)
        loudness = np.max(np.abs(start_func))#It counts the loudness of ur clap
        if loudness > threshold:
            current_time = time.time()#We are using this time things and many more bcs we need 2 claps
            if current_time - last_clap_time > 1:
                clap_count += 1
            else:
                clap_count = 1
            last_clap_time = current_time
            if clap_count == 2:
                print("Initializing JARVIS")
                while True:
                    speech_started = False
                    silent_chunks = 0
                    chunks = []#As pyAudio is not available we are using numPy arrays for speech recognitiom
                    while True:
                        chunk = listen_command(0.25)
                        loudness = np.max(np.abs(chunk))

                        if loudness > 6000:#We are keeping this 6000 as without it continue without a human voice
                            if not speech_started:
                                print("Speech Started")
                                speech_started = True
                            silent_chunks = 0
                            chunks.append(chunk)
                        elif speech_started:
                            silent_chunks += 1
                            if silent_chunks > 5:#If it is going to early,You can change it to 8
                                print("speech ended")
                                break
                    if len(chunks) == 0:
                        continue
                    full_audio = np.concatenate(chunks)#It add all the chunks in one string
                    text = ""
                    text = process_audio(full_audio)
                    response = handle_command(text)
                    print(f"You said: {text}")
                    print(response)
                    speak_command(response)
                    time.sleep(0.25)
                    if 'stop' in text.lower():
                        print("Bye")
                        clap_count = 0
                        stop_program = True
                        break
                
                if stop_program == True:
                    break
                                      