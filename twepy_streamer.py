import time
import tweepy
import csv
import emoji
import re

import twitter_credentials
import ReplieClass

def get_emoji_regexp():
    emojis = sorted(emoji.EMOJI_UNICODE, key=len, reverse=True)
    pattern = u'(' + u'|'.join(re.escape(u) for u in emojis) + u')'
    return re.compile(pattern)

def deEmojify(text):
    return get_emoji_regexp().sub(r'', text)

def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_KEY, twitter_credentials.ACCESS_SECRET)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    alltweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=2)

    alltweets.extend(new_tweets)

    oldest = alltweets[-1].id - 1

    # Capturar los todos los twwet (No implementado por retardo)
    """
    while len(new_tweets) > 0:
        
        "getting tweets before %s" % (oldest)

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=3, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))
    """

    # Traer Tweet-Replies
    allTweetsReplies = {}
    for tweet in alltweets:
      replies = tweepy.Cursor(api.search, q='to:{}'.format(screen_name),since_id=tweet.id, tweet_mode='extended').items()
      replyCount = tweet.retweet_count
      print("Tweet de id: ",tweet.id,"| Contiene: ",tweet.text ,"| # replicas son: ",replyCount)
      while replyCount > 0:
          try:
              reply = replies.next()
              allTweetsReplies[str(tweet.id)+'_'+str(replyCount)] =  ReplieClass.Replie(
                  reply.id_str,
                  reply.in_reply_to_status_id_str,
                  tweet.text,
                  len(deEmojify(reply.full_text).encode('ascii', errors='ignore').strip()),
                  reply.created_at,
                  deEmojify(reply.full_text).encode('ascii', errors='ignore').strip(),
                  reply.favorite_count,
                  reply.retweet_count)
              replyCount -= 1

          except tweepy.RateLimitError as e:
              print("Se alcanzo el limite de tiempo de la API".format(e))
              time.sleep(60)
              continue

          except tweepy.TweepError as e:
              print("Tweepy presenta un error:{}".format(e))
              break

          except StopIteration:
              break

          except Exception as e:
              print("Fallo en iterar replies {}".format(e))
              break

    outtweets = [[tweet.id_str, 
                  len(deEmojify(tweet.text).encode('ascii', errors='ignore').strip()),
                  tweet.created_at, deEmojify(tweet.text).encode('ascii', errors='ignore').strip(),
                  tweet.favorite_count, 
                  tweet.retweet_count]
                 for tweet in alltweets]

    with open('%s_tweets.csv' % screen_name, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","len", "date", "source", "likes", "retweets"])
        writer.writerows(outtweets)
    pass

    outtweets2 = [[allTweetsReplies[tweet].id,
                   allTweetsReplies[tweet].idOriginalTweet,
                   allTweetsReplies[tweet].sourceOriginalTweet,
                   allTweetsReplies[tweet].len, 
                   allTweetsReplies[tweet].date, 
                   allTweetsReplies[tweet].source, 
                   allTweetsReplies[tweet].likes, 
                   allTweetsReplies[tweet].retweets]
                 for tweet in allTweetsReplies]

    with open('%s_tweetsReplies.csv' % screen_name, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id","idOriginalTweet", "sourceOriginalTweet","len", "date", "source", "likes", "retweets"])
        writer.writerows(outtweets2)
    pass


def main():
    get_all_tweets("TheBabylonBee")

if __name__ == "__main__":
    main()