from fastapi import FastAPI, BackgroundTasks
from datetime import datetime, timedelta , date
import pytz
import random
import asyncio
import os
from tweet import tweet_it
from text import challenge_posts
app = FastAPI()

# Nepali timezone
nepal_tz = pytz.timezone('Asia/Kathmandu')

# Set the start date to October 3rd of the current year
start_date = date(datetime.now().year, 10, 3)

async def scheduled_tweet(day):
    image_path = f"Pictures/{day}.jpg"
    message = challenge_posts[day]
    tweet_it(image_path, message)

async def run_scheduler():
    for day in range(1, 31):
        current_date = start_date + timedelta(days=day - 1)
        
        # Random time between 8 PM and 10 PM
        random_hour = random.randint(20, 21)
        random_minute = random.randint(0, 59)
        tweet_time = nepal_tz.localize(datetime.combine(current_date, datetime.min.time()) + timedelta(hours=random_hour, minutes=random_minute))
        
        # Calculate seconds until the tweet time
        now = datetime.now(nepal_tz)
        seconds_until_tweet = (tweet_time - now).total_seconds()
        
        if seconds_until_tweet > 0:
            await asyncio.sleep(seconds_until_tweet)
            await scheduled_tweet(day)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scheduler())

@app.get("/")
async def root():
    return {"message": "Scheduled tweet app is running", "start_date": start_date.isoformat()}
