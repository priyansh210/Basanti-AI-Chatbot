import sentence_breakdown as sb
import new_features.wrapperfunctions as wf  # has the functions calling apis. Change baseURL in backendrequests to connect to correct database
from basanti import *
from sentence_breakdown import *
from listen import *
import new_features.telegram as telegram
import speak

break_query = sb.break_querry

from data import MESSAGES, SCHEDULES


def action_bot(created_by):

    print("Do you want to ask any questions")
    sentence = listenEnglish()
    print(sentence)
    if not sentence:
        return
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

        speak.speakEnglish(reconfirmAction)
        # conditions

        telegram.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"])
    
    elif action ==  "ADD TO SCHEDULE":
        necessary_params = ["WHO", "WHAT", "WHERE",  "WHEN"] #add where to prompt if message has to be sent
        broken_query = wf.checkNecessaryParams(broken_query, necessary_params)
        msg = broken_query["WHAT"]+" "+broken_query["WHEN"].isoformat()+" "+broken_query["WHERE"]
        print(msg)
        telegram.sendTelegramMessage(broken_query["WHO"], broken_query["WHAT"]+" "+broken_query["WHEN"].isoformat()+" "+broken_query["WHERE"])
        wf.createEvent(SCHEDULES, broken_query)

    else:
        speak.speakEnglish("Sorry could you please repeat your querry")
        pass
