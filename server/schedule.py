import os
import time

import pytz

from datetime import datetime, time as datetime_time
from dotenv import load_dotenv, find_dotenv

def is_current_time_between(begin_time, end_time, timezone):
    now = datetime.now(pytz.timezone(timezone)).time()

    if begin_time < end_time:
        return now >= begin_time and now <= end_time
    else: # crosses midnight
        return now >= begin_time or now <= end_time

while True:
    load_dotenv(find_dotenv())

    api_key = os.getenv("TIDBYT_API_KEY")
    device_id = os.getenv("TIDBYT_DEVICE_ID")
    timezone = os.getenv("TIMEZONE")
    quiet_hour_start_time = os.getenv("QUIET_HOUR_START_TIME")
    quiet_hour_end_time = os.getenv("QUIET_HOUR_END_TIME")

    os.system(
        f"""~/pixlet render ~/tidbyt/pixlet/flights.star && ~/pixlet push --background --installation-id Flights --api-token "{api_key}" "{device_id}" ~/tidbyt/pixlet/flights.webp"""
    )

    quiet_hour_start_hour, quiet_hour_start_minute = quiet_hour_start_time.split(":")
    quiet_hour_end_hour, quiet_hour_end_minute = quiet_hour_end_time.split(":")

    if is_current_time_between(
        datetime_time(int(quiet_hour_start_hour), int(quiet_hour_start_minute)),
        datetime_time(int(quiet_hour_end_hour), int(quiet_hour_end_minute))):
        time.sleep(3600)
    else:
        time.sleep(30)
