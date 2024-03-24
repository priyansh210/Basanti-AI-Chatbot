import basanti as bsnti
import requests
import json
from typing import Union

baseURL = "http://192.168.212.20:8000"
#"http:/0.0.0.0/:8000"
#172.17.7.92
# person
# change functions to one function


def addPersonToBackend(p: bsnti.person):
    temp = {"properties": p.properties}
    query = requests.post(baseURL + "/people", json=temp)
    return query


def fetchAllPeopleData(P: bsnti.People):
    query = requests.get(baseURL + "/people")
    query = json.loads(query.content)
    for person in query["data"]:
        new_p = bsnti.person()
        for key, val in person["properties"].items():
            new_p.updateProperty(key, val)
        P.add_person(new_p)


def postPeopleData(P: bsnti.People):
    for p in P.all_persons:
        requests.post(baseURL + "/people", json={"properties": p.properties})


def updateDoc(obj: Union[bsnti.person, bsnti.message, bsnti.events], collection: str):
    payload = {"collection": collection, "id": obj.id, "properties": obj.properties}
    requests.post(baseURL + "/update", json=payload)
def getPersonByName(name):
    query = requests.get(baseURL + "/people/" + name)
    query  =json.loads(query.content)
    return query


# message


def addMessageToBackend(m: bsnti.message):
    temp = {"properties": m.properties}
    query = requests.post(baseURL + "/messages", json=temp)
    return query


def getAllMessages(M: bsnti.Messages):
    
    # req = req.json()
    # return req["data"]
    req = requests.get(baseURL + '/messages')
    query = json.loads(req.content)
    for mess in query["data"]:
        new_m = bsnti.message()
        propdict = {key: val for key, val in mess["properties"].items()}
        new_m.updateProperty(propdict)
        M.add_message(new_m)

# events

def getAllEvents(E: bsnti.Schedules):
    
    # req = req.json()
    # return req["data"]
    print("here")
    req = requests.get(baseURL + '/schedules')
    query = json.loads(req.content)
    for event in query["data"]:
        new_e = bsnti.events()
        propdict = {key: val for key, val in event["properties"].items()}
        new_e.updateProperty(propdict)
        E.add_event(new_e)

def addEventToBackend(e: bsnti.events):
    temp = {"properties": e.properties}
    query = requests.post(baseURL + "/schedules", json=temp)
    return query


# inventory objects


def addObjToBackend(o: bsnti.inv_object):
    temp = {"properties": o.properties}
    query = requests.post(baseURL + "/inventory", json=temp)
