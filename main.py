import speech_recognition as sr#This is our speech recognition library
import pyttsx3#This is our text to speech library


def speak_command(result):
    engine.say(result)
    engine.runAndwait()#This is the command to make the engine speak the result

if __name__ == "__main__":
    r = sr.Recognizer()#This is the basic command to recognize the speech and convert it into text
    engine = pyttsx3.init()#This initializezes our pytss3 which is a text-to-speech engine