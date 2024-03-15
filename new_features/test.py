import bsnti
import requests
import wrapperfunctions
import datetime

P = bsnti.People()
M = bsnti.Messages()
T = bsnti.Tasks()
S = bsnti.Schedules()
I = bsnti.Inventory()

#backendrequests.fetchAllPeopleData(P)

P = bsnti.People()

# wrapperfunctions.addPerson(P, "aswin", "2nd", "3456789")
# print(P.all_persons[0].id)

wrapperfunctions.createEvent(S, "aswin", "", "Beeg Event 3000", datetime.datetime.now(), datetime.datetime(2024, 3, 20), "Raman Lab")

print(S.all_events[0].properties)

