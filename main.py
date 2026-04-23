import speech_recognition as sr#This is our speech recognition library
import pyttsx3#This is our text to speech library
import sounddevice as sd
import numpy as np
import time

stop_program = False

def listen_command(duration):#This command will listen to you
    sample_rate = 44100
    samples = duration * sample_rate#This is formula to claculate the number of smaples
    recording = sd.rec(int(samples), samplerate=sample_rate, channels=1, dtype='int16')#this is the command to record
    sd.wait()#Use this as it is necessary
    return recording

def speak_command(result):
    engine.say(result)
    engine.runAndWait()#This is the command to make the engine speak the result

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
    engine = pyttsx3.init()#This initializezes our pytss3 which is a text-to-speech engine
    print("Listening for a clap...")
    threshold = 10000
    clap_count = 0
    last_clap_time = 0
    while True:
        start_func = listen_command(1)
        loudness = np.max(np.abs(start_func))
        if loudness > threshold:
            current_time = time.time()
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
                    chunks = []
                    while True:
                        chunk = listen_command(0.3)
                        loudness = np.max(np.abs(chunk))
                        if loudness > 4000:
                            print("speech detected")
                            speech_started = True
                            silent_chunks = 0
                            chunks.append(chunk)
                        else:
                            if speech_started:
                                silent_chunks += 1
                                chunks.append(chunk)

                                if silent_chunks > 8:
                                    print("Speech ended")
                                    
                                    break
                    if len(chunks) == 0:
                        continue
                    full_audio = np.concatenate(chunks)
                    recording = full_audio
                    text = process_audio(recording)
                    print(f"You said: {text}")
                    if 'stop' in text.lower():
                        print("Bye!")
                        clap_count = 0
                        stop_program = True
                        break
                if stop_program == True:
                    break
                