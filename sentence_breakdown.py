import spacy
import pandas as pd

nlp = spacy.load("en_core_web_lg")
import dateparser
from listen import *
from transformers import pipeline
from KB import *

qa_model = pipeline("question-answering")

import difflib


def find_known_names(target, known_names):
    found_names = []
    for people in target:
        closest_match = difflib.get_close_matches(people, known_names, n=1, cutoff=0.7)
        if closest_match:
            found_names.append(closest_match[0])
    return found_names


def phrase_handling(action):

    options = set(functionality_space.values())

    # dispaly options:
    for i, op in enumerate(options):
        print(i, op)
    print(i + 1, "OTHER")

    strr = "Which action did you infer from:" + action
    print(strr)
    ans = listenEnglish()
    function = get_functionality(ans)[1]

    # add functionlity
    functionality_space[action] = function


def get_functionality(action):
    best_ans = (0, 0)

    for act in functionality_space:
        doc1 = nlp(act)
        doc2 = nlp(action)
        similarity = doc1.similarity(doc2)
        # print(data, similarity)
        if similarity > best_ans[0]:
            best_ans = (similarity, functionality_space[act])

    return best_ans


def break_sentence(sentence):

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

    return sentence, action, root_node


def get_root(sentence):
    doc = nlp(sentence)
    for token in doc:
        if token.dep_ == "ROOT":
            return token


def get_target(sentence):
    root_node = get_root(sentence)
    stack = [root_node]
    visited = [root_node]
    target_people = []
    while stack:
        token = stack.pop()
        if token.pos_ in ["PRON", "PROPN"]:
            target_people.append(token.lemma_)

        for i in token.children:
            if i.pos_ not in ["VERB"] and i not in visited:
                stack.append(i)
                visited.append(i)

    target_people = find_known_names(target_people, known_person)

    if target_people == []:
        return None
    else:
        return target_people


def get_when(sentence):
    doc = nlp(sentence)
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
    return parsed_datetime


def break_querry(sentence: str):
    if not sentence:
        return None

    context = sentence

    # return dict

    answer = {}

    # simplify the sentence and retrieve the root, action
    sentence, action, root_node = break_sentence(sentence)

    print("Simplified Sentence :", sentence)

    # get function from function space
    function = get_functionality(action)

    # unknow action handling
    if function[0] < 0.6:
        phrase_handling(action)

    print("Functionlaity:", function)
    answer["FUNCTION"] = function

    print("Action :", action)
    answer["ACTION"] = action

    # find the target
    target_people = get_target(sentence)
    print("Who :", target_people)
    answer["WHO"] = target_people

    # get what
    q1 = "What should I " + action + "for?"
    w1 = qa_model(question=q1, context=context)
    print("What:", w1["answer"])
    answer["WHAT"] = w1["answer"]

    # get when parsed from date time
    parsed_datetime = get_when(sentence)
    print("When:", parsed_datetime)
    answer["WHEN"] = parsed_datetime

    # get where
    q4 = "Where should I " + action + w1["answer"]
    w4 = qa_model(question=q4, context=context)
    if w4["score"] > 0.5:
        w4 = w4["answer"]
    else:
        w4 = None

    print("Where:", w4)
    answer["WHERE"] = w4

    return answer


# sentence = "input sentence"
# ans = break_querry(sentence)
# print(ans)
