import new_features.backendrequests as backendrequests
import basanti as bsnti
import json
import datetime
import speak
import listen
from sentence_breakdown import *

"""structure of objects:
    {
        'collection': '', ex: messages, tasks, schedules, people
        'id': '', the id of the object
        'properties': {}, dictionary of properties
    }
"""


def QuestionForMissingParameter(param: str):
    # basanti asks for the parameter
    return  # parameter value


# person
def createPerson(P: bsnti.People, n: str, y: str, p: str):
    per = bsnti.person(n, y, p)
    query = backendrequests.addPersonToBackend(per)
    query = query.json()
    print(query)
    id = query["id"]
    per.addID(id)
    P.add_person(per)


def delPerson(P: bsnti.People, prop: str, val: str):
    for p in P.all_persons:
        if p.properties[prop] == val:
            P.remove_person_by_prop(prop, val)


# message
def createMessage(
    M: bsnti.Messages,
    cb: str = "",
    cf: str = "",
    co: str = "",
    t: datetime.datetime = "",
):
    if cb == "":
        cb = QuestionForMissingParameter("created by")
    if cf == "":
        cf = QuestionForMissingParameter("created for")
    if co == "":
        co = QuestionForMissingParameter("content")
    if t == "":
        t = QuestionForMissingParameter("time")

    mess = bsnti.message(cb, cf, co, t.isoformat())
    query = backendrequests.addMessageToBackend(mess)
    query = query.json()
    print(query)
    id = query["id"]
    mess.addID(id)
    M.add_message(mess)


# def createMessage(M:bsnti.Messages, props:dict):

#     mess = bsnti.message("",props['WHO'],props['WHAT'],props['WHEN'].isoformat())
#     query = backendrequests.addMessageToBackend(mess)
#     query = query.json()
#     print(query)
#     id = query['id']
#     mess.addID(id)
#     M.add_message(mess)


# events
def createEvent(
    S: bsnti.Schedules,
    cb: str = "",
    cf: str = "",
    co: str = "",
    t: datetime.datetime = "",
    Time: datetime.datetime = "",
    Venue: str = "",
):
    if cb == "":
        cb = QuestionForMissingParameter("created by")
    if cf == "":
        cf = QuestionForMissingParameter("created for")
    if co == "":
        co = QuestionForMissingParameter("content")
    if t == "":
        t = QuestionForMissingParameter("time created")
    if Time == "":
        Time = QuestionForMissingParameter("Time of Event")
    if Venue == "":
        Venue = QuestionForMissingParameter("Venue")

    event = bsnti.events(cb, cf, co, t.isoformat(), Time.isoformat(), Venue)
    query = backendrequests.addEventToBackend(event)
    query = query.json()
    id = query["id"]
    event.addID(id)
    S.add_event(event)


# inv_objects


def createInvObj(I: bsnti.Inventory, n: str = "", l: str = "", q: str = ""):
    if n == "":
        n = QuestionForMissingParameter("name of object")
    if l == "":
        l = QuestionForMissingParameter("location")
    if q == "":
        q == QuestionForMissingParameter("quantity")

    obj = bsnti.inv_object(n, l, q)
    query = backendrequests.addObjToBackend(obj)
    query = query.json()
    id = query["id"]
    obj.addID(id)
    I.add_item(obj)


# check function for necessary params returned from query breaker


def checkNecessaryParams(broken_query: dict, necessary_params: list):
    for el in necessary_params:
        if broken_query[el] == None:
            if el == "WHO":
                question = "Who do I " + broken_query["ACTION"] + " for?"
                print(question)
                speak.speakEnglish(question)
                answer = listen.listenEnglish()
                answer = get_target(answer)
                broken_query["WHO"] = answer

            elif el == "WHEN":
                question = "When do I " + broken_query["ACTION"]
                print(question)
                speak.speakEnglish(question)
                answer = listen.listenEnglish()
                answer = get_when(answer)
                broken_query["WHEN"] = answer

            elif el == "WHERE":
                question = "Where do I " + broken_query["ACTION"]
                print(question)
                speak.speakEnglish(question)
                answer = listen.listenEnglish()
                broken_query["WHERE"] = answer

            elif el == "WHAT":
                question = "What do I " + broken_query["ACTION"]
                print(question)
                speak.speakEnglish(question)
                answer = listen.listenEnglish()
                broken_query["WHAT"] = answer

            # prompt here for the param and add it to the broken_query
            pass

    return broken_query
