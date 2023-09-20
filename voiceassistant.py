import re
import pyttsx3
import speech_recognition as sr

class TTS_Engine:
    def __init__(self, rate=120, voice="english"):
        self.engine = pyttsx3.init()
        self.set_rate(rate)
        self.set_voice(voice)

    def set_rate(self, rate):
        self.engine.setProperty("rate", rate)

    def set_voice(self, voice):
        voices = self.engine.getProperty('voices')
        for v in voices:
            if v.languages and voice in v.languages[0]:
                self.engine.setProperty('voice', v.id)
                return
        print(f"Voice {voice} not found, using default.")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

def listen(mic):
    r = sr.Recognizer()
    with mic as source:
        print("You can talk now?")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            return r.recognize_google(audio)
        except Exception as e:
            print("Error:", e)
            return None

def extract_name(text):
    reg = re.search("my name is ([A-Za-z]+)", text)
    return reg.group(1) if reg else None

def extract_old(text):
    reg = re.search("(\d+) years old", text)
    return reg.group(1) if reg else None

def main():
    tts = TTS_Engine()
    mic = sr.Microphone(device_index=1)

    tts.speak("Hi, how are you? What's your name?")
    response = listen(mic)
    if response:
        print(response)
        name = extract_name(response)
        if "good" in response.lower() and name:
            tts.speak(f"That's good to hear {name}, nice to meet you.")
        elif name:
            tts.speak(f"Hope things get better for you {name}.")

    tts.speak("How old are you?")
    response = listen(mic)
    if response:
        print(response)
        years_old = extract_old(response)
        if years_old:
            years_old = int(years_old)
            if years_old < 40:
                tts.speak(f"That's a good age, you are young {name}.")
            else:
                tts.speak(f"Oh.. {years_old} years old, so you are a veteran now haha.")
        else:
            tts.speak("Sorry, I didn't catch your age.")

if __name__ == "__main__":
    main()

