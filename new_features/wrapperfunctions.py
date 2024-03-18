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
# def createEvent(
#     S: bsnti.Schedules,
#     broken_query: dict
# ):
#     event = bsnti.events(broken_query.cb, cf, co, t.isoformat(), Time.isoformat(), Venue)
#     query = backendrequests.addEventToBackend(event)
#     query = query.json()
#     id = query["id"]
#     event.addID(id)
#     S.add_event(event)
def createEvent(E: bsnti.Schedules, props: dict):
    event = bsnti.events("", props["WHO"],props["WHAT"], datetime.datetime.now().isoformat() ,props["WHEN"].isoformat(), props["WHERE"])
    query = backendrequests.addEventToBackend(event)
    query = query.json()
    print(query)
    id = query['id']
    event.addID(id)
    E.add_event(event)


# inv_objects


def createInvObj(I: bsnti.Inventory, n: str = "", l: str = "", q: str = ""):

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
                answer = None
                while answer is None:
                    question = "Who do I " + broken_query["ACTION"] + " for?"
                    speak.speakEnglish(question)
                    answer = listen.listenEnglish()
                answer = get_target(answer)
                print(answer)
                broken_query["WHO"] = answer

            elif el == "WHEN":
                answer = None
                while answer is None:
                    question = "When do I " + broken_query["ACTION"]
                    speak.speakEnglish(question)
                    answer = listen.listenEnglish()
                # print(question)
                # speak.speakEnglish(question)
                # answer = listen.listenEnglish()
                answer = get_when(answer)
                broken_query["WHEN"] = answer

            elif el == "WHERE":
                answer = None
                while answer is None:
                    question = "Where do I " + broken_query["ACTION"]
                    speak.speakEnglish(question)
                    answer = listen.listenEnglish()
                # question = "When do I " + broken_query["ACTION"]
                # print(question)
                # speak.speakEnglish(question)
                # answer = listen.listenEnglish()
                broken_query["WHERE"] = answer

            elif el == "WHAT":
                answer = None
                while answer is None:
                    question = "What do I " + broken_query["ACTION"]
                    speak.speakEnglish(question)
                    answer = listen.listenEnglish()
                # print(question)
                # speak.speakEnglish(question)
                # answer = listen.listenEnglish()
                broken_query["WHAT"] = answer

            # prompt here for the param and add it to the broken_query
            pass

    return broken_query
def createPersonContext(name):
    res = backendrequests.getPersonByName(name)
    data = res["data"]["properties"]
    context = ""
    for key, value in data.items():
        context += str(key) + ': '+ str(value) +'\n'
    return context[:-1]