import spacy
import datefinder

nlp = spacy.load("en_core_web_sm")


def extract_subjects_objects_persons_verbs(sentence):
    # Process the input sentence using spaCy
    doc = nlp(sentence)
    
    # Initialize lists to store subjects, objects, persons, and verbs
    subjects = []
    objects = []
    persons = []
    verbs = []
    
    # Iterate through the tokens in the processed sentence
    for token in doc:
        # Check if the token is a subject (nsubj or nsubjpass)
        if "subj" in token.dep_:
            subjects.append(token.text)
        
        # Check if the token is an object (obj)
        elif "obj" in token.dep_:
            objects.append(token.text)
        
        # Check if the token is a person (PERSON entity)
        elif token.ent_type_ == "PERSON":
            persons.append(token.text)
        
        # Check if the token is a verb
        elif "verb" in token.dep_:
            verbs.append(token.text)
    
    # Return the extracted subjects, objects, persons, and verbs
    return subjects, objects, persons, verbs


def extract_time_and_date(sentence):
    # Process the input sentence using spaCy
    doc = nlp(sentence)
    
    # Initialize lists to store extracted time and date information
    times = []
    dates = []
    
    # Iterate through the entities in the processed sentence
    for ent in doc.ents:
        # Check if the entity is a time or date
        if ent.label_ in ["TIME", "DATE"]:
            if ent.label_ == "TIME":
                times.append(ent.text)
            elif ent.label_ == "DATE":
                dates.append(ent.text)
    
    # If no time or date entities are found, use datefinder to extract them
    if not times and not dates:
        matches = list(datefinder.find_dates(sentence))
        for match in matches:
            if match.time():
                times.append(match.strftime("%H:%M:%S"))
            if match.date():
                dates.append(match.strftime("%Y-%m-%d"))
    
    # Return the extracted time and date information
    return times, dates



sentence = "tell priyansh to that the meeting is scheduled on 20 jan 5 in the evening  "


subjects, objects, persons, verbs = extract_subjects_objects_persons_verbs(sentence)
times, dates = extract_time_and_date(sentence)


print("Subjects:", subjects)
print("Objects:", objects)
print("Persons:", persons)
print("Verbs:", verbs)
print("Times:", times)
print("Dates:", dates)
