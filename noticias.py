import requests
from textblob import TextBlob
import datetime as dt
import numpy as np

# Função para obter notícias
def get_news(symbol):
    url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey=54101bd1c60f43e69ef6b66b647fb9a6"
    response = requests.get(url)
    return response.json()

# Função para analisar o sentimento
def analyze_sentiment(news):
    daily_sentiments = []
    monthly_sentiments = []
    today = dt.datetime.now().date()
    current_month = today.month

    for article in news['articles']:
        analysis = TextBlob(article['title'])
        sentiment = analysis.sentiment.polarity
        article_date = dt.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date()

        if article_date == today:
            daily_sentiments.append(sentiment)
        if article_date.month == current_month:
            monthly_sentiments.append(sentiment)

    daily_sentiment = np.mean(daily_sentiments) if daily_sentiments else 0
    monthly_sentiment = np.mean(monthly_sentiments) if monthly_sentiments else 0

    return daily_sentiment, monthly_sentiment, news['articles']

# Obter e analisar notícias
symbol = "EURUSD"
news = get_news(symbol)
daily_sentiment, monthly_sentiment, articles = analyze_sentiment(news)

print(f"Sentimento diário para {symbol}: {daily_sentiment}")
print(f"Sentimento mensal para {symbol}: {monthly_sentiment}")
print("\nNotícias do dia:")
for article in articles:
    article_date = dt.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').date()
    if article_date == dt.datetime.now().date():
        print(f"- {article['title']} ({article['publishedAt']})")