import re
from nltk.sentiment import SentimentIntensityAnalyzer

# Initialize
sia = SentimentIntensityAnalyzer()


def clean_text(text):
    text = re.sub(r"http\S+", "", text)      
    text = re.sub(r"#\w+", "", text)         
    text = re.sub(r"@\w+", "", text)         
    text = re.sub(r"[^\w\s]", "", text)      
    return text.strip()


def analyze_sentiment(text):

    text = clean_text(text)

    if not text or len(text) < 5:
        return "neutral", 0.0

    score = sia.polarity_scores(text)["compound"]

    if score > 0.05:
        label = "positive"
    elif score < -0.05:
        label = "negative"
    else:
        label = "neutral"

    return label, round(score, 4)