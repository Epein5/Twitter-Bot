import tweepy
import os
from text import challenge_posts
# Enter API tokens below
bearer_token = "AAAAAAAAAAAAAAAAAAAAAKsQwQEAAAAAqVYNOt%2FmA6w7uLPo7ZmIvnx4WSk%3DSfL6CMUKB0jBrgoyZQOMT3qlJ2E7vhnOaMtzO2VgV6aEgnlwtg"
consumer_key = 'ySPI5798pkarOajxw3Qy1tcqv'
consumer_secret = 'ZBjhBApV22DiU3Dmxy5LwpwcyDAL9wjsERGQpPAF8Z14bvRtzp'
access_token = '1841403680320610304-rMCnKkYFmfRTuifus80c1myk9tifyH'
access_token_secret = 'rkixl0mEWKPu8hdEi9UKvYJcUWN3mc1Pra1bLu8SomgUR'

# bearer_token = 'AAAAAAAAAAAAAAAAAAAAAKsQwQEAAAAAqVYNOt%2FmA6w7uLPo7ZmIvnx4WSk%3DSfL6CMUKB0jBrgoyZQOMT3qlJ2E7vhnOaMtzO2VgV6aEgnlwtg'
# api_key = 'ySPI5798pkarOajxw3Qy1tcqv'
# api_key_secret = 'ZBjhBApV22DiU3Dmxy5LwpwcyDAL9wjsERGQpPAF8Z14bvRtzp'
# client_id = 'R0RNQmhfOVN6VEtYVkNKWjhoLXo6MTpjaQ'
# client_secret = 'xZeJ6DKPgB0p3_5zkKKp4plWYs-6EKDssvRhY2xW2pXVCEuXRJ'
# access_token = 1841403680320610304-rMCnKkYFmfRTuifus80c1myk9tifyH
# access_token_secret = rkixl0mEWKPu8hdEi9UKvYJcUWN3mc1Pra1bLu8SomgUR

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