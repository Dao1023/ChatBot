import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('voice', 'zh')
    engine.say(text)
    engine.runAndWait()
