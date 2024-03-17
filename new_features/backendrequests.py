import basanti as bsnti
import requests
import json
from typing import Union

baseURL = "http://172.17.7.92:8000"

# person
# change functions to one function


def addPersonToBackend(p: bsnti.person):
    temp = {"properties": p.properties}
    query = requests.post(baseURL + "/people", json=temp)
    return query


def fetchAllPeopleData(P: bsnti.People):
    query = requests.get(baseURL + "/people")
    query = json.loads(query.content)
    query = query["data"][1]["_id"]["$oid"]
    print(query)


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


# events


def addEventToBackend(e: bsnti.events):
    temp = {"properties": e.properties}
    query = requests.post(baseURL + "/messages", json=temp)
    return query


# inventory objects


def addObjToBackend(o: bsnti.inv_object):
    temp = {"properties": o.properties}
    query = requests.post(baseURL + "/inventory", json=temp)
