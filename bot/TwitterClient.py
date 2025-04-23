import requests
import json
from requests_oauthlib import OAuth1
from config import Config

class TwitterClient:
    def __init__(self):
        self.url = "https://api.twitter.com/2/tweets"
        self.auth = OAuth1(
            Config.TWITTER_CONSUMER_API_KEY, 
            Config.TWITTER_CONSUMER_API_SECRET,
            Config.TWITTER_ACCESS_TOKEN, 
            Config.TWITTER_ACCESS_SECRET
        )

    def post_tweet(self, text):
        payload = json.dumps({"text": text})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.url, headers=headers, data=payload, auth=self.auth)
        return response.json()

# Example usage
if __name__ == "__main__":
    twitter_client = TwitterClient()
    tweet_response = twitter_client.post_tweet("how was the day going ")
    print(tweet_response)
