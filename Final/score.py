#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Impoorted For Scraping Tweets
import tweepy

# Pretty Printing JSON data
import json

# Making the Dataframes
import pandas as pd

# Importing the API keys
from api_keys import consumer_key , consumer_secret , access_token , access_token_secret

# Importing the model functions
from model import predict_sentiment , process_tweet


# In[2]:


# Set-up for Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# In[3]:


#User
user_names = []

file_in = open('users.txt','r')
for line in file_in:
    user_names.append(line.strip('\n'))

# In[4]:


from datetime import datetime, date
from dateutil import relativedelta

def duration_months(created):
    start = created
    end = datetime.strptime(str(date.today()), "%Y-%m-%d")

    diff = relativedelta.relativedelta(end, start)
    return diff.months + diff.years * 12


# In[5]:


data = []

for u in user_names:
    print(u + " fetched!")
    number_of_tweets = 200

    # Fetching the timeline of the user
    timeline = api.user_timeline(id=u, count=number_of_tweets, include_rts=True, tweet_mode = 'extended')

    # Extracting the data of the user
    
    Name = str(timeline[0]._json["user"]["name"])
    Username = str(timeline[0]._json["user"]["screen_name"])
    Follower_Count = int(timeline[0]._json["user"]["followers_count"])
    Following_Count = int(timeline[0]._json["user"]["friends_count"])
    Listed_Count = int(timeline[0]._json["user"]["listed_count"])
    Profile_Picture = str(timeline[0]._json["user"]["profile_image_url"] != "")
    Description = str(timeline[0]._json["user"]["description"] != "")
    Media = int(timeline[0]._json["user"]["statuses_count"])
    Created = api.get_user(u).created_at

    tweets = []
    time = []
    retweets = []
    likes = []

    for tweet in timeline:
        tweets.append(tweet.full_text)
        time.append(tweet.created_at)
        retweets.append(tweet.retweet_count)
        likes.append(tweet.favorite_count)

    data.append({
        "Name" : Name,
        "Username" : Username,
        "FollowerCount" : Follower_Count,
        "FollowingCount" : Following_Count,
        "ListedCount" : Listed_Count,
        "Active" : duration_months(Created),
        "TotalTweets" : Media,
        "ProfilePicture" : Profile_Picture,
        "Description" : Description,
        "TweetList" : tweets,
        "TimeList" : time,
        "Retweets" : retweets,
        "Likes" : likes
    })


# In[6]:


#Converting to dataframe

dataset = pd.DataFrame(data)


# In[7]:


#Tweet Frequency
def tweet_frequency(time_list):
    time_diff_tweets = []

    for i in range(0,len(time_list)-1):
        diff = relativedelta.relativedelta(time_list[i], time_list[i+1])
        diff_min = diff.minutes + diff.hours*60 + diff.days*24*60 + diff.months*30*24*60 + diff.years*365*24*60
        time_diff_tweets.append(diff_min)

    return sum(time_diff_tweets)/(number_of_tweets-1)


# In[8]:


def calc_retweet_count(row):
    return sum(row['Retweets'])/(len(row['Retweets']))

def calc_tweet_freq(row):
    return tweet_frequency(row['TimeList'])

def calc_FFratio(row):
    return row['FollowerCount']/row['FollowingCount']

def calc_Listed_ratio(row):
    return row['ListedCount']/row['FollowerCount']

def calc_like_count(row):
    return sum(row['Likes'])/(len(row['Likes']))


# In[9]:


dataset['RetweetCount'] = dataset.apply(calc_retweet_count, axis=1)
dataset['TweetFreq'] = dataset.apply(calc_tweet_freq, axis=1)
dataset['FFRatio'] = dataset.apply(calc_FFratio, axis=1)
dataset['ListedRatio'] = dataset.apply(calc_Listed_ratio, axis=1)
dataset['LikeCount'] = dataset.apply(calc_like_count, axis=1)


# In[10]:


#Scaling Values
from sklearn.preprocessing import MinMaxScaler
import joblib

X = dataset.iloc[:, :].values
scaler_1 = joblib.load('./static/Scaler_1.mdl')
scaler_2 = joblib.load('./static/Scaler_2.mdl')

X[:, 2:7] = scaler_1.fit_transform(X[:, 2:7])
X[:, 13:] = scaler_2.fit_transform(X[:, 13:])


# In[11]:


# Setting up the dataframe

dataset = pd.DataFrame(X, columns = ["Name", "Username","FollowerCount","FollowingCount","ListedCount","Active","TotalTweets","ProfilePicture","Description","TweetList","TimeList","Retweets", "Likes","RetweetCount", "TweetFreq", "FFRatio", "ListedRatio" , "LikeCount"])


# In[12]:


#Calculation of Twit Score
def calc_twit(row):
    pic = 0
    bio = 0
    if(row['ProfilePicture'] == "True"):
        pic = 1
        
        if(row['Description'] == "True"):
            bio = 1

            relavance_score = (0.4 * row['ListedRatio']) + (0.3 * row['RetweetCount']) + (0.3 * row['LikeCount'])
            usage_score = (0.5 * row['TweetFreq']) + (0.3 * row['TotalTweets']) + (0.1*(bio + pic))
            authenticity_score = (0.6 * row['Active']) + (0.4 * row['FollowerCount'])

            return ((0.25 * row['FFRatio']) + (0.25 * relavance_score) + (0.25 * usage_score) + (0.25 * authenticity_score))*100


# In[13]:


#Calculation of Twit Score
def calc_twit(row):
    pic = 0
    bio = 0
    if(row['ProfilePicture'] == "True"):
        pic = 1
        
        if(row['Description'] == "True"):
            bio = 1

            relavance_score = (0.4 * row['ListedRatio']) + (0.6 * row['RetweetCount'])
            usage_score = (0.5 * row['TweetFreq']) + (0.3 * row['TotalTweets']) + (0.1*(bio + pic))
            authenticity_score = (0.6 * row['Active']) + (0.4 * row['FollowerCount'])

            return ((0.25 * row['FFRatio']) + (0.25 * relavance_score) + (0.25 * usage_score) + (0.25 * authenticity_score))*100


# In[14]:


dataset['TwitScore'] = dataset.apply(calc_twit, axis=1)


# In[15]:


# Importing the words to check weather a tweet is financial or not

financial_words = set()

file = open('advanced.txt')
for line in file:    
    financial_words.add(line)

file.close()

file = open('common.txt')
for line in file:    
    financial_words.add(line.strip('\n'))

file.close()


# In[16]:


financial_total = 0
financial_positive = 0
profile_total = 0
profile_positive = 0
is_financial = False
actual_financial_score = 0

scores = {
    'profile_scores' : [],
    'financial_scores' : []
}

for row in range(len(dataset)):
    tweets_list = dataset.iloc[row ,9]
    
    for tweet in tweets_list:
        tweet = process_tweet(tweet)
        
        sentiment = predict_sentiment(tweet)
        sentiment = sentiment[0]
        
        for word in tweet:
            if word in financial_words:
                is_financial = True
                break
                
        if is_financial == True:
            financial_total += 1
            financial_positive += sentiment
            
        is_financial = False
        
        profile_total += 1
        profile_positive += sentiment
        
    scores['profile_scores'].append(profile_positive / profile_total * 100)
    
    if financial_total == 0:
        scores['financial_scores'].append(0)
    else:    
        actual_financial_score = 0.5 * ((financial_positive / financial_total * 100) + (financial_total / profile_total * 100))
        scores['financial_scores'].append(actual_financial_score)
        
    financial_total = 0
    financial_positive = 0
    profile_total = 0
    profile_positive = 0
        


# In[17]:


scores = pd.DataFrame(scores)


# In[18]:


df = pd.concat([dataset , scores] , axis = 1)


# In[19]:


def calc_score(row):
    return row["TwitScore"] + row['financial_scores'] + row['profile_scores']


# In[20]:


df['Behavioral Score'] = df.apply(calc_score, axis=1)


# In[21]:


df.to_csv("output.csv")
print("Output in output.csv")