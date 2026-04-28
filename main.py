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
import subprocess

import subprocess

_ps = subprocess.Popen(
    [
        'powershell', '-NoProfile', '-NonInteractive', '-Command',
        'Add-Type -AssemblyName System.Speech; '
        '$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        'while($true){ '
        '$t = [Console]::ReadLine(); '
        'if($t -eq "EXIT"){break}; '
        '$s.SpeakAsync($t); '
        'while($s.State -eq "Speaking"){ Start-Sleep -Milliseconds 50 }; '
        'Write-Output "DONE" '
        '}'
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.DEVNULL
)#I got this command from chat gpt as i am a begginer

stop_program = False
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def handle_command(text):#We are not doing all the things in our function to increase speed and readability
    text = text.lower()
    if "open youtube" in text:
        return "open_youtube"
    if "Sorry, I didn't understand that." == text:
        return "soryy, we didnt understand what u said"
    if len(text.split()) < 3:
        return "ignore"
    if any(word in text for word in ["what", "why", "how", "explain", "who"]):#We will use ai for these as api credits are expensive lol
        return "ai"
    
    return "small_talk"


def listen_command(duration):#This command will listen to you
    sample_rate = 44100
    samples = duration * sample_rate#This is formula to claculate the number of smaples
    recording = sd.rec(int(samples), samplerate=sample_rate, channels=1, dtype='int16')#this is the command to record
    sd.wait()#Use this as it is necessary
    return recording



def speak_command(text):#Instead of using pyttsx3,i used windows powershell as pyttsx3 was buggy and not working
    text = text.replace('"', '').replace("'", "").replace('\n', ' ').strip()#tbh also had to use some chatgpt as windows powershell is scary
    if not text:
        return
    print(f"JARVIS: {text}")
    _ps.stdin.write((text + '\n').encode('utf-8'))
    _ps.stdin.flush()
    _ps.stdout.readline()

def capture_command():#Idk if you know this or not but this is the hardest part
    sample_rate = 16000
    block_size = 800
    timeout = 0
    speech_started = False
    silent_chunks = 0
    chunks = []

    def callback(indata, frames, time_info, status):#I know these look scary but we dont have pyaudio
        nonlocal speech_started,silent_chunks,chunks

        loudness = np.max(np.abs(indata))
        if loudness > 6500:#I put this 6500 but if it cant catch ur voice,you can also put 2500 or whatever is working
            if speech_started == False:
                print("🎤 Listening...")
                speech_started = True

            silent_chunks = 0
            chunks.append(indata.copy())
        else:
            if speech_started == True:
                silent_chunks += 1
                chunks.append(indata.copy())
    stream = sd.InputStream(
        samplerate = sample_rate, 
        channels=1,
        dtype = 'int16',
        blocksize=block_size,
        callback=callback
    )
    stream.start()
    while True:
        sd.sleep(50)
        timeout += 50

        if speech_started == True and silent_chunks > 12:
            print("✅ Got it!")
            break
        if not speech_started and timeout > 8000:
            break

    stream.stop()
    stream.close()

    if len(chunks) == 0:
        return None

    full_audio = np.concatenate(chunks)
    if len(chunks) < 5:
        return None
    return full_audio


def process_audio(recording):#This is the the used to process the audio to convert it into text
    recording = recording.astype(np.int16)
    Audio_bytes = recording.tobytes()#This is used to convert into bytes
    Audio_data = sr.AudioData(Audio_bytes, 16000, 2)#This is also necessary as it creates audio data
    try:#We used this as sometimes it may not understand what we said and give us an error
        text = r.recognize_google(Audio_data)
    except sr.UnknownValueError:
        text = None
    except Exception as e:
        text = None
    return text

def ask_ai(prompt):#I dont think i have to explain this.
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
    r = sr.Recognizer()
    print("=" * 40)
    print("  JARVIS - Voice Agent")
    print("  Say 'Jarvis' to wake up")
    print("  Say 'stop' or 'shutdown' to exit")
    print("=" * 40)
    speak_command("JARVIS online. Say Jarvis to activate me.")
    while True:
        print("[StandBY] Say JARVIS.....")
        audio = capture_command()#Captures our JARVIS command to wake hismelf up
        if audio is None:
            continue
        wake_text = process_audio(audio)
        if not wake_text or "jarvis" not in wake_text.lower():
            continue
        print("JARVIS Activated")
        speak_command("Yes Sir!")
        while True:
            command_audio = capture_command()
            if command_audio is None:
                continue
            command_text = process_audio(command_audio)
            if not command_text:#It will do this if it cant understand what u said
                print("Sorry,Kindly say again")
                continue
            print(f"You said: {command_text}")
            if 'stop' in command_text.lower():
                print("Goodbye Sir")
                _ps.stdin.write(b"EXIT\n")#Closes the powershell
                _ps.stdin.flush()
                exit()

            action = handle_command(command_text)
            if action == "open_youtube":
                wb.open("https://www.youtube.com/")
            elif action == "ai":
                response = ask_ai(command_text)
                print(response)
                speak_command(response)
            elif action == "small_talk":
                print("I am still learning that")
                speak_command("I am still learning that")