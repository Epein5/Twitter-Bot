# from fastapi import FastAPI, BackgroundTasks
# from datetime import datetime, timedelta , date
# import pytz
# import random
# import asyncio
# import os
# from tweet import tweet_it
# from text import challenge_posts
# app = FastAPI()

# # Nepali timezone
# nepal_tz = pytz.timezone('Asia/Kathmandu')

# # Set the start date to October 3rd of the current year
# start_date = date(datetime.now().year, 10, 3)

# async def scheduled_tweet(day):
#     image_path = f"Pictures/{day}.jpg"
#     message = challenge_posts[day]
#     tweet_it(image_path, message)

# async def run_scheduler():
#     for day in range(1, 31):
#         current_date = start_date + timedelta(days=day - 1)
        
#         # Random time between 8 PM and 10 PM
#         random_hour = random.randint(20, 21)
#         random_minute = random.randint(0, 5)
#         tweet_time = nepal_tz.localize(datetime.combine(current_date, datetime.min.time()) + timedelta(hours=23, minutes=random_minute))
        
#         # Calculate seconds until the tweet time
#         now = datetime.now(nepal_tz)
#         seconds_until_tweet = (tweet_time - now).total_seconds()
        
#         if seconds_until_tweet > 0:
#             await asyncio.sleep(seconds_until_tweet)
#             await scheduled_tweet(day)

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(run_scheduler())

# @app.get("/")
# async def root():
#     return {"message": "Scheduled tweet app is running", "start_date": start_date.isoformat()}

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
import pytz

from text import challenge_posts
from tweet import tweet_it

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.start()

def scheduled_tweet():
    current_date = datetime.now(pytz.timezone('Asia/Kathmandu'))
    days_since_start = (current_date.date() - start_date).days
    
    if days_since_start == 0:
        day_number = 4
    else:
        day_number = 4 + days_since_start

    if 4 <= day_number < len(challenge_posts):
        tweet_it(f"Pictures/{day_number}.jpg", challenge_posts[day_number])
        print(f"Tweeted for day {day_number}")
    else:
        print(f"Day {day_number} is out of range. No tweet sent.")

start_date = (datetime.now(pytz.timezone('Asia/Kathmandu')) + timedelta(days=1)).date()

scheduler.add_job(
    scheduled_tweet,
    trigger=CronTrigger(hour=20, minute=0, start_date=start_date),
    id='daily_tweet',
    name='Tweet every day at 8 PM',
    timezone=pytz.timezone('Asia/Kathmandu')
)

@app.get("/")
async def root():
    return {"message": "Scheduled tweeting application is running"}

@app.get("/next-run")
async def get_next_run():
    job = scheduler.get_job('daily_tweet')
    if job:
        next_run = job.next_run_time
        return {"next_run": next_run.strftime("%Y-%m-%d %H:%M:%S")}
    return {"message": "No scheduled job found"}