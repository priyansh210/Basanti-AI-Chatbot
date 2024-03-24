import sentence_breakdown as sb
import new_features.wrapperfunctions as wf  # has the functions calling apis. Change baseURL in backendrequests to connect to correct database
from basanti import *
from sentence_breakdown import *
from listen import *
import speak
from intent_classifier import *
import requests
  
break_query = sb.break_querry

from data import MESSAGES, SCHEDULES, PEOPLE
import new_features.telegram as telegram


def listen_state(created_by):
    while True: 
        sentence = listenEnglish()
        # speak.speakEnglish("Do you want to ask any questions")
        # print('here1')
        
        # print('here2')
        print(sentence)
        if not sentence:
            continue
        intent, confidence = predict_sentiment(sentence)
        print(intent)
        if intent == 'Question':
            question_bot(created_by, sentence)
        elif intent == 'Action':
            action_bot(created_by, sentence)
        

def action_bot(created_by, sentence):

    broken_query = break_querry(sentence)
    broken_query["CREATED_BY"] = created_by

    action = broken_query["FUNCTION"][1]

    if action == "ADD MESSAGE":

        necessary_params = [
            "WHO",
            "WHAT",
        ]

        broken_query = wf.checkNecessaryParams(broken_query, necessary_params)

        wf.createMessage(MESSAGES, broken_query)

    elif action == "SEND MESSAGE":

        necessary_params = [
            "WHO",
            "WHAT",
        ]

        broken_query = wf.checkNecessaryParams(broken_query, necessary_params)

        # reconfirm action
        reconfirmAction = (
            "I am going to send a message to "
            + " ".join(broken_query["WHO"])
            + " about "
            + broken_query["WHAT"]
        )

        # speak.speakEnglish(reconfirmAction)
        # conditions
    
        telegram.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"])

    elif action == "GET MESSAGE":
        message_list = wf.checkCurrentUserMessages(MESSAGES, created_by)
        for msg in message_list:
            speak.speakEnglish(msg)
    
    elif action ==  "ADD TO SCHEDULE":
        necessary_params = ["WHO", "WHAT", "WHERE",  "WHEN"] #add where to prompt if message has to be sent
        broken_query = wf.checkNecessaryParams(broken_query, necessary_params)
        msg = broken_query["WHAT"]+" "+broken_query["WHEN"].isoformat()+" "+broken_query["WHERE"]
        print(msg)
        telegram.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"]+" "+broken_query["WHEN"].isoformat()+" "+broken_query["WHERE"])
        broken_query["createdBy"] = created_by

    elif action == "GET SCHEDULE":
        event_list = wf.checkCurrentUserEvents(SCHEDULES, created_by)
        for event in event_list:
            speak.speakEnglish(event)


    else:
        speak.speakEnglish("Sorry could you please repeat your querry")
        pass

def question_bot(created_by, question:str):
    print("hi")
    chatURL = "https://positively-primary-stallion.ngrok-free.app/"
    question = {"ques": question}
    answer = requests.post(chatURL, params = question)
    answer = answer.json()
    print(answer["message"])
    answer:str = answer["message"]
    speak.speakEnglish(answer.replace('\n', " "))

listen_state('aswin')