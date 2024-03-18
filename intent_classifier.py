import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load the pre-trained BERT model and tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Load the fine-tuned model weights
model.load_state_dict(torch.load("/content/gdrive/My Drive/multiclass_bert_model.pth"))
model.eval()  # Set the model to evaluation mode

# Define a function to predict the sentiment of a single text
def predict_sentiment(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt", max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).detach().numpy()[0]
        predicted_label = torch.argmax(logits, dim=1).item()
        # max_confidence = probabilities[predicted_label]
        max_confidence=1
        if max_confidence < 0.7:
          predicted_label_name = "unknown"
        else:
          # Convert label index to label name (assuming you have a list of labels)
          labels = ["Question","Reminder"]  # Example list of labels
          predicted_label_name = labels[predicted_label]

    return predicted_label_name,max_confidence