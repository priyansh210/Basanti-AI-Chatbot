import spacy
import pandas as pd

nlp = spacy.load("en_core_web_lg")
import dateparser

from transformers import pipeline

qa_model = pipeline("question-answering")


known_person = [
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
    "aswin",
    "herschelle",
]

known_objects = ["messsage", "schedule", "inventory", "funds", "list"]

functionality_space = {
    "add reminder": "ADD MESSAGE",
    "add message": "ADD MESSAGE",
    "tell": "ADD MESSAGE",
    "send message": "SEND MESSAGE",
    "drop message": "ADD MESSAGE",
    "have message": "GET MESSAGE",
    "remind": "ADD MESSAGE",
    "leave message": "ADD MESSAGE",
    "add": "ADD",
    "create list": "CREATE LIST",
    "add event": "ADD TO SCHEDULE",
    "schedule event": "ADD TO SCHEDULE",
    "add expense": "REMOVE FUND",
    "add fund": "ADD FUND",
    "remove fund": "REMOVE FUND",
    "spend": "REMOVE FUND",
}


def find_functionality(action):
    best_ans = (0, 0)

    for act in functionality_space:
        doc1 = nlp(act)
        doc2 = nlp(action)
        similarity = doc1.similarity(doc2)
        # print(data, similarity)
        if similarity > best_ans[0]:
            best_ans = (similarity, functionality_space[act])

    return best_ans


def break_querry(sentence: str):

    # return dict

    answer = {}

    # simplify the sentence and retrieve the root, action

    doc = nlp(sentence)
    simple_sentence = ""
    action = ""
    start = False

    for token in doc:
        if token.tag_ == "VBP":
            continue

        elif token.dep_ == "ROOT":
            root_node = token
            start = True
            action += " " + token.lemma_

            for t in token.children:

                if t.pos_ == "NOUN" and t.dep_ != "punct":
                    action += " " + t.lemma_
                    got_action = True
                    break

        if start:
            simple_sentence += " " + token.text

    sentence = simple_sentence.strip()
    action = action.strip()

    print("Simplified Sentence :", sentence)

    function = find_functionality(action)[1]
    print("Functionlaity:", function)
    answer["FUNCTION"] = function

    print("Action :", action)
    answer["ACTION"] = action

    # find the target

    stack = [root_node]
    visited = [root_node]
    target_people = []
    while stack:
        token = stack.pop()

        for i in token.children:
            if i.pos_ in ["PRON", "PROPN", "ADP"] and i not in visited:
                stack.append(i)
                visited.append(i)
                if i.pos_ in ["PRON", "PROPN"]:
                    target_people.append(i.lemma_)

    print("Who :", target_people)
    answer["WHO"] = target_people

    context = sentence

    # get what

    scheduled_for = " ".join(target_people)
    q1 = "What should I " + action + "for?"
    w1 = qa_model(question=q1, context=context)
    print("What:", w1["answer"])
    answer["WHAT"] = w1["answer"]

    # get when parsed from date time

    dates = []
    times = []
    for ent in doc.ents:

        if ent.label_ in ["TIME", "DATE"]:
            if ent.label_ == "TIME":
                times.append(ent.text)
            elif ent.label_ == "DATE":
                dates.append(ent.text)

    date = "".join(dates)
    time = "".join(times)
    input_text = date + " " + time
    parsed_datetime = dateparser.parse(input_text)
    print("When:", parsed_datetime)
    answer["WHEN"] = parsed_datetime

    # get where

    q4 = "Where should I " + action
    w4 = qa_model(question=q4, context=context)
    if w4["score"] > 0.5:
        w4 = w4["answer"]
    else:
        w4 = None

    print("Where:", w4)
    answer["WHERE"] = w4
    print(answer)

    return answer


# sentence = "send Aswin a message to meet Herschelle"
# ans = break_querry(sentence)
# print(ans)
