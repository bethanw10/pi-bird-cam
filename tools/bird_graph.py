from datetime import datetime, timedelta
from twython import Twython, TwythonError
import pandas as pd
import matplotlib.pyplot as plt

from auth import (
    consumer_key,
    consumer_secret
)


def round_datetime(dt, minutes):
    approx = round(dt.minute / float(minutes)) * minutes

    date = dt.replace(second=0)
    date += timedelta(minutes=(approx - dt.minute))
    print(str(dt) + " -> " + str(date))
    return date


def hour_graph(date_times):
    dates_index = pd.DatetimeIndex(date_times)
    dates_index = dates_index.groupby(dates_index.hour)

    print(dates_index.keys())

    count_per_hour = [len(value) for value in dates_index.values()]
    # hour_range = [f"{hour}:00 - {hour}:59" for hour in dateIndex.keys()]
    hour_range = [f"{hour}:00" for hour in dates_index.keys()]

    plt.bar(range(len(dates_index)), count_per_hour, alpha=0.5, width=0.9)
    plt.xticks(range(len(dates_index)), hour_range, rotation='vertical')

    plt.title('Number of Birds by Time of Day')
    plt.xlabel('Hour')
    plt.ylabel('Number of Birds')
    plt.show()


def time_graph(date_times, time_division_minutes):
    date_index = pd.Series(date_times)

    date_index = date_index.apply(lambda dt: round_datetime(dt, time_division_minutes))

    date_index = pd.DatetimeIndex(date_index)
    date_index = date_index.groupby(date_index.time)

    print(date_index.keys())

    count_per_hour = [len(value) for value in date_index.values()]
    hour_range = [hour.strftime('%H:%M') for hour in date_index.keys()]

    plt.bar(range(len(date_index)), count_per_hour, alpha=0.5, width=0.9)
    plt.xticks(range(len(date_index)), hour_range, rotation='vertical')
    return plt


def half_hour_graph(date_times):
    plot = time_graph(date_times, 30)

    plot.title('Number of Birds per half hour')
    plot.xlabel('Time')
    plot.ylabel('Number of Birds')
    plot.show()


def quarter_hour_graph(date_times):
    plot = time_graph(date_times, 15)

    plot.title('Number of birds per quarter hour')
    plot.xlabel('Time')
    plot.ylabel('Number of Birds')
    plot.show()


if __name__ == '__main__':
    twitter = Twython(consumer_key, consumer_secret)

    try:
        user_timeline = twitter.get_user_timeline(screen_name='Pi_Bird_Cam', count=200)

        dates = []
        twitter_date_format = '%a %b %d %H:%M:%S +0000 %Y'

        for post in user_timeline:
            created_date = datetime.strptime(post['created_at'], twitter_date_format)
            dates.append(created_date)

        quarter_hour_graph(dates)

    except TwythonError as e:
        print(e)

