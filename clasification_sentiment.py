import re
from textblob import TextBlob
import pandas as pd
import numpy as np

class TweetAnalyzer():
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return 2

    def tweets_to_data_frame(self, tweets):
        df = tweets
        return df

def main():
    tweet_analyzer = TweetAnalyzer()

    tweets = pd.read_csv('TheBabylonBee_tweetsReplies.csv')

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in tweets['source']])
    df['cleanTweet'] = np.array([tweet_analyzer.clean_tweet(tweet[2:]) for tweet in tweets['source']])
    df.to_csv('resultAnalysis.csv')  

if __name__ == "__main__":
    main()
