# Trust and Affluence Score Prediction

## Introduction

Less than 10% Indians have a credit bureau presence, so it is essential to identify and utilize alternate forms of data to assess customers’s credit worthiness. As part of this project, we tried to identify markers from social media data that indicate trust and affluence with we expect to be a valid indicator for credit score.

Due to lack of enough data to verify any methods that we may think of, we have taken inspiration and have based most of our approach on [this paper](https://www.itm-conferences.org/articles/itmconf/pdf/2021/02/itmconf_icitsd2021_01012.pdf) published in the ITM Web of Conferences, pertaining to a similar topic, because it had precedent. The paper proposes a method to calculate a social media score (referred to as Behavioral Score) derived from a user’s Twitter profile and Twitter timeline, which they later propose combining with their traditional credit scores. Taking inspiration from the
paper, we have modelled our approach around finding a behavioral score for a person which acts as a measure of their trust and affluence, helping us assess their credit worthiness.

We have attempted to derive - Twit Score, Profile Score and Financial Score for a user, which were aggregated to get our final measure (details on the scores and the approach are in later slides.)

![1.png](https://github.com/DebangshuB/Trust-and-Affluence-Score-Prediction/blob/main/Images/1.png)

## Our Approach

For evaluating a user we use the flow as discussed above

Behavioral Score = Twit Score + Profile Score + Financial Score

The user data is collected using Tweepy, a Python library for accessing the Twitter
API. 

We collected data for 34 users of varying backgrounds. We extracted the features
from the data, applied feature engineering on them, and scaled all the numerical
values. Using these features we then calculate the scores. 

Using the previously trained model and this normalization factors we can predict the scores for a new user / users.

**Scoring Mechanism**

| Scores          | Definition                                                                                                                                                                                                                                                                                                                                                                    |
|:---------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Twit Score      | The user profile of the person forms the basis of computing the twit score. It is an attempt to rate the quality of Twitter user by various metrics available through the API. A Twitter user with a relatively low wit score is more likely to be a sign of a spam account or a less safe user.                                                                              |
| Profile Score   | The 200 most recent tweets of the user form the basis of this score. They are  pre-processed by tokenization, lemmatization, stop-word removal, etc. Subsequently, sentiment analysis is performed and the percentage of positive  tweets is chosen to be the profile score.                                                                                                  |
| Financial Score | The financial tweets of the user form the basis of this score. The financial tweets  are identified by checking against a corpus of such terms. To classify the financial  tweets as positive or negative, sentiment analysis is performed on them. The  financial score is the average of the percentage of financial tweets and the percentage of positive ones among them. |

**Twit Score Calculation**

| Serial No. | Score                   | Data                                  | Weights                   |
| ---------- | ----------------------- | ------------------------------------- | ------------------------- |
| 1          | **Friend Follow Ratio** | followers_count / friends_count       | 25% of Twit Score         |
| 2          | **Relevance Score**     |                                       | 25% of Twit Score         |
| 2 (a)      | Listed Ratio            | listed_count / followers_count        | 40% of Relevance Score    |
| 2 (b)      | ReTweet                 | Average retweet count for past tweets | 30% of Relevance Score    |
| 2 (c)      | Likes                   | Average likes for past tweets         | 30% of Relevance Score    |
| 3          | **Usage Score**         |                                       | 25% of Twit Score         |
| 3 (a)      | Tweet Frequency         | Average time between tweets           | 50% of Usage Score        |
| 3 (b)      | Media                   | Amount of status posted               | 30% of Usage Score        |
| 3 (c)      | Twitter Bio             | description                           | 10% of Usage Score        |
| 3 (d)      | Profile Picture         | profile_image_url                     | 10% of Usage Score        |
| 4          | **Authenticity Score**  |                                       | 25% of Twit Score         |
| 4 (a)      | Duration                | created_at                            | 60% of Authenticity Score |
| 4 (b)      | Followers Count         | followers_count                       | 40% of Authenticity Score |
|            |                         |                                       | **100% of Twit Score**    |

For performing Sentiment Analysis we trained a custom model using the
Sentiment140 dataset consisting of labeled tweets.
We tested Logistic Regression, Random Forests, Gradient Boosting, Adaptive
Boosting, and Voting Classifier with all the same models as well, by feeding Count
Vectorized Data followed by TFIDF Vectorized data.
We concluded that Logistic Regression with Count Vectorized data would be the
best choice. The code for running the different models we tried, along with their
results as confusion matrices.
For finding whether a tweet is a financial tweet or not, we compiled a list of
financial terms and checked the tweets for common
and advanced words related to finance.

## Result

After executing the code we get an excel file that looks like this.

![2.png](https://github.com/DebangshuB/Trust-and-Affluence-Score-Prediction/blob/main/Images/2.png)

## Limitations

In our current solution, we have taken relative values of the elements used for
calculating the the Twit Score. The accuracy is limited by the number and variety
of people, because it is relative.
Verification of the accuracy of correlation between the behavioral score and the
actual credit score has not been done by us as it was not possible to get real credit
scores for people on Twitter.
Twitter users are younger, more highly educated and have higher incomes than
average adults overall (source: Pew Research). It can be said that our solution is
slightly skewed towards such more affluent kind of people. There could
potentially be a lot of low income people whose credit worthiness if we could
determine and provide them credit, it would actually lead to development at the
grassroots level.

## Improvements

**Expanding to Instagram and Facebook**


Instagram and Facebook have a more tightly knit network of users, compared to
twitter where everyone can just follow anyone they wish to. They are also less
skewed towards the more affluent people compared to Twitter.
Instagram and Facebook have similar concepts of posts, comments, activity, tags,
mentions, etc. With minor modification to our current code, we can process that
information too with relative ease. Other useful information such as educational
qualifications, employment history, number of dependants can also be extracted,
along with an estimation of their income levels based off geotags on posts, etc,
leading to more accurate and well rounded overall score

## Future Score

Applying network analysis using people with pre-existing credit scores in a
person’s network, which we had previously proposed, as an additional element to
the solution would yield even better results.
Creating clusters of people who already have credit scores, according to their
interests data extracted from Instagram and Facebook, and other financial and
personal data, and assigning new similar people to those clusters could result in
us being able to determine scores of people in a more accurate and easier way as
well.
The aforementioned clustering can have alternative use-cases like recommender
systems and social commerce applications as well.
Analyzing a person’s transactions history, with their input on it, and using it in
tandem with the social media score can help establish a tighter relationship
between their social media behaviour and their financial attitudes.

## Conclusion

From running analysis on 34 samples, it can be deduced that a person
with behavioral score around 150 or above has a good level of trust and
affluence.
Our solution is proof of our concept that data extracted from social
media can contribute in predicting a person’s credit worthiness.
We believe that we are aware of our shortcomings; and with enough
time in our hands, and proper resources, such as a means of collecting
user social media data, the improvements and future scope of our
solution is not at all a pipe dream, and is something we could totally
achieve.

## Contributors

### Primary Contributors
* [Aditya Kumar Dalmia](https://github.com/dalmeow)
* [Debangshu Bhattacharjee](https://github.com/DebangshuB)
* [Debmalya Chatterjee](https://github.com/Debmalya-prog)

#### About the Primary Contributors

The three of us are in the third year of our B.Tech in Computer Science and Engineering from KIIT University, Bhubaneswar, India.\
This project was out submission for the problem statement **Trust and affluence signal extraction from social media data** for Flipkart GRID 3.0.

