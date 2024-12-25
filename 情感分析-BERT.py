import pandas as pd
from tqdm import tqdm
from torch.nn.functional import softmax
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import re

# Ensure you have a CUDA device available and detected by PyTorch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pre-trained BERT tokenizer and BERT model for sequence classification
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertForSequenceClassification.from_pretrained('bert-base-chinese')
model.to(device)
model.eval()

# Function to predict sentiment using BERT
def predict_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True).to(device)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)
    return probs[:, 1].item()  # Assuming that class 1 corresponds to positive sentiment

# Read the Excel file
df = pd.read_excel("春晚小品40年_数据.xlsx", sheet_name='小品分析')

# Perform sentiment analysis using BERT
for column in ['内容概括', '台词']:
    sentiment_scores = []
    for text in tqdm(df[column], desc=f'Analyzing {column}'):
        # Predict sentiment
        sentiment_score = predict_sentiment(text)
        sentiment_scores.append(sentiment_score)
    df[column + '情感'] = sentiment_scores

# Save to a new Excel file
df.to_excel("春晚小品40年_分析_BERT.xlsx", index=False)