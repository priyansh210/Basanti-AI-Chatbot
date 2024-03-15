import json
import spacy

nlp = spacy.load("en_core_web_lg")


class KB:

    def __init__(self) -> None:

        f = open("knowledgeBase.json", "r")
        data = json.load(f)
        f.close()

        self.KB = data

    def get(self):
        return self.KB

    def update(self):
        with open("knowledgeBase.json", "w") as f:
            newData = json.dumps(self.KB)
            f.write(newData)
        f.close()

    def add(self, obj):
        createdBy, knowledge = obj
        data = {"createdBy": createdBy, "knowledge": knowledge}
        self.KB.append(data)
        print(self.KB)

    def find(self, sentence):

        best_ans = []

        for data in self.KB:
            doc1 = nlp(data["knowledge"])
            doc2 = nlp(sentence)
            similarity = doc1.similarity(doc2)
            # print(data, similarity)
            if similarity > 0.6:
                best_ans.append((data["knowledge"], similarity))

        return sorted(best_ans, key=lambda x: x[1], reverse=True)[0]


# testing
# known = KB()
# print(known.get())
# print(known.find("where is raspberry pi"))
# known.add(("priyansh", "the pen is on the table"))
# known.update()
# print(known.get())
