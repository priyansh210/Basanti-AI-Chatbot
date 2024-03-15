import translate as ts
import speech_recognition as sr


def listenHindi():

    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("Listening")
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language="hi-In")

            print("the query is printed='", Query, "'")

        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"

        print(Query)
        Query = ts.translate_hi_en(Query)
        return Query


def listenEnglish():

    r = sr.Recognizer()
    with sr.Microphone() as source:

        print("Listening")
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language="en")

            print("the query is printed='", Query, "'")

        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
        return Query
