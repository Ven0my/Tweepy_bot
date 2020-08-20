# This is a twitter bot which auto replies to tweets when given(input) with a certain search string.
import keys
import tweepy
from random import randint
from time import sleep
import random
import csv
import time



#Authentication part.
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


FILE_NAME = "last_seen.txt"

# Methods for updating the last seen tweet to prevent duplicate posts
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = str(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

# Prevents sending too many requests to Twitter's servers
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

last_seen_id = retrieve_last_seen_id(FILE_NAME)
   
#list to choose a random text.
messages = [
    "Hi would love to help you!",
    "we have some recruiters who can help you.",            
    "Go get one here",
    "click the following link",
    "so click the attached link",
    "Want job? You are just a click away!!",
    "Its a Pleasure to help you, Click the following link",
    "You are Just a click away from getting your dream job",
    "Hope this helps you.",
    "Click the following link and apply for the job",
    "get your dream job here."
    ]

message = ""


#searching for the tweets (geo_search = USA)
places = api.geo_search(query="USA", granularity="country")
place_id = places[0].id
search_results = api.search(q ="I need a job", count=10000, lang="en", place = place_id, since_id=last_seen_id,tweet_mode='extended')
def respond_to_search(search_results, tweet_list):
    for result in reversed(search_results):

        # selecting a random message from the message list
        message = random.choice(messages) 
        
        # Prints 
        print(result.id)
        print("TUTREE BOT INITIATED")
        
        # Posts resulting tweets and shows what the bot will tweet
        print("@" + result.user.screen_name + ": '" + result.full_text + "'")
        print("@JobAssistant1: '@" + result.user.screen_name + " " + message + "\n https://amazjobs.com""'\n")
        
        # Updated last_seen_id to prevent responding to the same tweet
        last_seen_id = result.id
        store_last_seen_id(last_seen_id,  FILE_NAME)
        # Posts Tweet
        post = api.update_status('@' + result.user.screen_name + " " + message + "\n https://amazjobs.com", result.id)
        

        # writing tweet id and reply id in a csv file
        with open('tweet_record.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([result.user.screen_name, result.id, post.id])
        
    return message

# Runs function
respond_to_search(search_results, message)
