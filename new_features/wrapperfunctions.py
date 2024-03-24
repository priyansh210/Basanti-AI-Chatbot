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
    per = bsnti.person()
    props = {'name': n, 'year': y, 'phone': p}
    per.updateProperty(props)
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


def getAllPeople(P: bsnti.People):
    backendrequests.fetchAllPeopleData(P)
# message
def createMessage(
    M: bsnti.Messages,
    createdBy: str = "",
    createdFor: str = "",
    content: str = "",
):
    time = datetime.datetime.now()
    mess = bsnti.message()
    props = {'createdBy': createdBy, 'createdFor': createdFor, 'content': content, 'time': time}
    mess.updateProperty(props)
    query = backendrequests.addMessageToBackend(mess)
    query = query.json()
    print(query)
    id = query["id"]
    mess.addID(id)
    M.add_message(mess)

def getAllMessages(M: bsnti.Messages):
    backendrequests.getAllMessages(M)


def checkCurrentUserMessages(M: bsnti.Messages, currUser: str):
    user_messages = []
    for message in M.all_messages:
        for_list = [ x.lower() for x in message.properties["createdFor"]]
        if currUser.lower() in for_list:
            user_messages.append(message)
    # return user_messages, len(user_messages)
    num = len(user_messages)
    # print(f"You have {num} new message/s!")
    message_list = []
    message_list.append(f"You have {num} new message/s!")
    for message in user_messages:
        created_by = message.properties["createdBy"]
        content = message.properties["content"]

        if(created_by):
            one = f"From {created_by.capitalize()}: "
            # print(f"From {created_by.capitalize()}: ", end="")
        else:
            # print("From unkown: ", end="")
            one = "From unkown: "
        two = content
        # print(content)
        message_list.append(one+two)
    return message_list

#event
def createEvent(E: bsnti.Schedules, props: dict, ):
    event = bsnti.events()
    init_dict = {"createdFor": props["WHO"], "content": props["WHAT"],"timeOfCreation": datetime.datetime.now().isoformat(),"createdBy": props["createdBy"],"time":props["WHEN"].isoformat(), "venue":props["WHERE"]}
    event.updateProperty(init_dict)
    query = backendrequests.addEventToBackend(event)
    query = query.json()
    print(query)
    id = query['id']
    event.addID(id)
    E.add_event(event)

def getAllEvents(E:bsnti.Schedules):
    backendrequests.getAllEvents(E)

def checkCurrentUserEvents(E:bsnti.Schedules, currUser: str):
    user_events = []
    for event in E.all_events:
        for_list = [ x.lower() for x in event.properties["createdFor"]]
        if currUser.lower() in for_list:
            user_events.append(event)
    # return user_events, len(user_events)
    num = len(user_events)
    # print(f"You have {num} new event/s!")
    event_list = []
    event_list.append(f"You have {num} new event/s!")
    for event in user_events:
        created_by = event.properties["createdBy"]
        content = event.properties["content"]

        if(created_by):
            one = f"From {created_by.capitalize()}: "
            # print(f"From {created_by.capitalize()}: ", end="")
        else:
            # print("From unkown: ", end="")
            one = "From unkown: "
        two = content
        # print(content)
        event_list.append(one+two)
    return event_list

# inv_objects

def createInvObj(I: bsnti.Inventory, n: str = "", l: str = "", q: str = ""):

    obj = bsnti.inv_object()
    props = {'name': n, 'location': l, 'quantity': q}
    obj.updateProperty(props)
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