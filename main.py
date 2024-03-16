import sentence_breakdown as sb
import new_features.wrapperfunctions as wf #has the functions calling apis. Change baseURL in backendrequests to connect to correct database
import new_features.bsnti as bsnti #has the classes
import new_features.tele_bot as tele_bot

from sentence_breakdown import *
from listen import *

break_query = sb.break_querry

P = bsnti.People()
M = bsnti.Messages()
T = bsnti.Tasks()
S = bsnti.Schedules()
I = bsnti.Inventory()

# while True:
#     prompt = "send Priyansh a message to meet Herschelle" #add funtion here to get input

#     broken_query = break_query(prompt)

#     match broken_query['FUNCTION']:
#         case "ADD MESSAGE":
#             necessary_params = ["WHO", "WHAT"] #add where to prompt if message has to be sent
#             wf.checkNecessaryParams(broken_query, necessary_params)
#             wf.createMessage(M, broken_query)
#         case "SEND MESSAGE":
#             necessary_params = ["WHO", "WHAT"] #add where to prompt where message has to be sent, add more message sending stuff like emails
#             wf.checkNecessaryParams(broken_query, necessary_params)
#             tele_bot.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"])
#         case _:
#             #apologize and prompt again for the query
#             pass
#     break

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

    broken_query = break_querry(sentence)
    print(broken_query)

    match broken_query['FUNCTION'][1]:
        case "ADD MESSAGE":
            necessary_params = ["WHO", "WHAT"] #add where to prompt if message has to be sent
            wf.checkNecessaryParams(broken_query, necessary_params)
            wf.createMessage(M, broken_query)
        case "SEND MESSAGE":
            necessary_params = ["WHO", "WHAT"] #add where to prompt where message has to be sent, add more message sending stuff like emails
            wf.checkNecessaryParams(broken_query, necessary_params)
            tele_bot.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"])
        case _:
            #apologize and prompt again for the query
            pass
    break
    