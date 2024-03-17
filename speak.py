import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
newVoiceRate = 175
engine.setProperty("rate", newVoiceRate)
print(voices)


def speakEnglish(command):
    # Initialize the engine
    print(command)
    engine.say(command)
    engine.runAndWait()
