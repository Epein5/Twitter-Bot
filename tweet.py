import tweepy
import os
# Enter API tokens below
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADXBwAEAAAAA5Agl3JWmBLr2yI79jLs%2B9BDL424%3DYNfEljda1O9XYkRBH1SU9w0TeMYUm36eycNDdRsQcRnD1XyIAI'
consumer_key = 'c3h7VhWJVZJseAGUzTmuDB07e'
consumer_secret = 'WFgaB4msDdkmxonRzgPk2E1ji856bXEqP0QhTHMpZxyOiAOQAn'
access_token = '1841403680320610304-6cY4eDtrKcmawRW203WumEKo6zSTFy'
access_token_secret = '7P1slGf5gk37UaXuWlJoivR9AAX4rHuiw2LWq5qdlY1ZC'

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

def check_file_exists(file_path):
  return os.path.exists(file_path)

def tweet_it(imagepath, message):
  if check_file_exists(imagepath):
    media_id = api.media_upload(filename=imagepath).media_id_string
    client.create_tweet(text=message, media_ids=[media_id])
  else:
    client.create_tweet(text=message)