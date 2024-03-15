from sentence_breakdown import *
from listen import *


while 1:
    ans = input("Do you want to ask a question y/n : ")
    if ans in "nN":
        break

    sentence = listenEnglish()

    # que = sr_eng.speech_rec()
    # que = json.loads(que)
    # sentence = que["text"]

    print(sentence)

    # sentence = "tell priyansh to that the meeting is scheduled on 20 jan 5 in the evening  "

    data = break_querry(sentence)
    print(data)
