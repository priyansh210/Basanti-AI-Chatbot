import translate as ts


import speech_recognition as sr


from extract_info import *


def takeCommandHindi():

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


def takeCommandEnglish():

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


while 1:
    ans = input("Do you want to ask a question y/n : ")
    if ans in "nN":
        break

    sentence = takeCommandEnglish()

    # que = sr_eng.speech_rec()
    # que = json.loads(que)
    # sentence = que["text"]

    print(sentence)

    # sentence = "tell priyansh to that the meeting is scheduled on 20 jan 5 in the evening  "

    data = extract_info("priyansh", sentence)
    print(data)
