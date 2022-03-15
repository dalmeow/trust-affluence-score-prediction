# How to use the functions ?
# predict(tweet) 
#     -> Tokenized and preprocessed tweet
#     -> Sentiment 


# Cleaning Tweets
import re

# Removing stopwords and Stemming
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import string

# Importing models
import joblib
import json

model = joblib.load("./static/Logistic_Regression.mdl")
vectorizer = joblib.load("./static/Vectorizer_CV.mdl")

f = open('./static/wordfreq.json')
wordfreq = json.load(f)
f.close()

def predict_sentiment(tweet):

    # The preprocess funtion would be used beforehand.
    # The input tweet will be a list of stemmed words

    tweet = [ word for word in tweet if word in wordfreq ]
    
    tweet = " ".join(tweet)
    tweet = vectorizer.transform([tweet])
    result = model.predict(tweet)
    
    return result
 
 
# Downloading the stop words
nltk.download('stopwords')
stopwords_english = stopwords.words('english')

# Instantiating the Stemmer
stemmer = PorterStemmer()

# Instantiating the Tokenizer
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

def process_tweet(tweet):

    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)

    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)

    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)

    # remove punctuation
    tweet = re.sub(r'[^A-Za-z0-9 ]+', '', tweet)

    # tokenize tweets
    tweet_tokens = tokenizer.tokenize(tweet)

    tweets_clean = []
    
    for word in tweet_tokens:
        if (word not in stopwords_english and word not in string.punctuation):
            stem_word = stemmer.stem(word)  # stemming word
            tweets_clean.append(stem_word)

    return tweets_clean