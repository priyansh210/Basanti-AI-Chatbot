import spacy
import pandas as pd
from sentence_breakdown import *

nlp = spacy.load("en_core_web_lg")

a = get_target("Priyansh")
print(a)
