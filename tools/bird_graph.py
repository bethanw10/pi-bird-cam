from datetime import datetime, timedelta
from twython import Twython, TwythonError
import pandas as pd
import matplotlib.pyplot as plt

from auth import (
    consumer_key,
    consumer_secret
)

def round_datetime(dt, minutes):
    approx = round(dt.minute / 30.0) * 30

    date = dt.replace(second=0)
    date += timedelta(minutes=((approx * 60) - dt.minute))
    print(date)
    return date


twitter = Twython(consumer_key, consumer_secret)

try:
    user_timeline = twitter.get_user_timeline(screen_name='Pi_Bird_Cam', count=200)

    dates = []
    twitter_date_format = '%a %b %d %H:%M:%S +0000 %Y'

    for post in user_timeline:
        created_date = datetime.strptime(post['created_at'], twitter_date_format)
        dates.append(created_date)

    dateIndex = pd.DatetimeIndex(dates)
    #dateIndex = dateIndex.groupby(dateIndex.hour)
    #dateIndex = pd.DataFrame(dates)

    dateIndex = dateIndex.to_series().apply(lambda dt: round_datetime(dt, timedelta(minutes=30)))
    dateIndex = pd.DatetimeIndex(dateIndex)
    dateIndex = dateIndex.groupby(dateIndex.time)

    print(dateIndex.keys())

    count_per_hour = [len(value) for value in dateIndex.values()]
    hour_range = [hour for hour in dateIndex.keys()]
    #hour_range = [f"{hour}:00 - {hour}:59" for hour in dateIndex.keys()]
    #hour_range = [f"{hour}:00" for hour in dateIndex.keys()]

    plt.bar(range(len(dateIndex)), count_per_hour, alpha=0.5, width=0.9)
    plt.xticks(range(len(dateIndex)), hour_range, rotation='vertical')

    plt.title('Number of Birds by Time of Day')
    plt.xlabel('Hour')
    plt.ylabel('Number of Birds')
    plt.show()

except TwythonError as e:
    print(e)

