import speak
import listen

import chatbot
import face_detection
import threading
from data import *
from new_features.wrapperfunctions import *

getAllMessages(MESSAGES)
getAllPeople(PEOPLE)
getAllEvents(SCHEDULES)


face_det = threading.Thread(target = face_detection.detect_face)

face_det.start()

def session():
    while True:
        per = face_detection.identified_person
        if per == '':
            continue

        per = per.split('_')
        per = per[0]
        print(per)
        chatbot.listen_state(per)
    #print('chat ended')

sess = threading.Thread(target=session)

sess.start()
# session(created_by:person)
# def session(created_by: str):
#     session_runing = True

#     chatbot.listen_state(created_by)
# sess.run()
# face_det.run()



    
# while True:
#     print(face_detection.identified_person)

