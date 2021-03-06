import picamera
import datetime
import time
import os
import matplotlib.pyplot as plot
from pi_motion_lite import *
from twython import Twython

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# Only run during a certain period of the day
START_HOUR = 8
END_HOUR = 16
RUN_ALWAYS = False

DELAY_S = 5

TWEET_IMAGE_LIMIT = 4
TWEET_TIME_LIMIT = 1


def upload_to_twitter(filenames, capture_time):
    try:
        media_ids = []
        
        for filename in filenames:
            image = open(filename, 'rb')
            response = twitter.upload_media(media=image)
            media_id = response['media_id']
            print(filename + ' ' + str(media_id))
            media_ids.append(str(media_id))
        
        print(','.join(media_ids))
        
        twitter.update_status(
            status="Taken at: " + capture_time.strftime("%d %B, %Y %H:%M:%S"),
            media_ids=','.join(media_ids))                 
        
    except Exception as e:
        print('Error uploading files:' + str(e))              
        

def should_run():
    return START_HOUR <= datetime.datetime.now().hour < END_HOUR


def format_time(datetime):
    return str(datetime.strftime('%Y-%m-%d___%H-%M-%S'))


if __name__ == '__main__':
    twitter = Twython(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )
            
    print('-Starting-')
    is_asleep = True    
    files_to_upload = []
    oldest_capture_time = None
    base_stream = getStreamImage(True)
    
    while True:
        
        if not should_run() and not RUN_ALWAYS:
            if is_asleep is False:
                print('Sleeping...')
            
            is_asleep = True
            time.sleep(60)
            continue
        else:
            if is_asleep is True:
                print('Running...')
                base_stream = getStreamImage(True)
            is_asleep = False
                
        current_stream = getStreamImage(True)
        
        if checkForMotion(base_stream, current_stream):
            capture_time = datetime.datetime.now()
            filename = 'images/capture_' + format_time(capture_time) + '.jpg'

            with picamera.PiCamera() as pi_camera:
                pi_camera.capture(filename)
            
            print("Motion Detected")
            print('\t' + str(capture_time) + '\n')
                                    
            # Save streams for debugging
            plot.imsave('streams/' + format_time(capture_time) + '_base.jpg', base_stream)            
            plot.imsave('streams/' + format_time(capture_time) + '_current.jpg', current_stream)
                      
            if oldest_capture_time is None:
                oldest_capture_time = capture_time
                        
            files_to_upload.append(filename)
            
            # Twitter has an image limit - upload photos if limit is reached 
            if len(files_to_upload) >= TWEET_IMAGE_LIMIT:
                print('Tweet image limit met')
                upload_to_twitter(files_to_upload, capture_time)
                oldest_capture_time = None
                files_to_upload = []
                
        
        if oldest_capture_time is not None:
            time_difference = datetime.datetime.now() - oldest_capture_time
            diff_minutes = (time_difference.total_seconds() / 60) 
            
            if diff_minutes >= TWEET_TIME_LIMIT:
                print('Tweet time limit met')
                upload_to_twitter(files_to_upload, capture_time)
                oldest_capture_time = None
                files_to_upload = []
                
        base_stream = current_stream
