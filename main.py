import speech_recognition as sr#This is our speech recognition library
import pyttsx3#This is our text to speech library
import sounddevice as sd#This library is used in place of pyaudio
import numpy as np#Used for its array
import time#We need it for many things
from dotenv import load_dotenv#So my api dont get leaked ofc
import os
import threading
import requests
import webbrowser as wb
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

stop_program = False
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def handle_command(text):
    text = text.lower()
    if "open youtube" in text:
        return "open_youtube"
    if "Sorry, I didn't understand that." == text:
        return "soryy, we didnt understand what u said"
    if len(text.split()) < 3:
        return "ignore"
    if any(word in text for word in ["what", "why", "how", "explain", "who"]):
        return "ai"
    
    return "small_talk"


def listen_command(duration):#This command will listen to you
    sample_rate = 44100
    samples = duration * sample_rate#This is formula to claculate the number of smaples
    recording = sd.rec(int(samples), samplerate=sample_rate, channels=1, dtype='int16')#this is the command to record
    sd.wait()#Use this as it is necessary
    return recording



def speak_command(result):#Instead of using pyttsx3,i used windows powershell as pyttsx3 was buggy and not working
    result = result.replace('"', '')
    result = result.replace("'", "") 
    os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{result}\');"')#This is a command that i had to take from chatgpt.

def process_audio(recording):#This is the the used to process the audio to convert it into text
    recording = recording.astype(np.int16)
    Audio_bytes = recording.tobytes()#This is used to convert into bytes
    Audio_data = sr.AudioData(Audio_bytes, 44100, 2)#This is also necessary as it creates audio data
    try:#We used this as sometimes it may not understand what we said and give us an error
        text = r.recognize_google(Audio_data)
    except sr.UnknownValueError:
        text = None
    except Exception as e:
        text = None
    return text

def ask_ai(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")

    try:
        response = model.generate_content(
            f"""
            You are Jarvis:
            - Short answers
            - Human-like

            User: {prompt}
            """
        )
        return response.text or "No response."

    except ResourceExhausted:
        return "Sir, my AI limit is reached. Please wait a bit."

    except Exception as e:
        print(e)
        return "Something went wrong."

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
                        chunk = listen_command(0.10)
                        loudness = np.max(np.abs(chunk))

                        if loudness > 6500:#We are keeping this 6500 as without it continue without a human voice
                            if not speech_started:
                                print("Speech Started")
                                speech_started = True
                            silent_chunks = 0
                            chunks.append(chunk)
                        elif speech_started:
                            silent_chunks += 1
                            chunks.append(chunk)
                            if silent_chunks > 3:#If it is going to early,You can change it to 5
                                print("speech ended")
                                break
                    if len(chunks) == 0:
                        continue
                    full_audio = np.concatenate(chunks)#It add all the chunks in one string
                    text = ""
                    text = process_audio(full_audio)
                    if not text:
                        print("Skipping noise...")
                        continue
                    response = handle_command(text)
                    print(f"You said: {text}")
                    if 'stop' in text.lower():
                        print("Bye")
                        clap_count = 0
                        stop_program = True
                        break
                    if response == "open_youtube":
                        wb.open("https://www.youtube.com/")
                    elif response == "ai":
                        result = ask_ai(text)
                        print(result)
                        threading.Thread(target=speak_command, args=(result,), daemon=True).start()
                    elif response == "small_talk":
                        response = "I'm still learning that."
                        speak_command(response)
                    elif response == "ignore":
                        continue
                    else:
                        print(result)
                        speak_command(result)
                if stop_program == True:
                    break