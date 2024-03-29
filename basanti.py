import datetime
 #change code so that all classes except the ones with lists inherit from the template class.
#No need to initialize the properties, just keep it an empty dictionary
#Make methods to add properties using the inherited funcitions

class TemplateClass:
    def __init__(self) -> None:
        self.properties = {
            # "createdBy": created_by,
            # "createdFor": created_for,
            # "content": content,
            # "createdAt": t,
            # for mongo, it returns id automatically which will be used to set the id. To be changed when database is shifted
            # the id returned by mongo will be added as an id field
        }

    def addID(self, id):
        self.id = (
            id  # made to add id to object after pushing to mongo and recieving its id
        )

    def updateProperty(self, propDict: dict):
        self.properties.update(propDict)
        # for key, value in propDict.items():
        #     self.properties[key] = value

    def deleteProperty(self, key):
        self.properties.pop(key)

    def getProperty(self, key):
        return self.properties[key]


class task(TemplateClass):
    def __init__(self) -> None:
        super().__init__()

class message(TemplateClass):
    def __init__(
        self
        # created_by: person,
        # created_for: list[person],
        # content: str,
        # t: datetime.datetime,
    ) -> None:
        super().__init__()

class events(TemplateClass):
    def __init__(self) -> None:
        super().__init__()
        # name of event stored in content
        # make this better by changing update property to take in a dictionary

class person(TemplateClass):
    def __init__(self) -> None:
        super().__init__()
        #name
        #year
        #phone
        #chat id

class inv_object(TemplateClass):
    def __init__() -> None:
        super().__init__()
        #name
        #quantity
        #location

class Messages:
    def __init__(self) -> None:
        self.all_messages: list[message] = []

    def add_message(self, msg):
        self.all_messages.append(msg)

    def remove_message(self, id):
        for el in self.all_messages:
            if el.id == id:
                self.all_messages.remove(el)

    def get_message_person(self, person: person):
        return [
            msg
            for msg in self.all_messages
            if person.properties["name"] in msg.properties["createdFor"]
        ]

class People:
    def __init__(self, p: list[person] = []) -> None:
        self.all_persons = p

    def add_person(self, person):
        self.all_persons.append(person)

    def remove_person_by_id(self, id):
        for el in self.all_persons:
            if el.id == id:
                self.all_persons.remove(el)

    def remove_person_by_prop(self, prop, val):
        for el in self.all_persons:
            if el.properties[prop] == val:
                self.all_persons.remove(el)

    def get_person_by_prop(self, prop, val):
        for el in self.all_persons:
            if el.properties[prop] == val:
                return el


"""
    People Object in mongo looks like:
        P = {
            '_id': {'$oid': 'id_value'}, 'properties': {all properties}
        }
"""


class Schedules:
    def __init__(self, e:list[events]=[]) -> None:
        self.all_events = e

    def add_event(self, e):
        self.all_events.append(e)

    def remove_event_by_id(self, id):
        for el in self.all_events:
            if el.id == id:
                self.all_events.remove(el)

    def remove_event_by_name(self, name):
        for el in self.all_events:
            if el.properties["content"] == name:
                self.all_events.remove(el)

    def get_event_by_name(self, name):
        for el in self.all_events:
            if el.properties["content"] == name:
                return el

    def get_event_by_id(self, id):
        for el in self.all_events:
            if el.id == id:
                return el

    def update_event_by_id(self, id, new):
        for i, el in enumerate(self.all_events):
            if el.id == id:
                self.all_events[i] = new


class Tasks:
    def __init__(self, t=[]) -> None:
        self.all_tasks = t

    def add_task(self, t):
        self.all_tasks.append(t)

    def remove_task_by_id(self, id):
        for el in self.all_tasks:
            if el.id == id:
                self.all_tasks.remove(el)

    def get_task_by_id(self, id):
        for el in self.all_tasks:
            if el.id == id:
                return el

    def update_event_by_id(self, id, new):
        for i, el in enumerate(self.all_events):
            if el.id == id:
                self.all_events[i] = new
                return


class Inventory:
    def __init__(self, i=[]) -> None:
        self.inv_list = i

    def add_item(self, item):
        self.inv_list.append(item)

    def remove_item(self, id):
        for el in self.inv_list:
            if el.id == id:
                self.inv_list.remove(el)

    def get_item(self, id):
        for el in self.inv_list:
            if el.id == id:
                return el
