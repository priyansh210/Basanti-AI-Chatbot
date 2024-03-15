import Levenshtein
import spacy
import dateparser
from knowledgeBase import *


# general data
kb = KB()

nlp = spacy.load("en_core_web_lg")

people = [
    "I",
    "everyone",
    "mashaal",
    "priyansh",
    "anmol",
    "divyansh",
    "rupesh",
    "rajesh",
    "ashutosh",
    "naveen",
    "harshit",
]
x = "$".join(people)

sentences = [
    "remind me to meet rajesh sir at 5 pm tomorrow",
    "we bought a few things to remind me to send you the Excel sheet letter",
    # "remember the raspberry pi is kept in my drawer",
    # "remind everyone about the peer learning session tomorrow",
    # "tell priyansh to take the keys from my table",
    # "ask rajesh sir when ever you seem him to tell me when hes free",
    # "schedule a meeting for me at 5pm tomorrow",
    # "where is raspberry pi",
    # "add the 2 raspi to our inventory",
    # "add an expense of 4 teas today",
    # "add a reminder for the evening meeting",
    # "we spent 40 rs on tea today from lab funds",
]


categories = {
    "tell": "TASK",
    "remind": "REMINDER",
    "remember": "REMEMBER",
    "find": "FIND",
    "help": "FIND",
    "ask": "TASK",
    "assign": "TASK",
    "schedule": "ADD EVENT",
    "set": "ADD",
    "add": "ADD",
    "spend": "REMOVE",
    "remove": "REMOVE",
    "cancel": "REMOVE",
    "delete": "REMOVE",
    "recall": "FIND",
    "where": "FIND",
}


add_remove_funcs = {
    "add reminder": "REMINDER",
    "add inventory": "ADD INVENTORY",
    "add funds": "ADD FUNDS",
    "add expense": "REMOVE FUNDS",
    "spend": "REMOVE FUNDS",
    "remove funds": "REMOVE FUNDS",
    "remove inventory": "REMOVE INVENTORY",
    "remove event": "REMOVE EVENT",
}


def add_new_action(action):
    print("What do you infer from : ", action)
    l = ["TASK", "REMIND", "REMEMBER", "ADD", "REMOVE", "FIND", "OTHER"]
    print(l)

    n = int(input("enter option : "))
    categories[action] = l[n]


def most_probable_intent(input_string, funcs):

    best_ans = ("", 0)
    doc1 = nlp(input_string)
    for f in funcs:
        doc2 = nlp(f)
        similarity = doc1.similarity(doc2)
        if similarity > best_ans[1]:
            best_ans = (f, similarity)

    return best_ans


def most_probable_string(input_string, string_list):
    best_match = min(string_list, key=lambda s: Levenshtein.distance(input_string, s))
    return best_match


def extract_info(created_by, sentence):

    doc = nlp(sentence.lower())

    # Breaking the sentence into nouns persons targets actions etc to understand about it

    subjects = []
    objects = []
    persons = []
    verbs = []
    nouns = []
    times = []
    dates = []
    root = []
    num = []
    question_words = []

    for token in doc:

        if "subj" in token.dep_:
            subjects.append(token.text)
        elif token.pos_ == "NUM":
            num.append(token.text)
        elif "obj" in token.dep_:
            objects.append(token.lemma_)

        elif "ROOT" in token.dep_:
            root.append(token.lemma_)

        elif token.pos_ == "VERB":
            verbs.append(token.lemma_)

        elif token.dep_ == "advmod" or token.pos_ == "ADV":
            question_words.append(token.lemma_)

        elif token.pos_ == "NOUN":
            nouns.append(token.text)

    for ent in doc.ents:

        if ent.label_ in ["TIME", "DATE"]:
            if ent.label_ == "TIME":
                times.append(ent.text)
            elif ent.label_ == "DATE":
                dates.append(ent.text)

    # converting the objects to people

    scheduled_for = ""
    for obj in objects:
        for p in people:
            doc1 = nlp(obj)
            doc2 = nlp(p)
            similarity = doc1.similarity(doc2)
            if similarity > 0.8:
                if scheduled_for == "":
                    scheduled_for = p

                persons.append(p)

    # the task is the sentence
    task = sentence

    # converting date time to standard format
    date = "".join(dates)
    time = "".join(times)
    input_text = date + " " + time
    parsed_datetime = dateparser.parse(input_text)

    # detremining category of the request
    if "where" in question_words:
        root.insert(0, "where")
    cat = ""
    for action in root:
        if action not in categories:
            print(sentence)
            add_new_action(action)

        cat = categories[action]
        # print(cat)
        break

    # finalizing the category , Add a meeting and schedule a meeting could be the same

    if cat == "ADD" or cat == "REMOVE":
        arbt = " ".join(root) + " " + " ".join(objects)
        cat = most_probable_intent(arbt, list(add_remove_funcs.keys()))[0]
        cat = add_remove_funcs[cat]

    # debugging
    print("----------")
    print(objects, verbs)
    print(question_words)
    print("ACTION:", root)
    print("CREATED BY:", created_by)
    print("CREATED FOR:", scheduled_for)
    print("TASK:", task)
    print("DUE TIME:", parsed_datetime)
    print("CATEGORY:", cat)

    print("----------")
    # category

    if cat == "REMEMBER":
        kb.add((created_by, task))
        kb.update()

    if cat == "FIND":
        print(kb.find(sentence))

    # Reminder , Meeting , schedule a meeting , assign task


# for i in sentences:
#     extract_info("priyansh", i)
