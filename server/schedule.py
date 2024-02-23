import glob
import os
import time

import pytz

from datetime import datetime, time as datetime_time
from dotenv import find_dotenv, load_dotenv

def is_current_time_between(begin_time, end_time, timezone):
    now = datetime.now(pytz.timezone(timezone)).time()

    if begin_time < end_time:
        return begin_time <= now <= end_time
    else: # crosses midnight
        return now >= begin_time or now <= end_time

def git_pull():
    os.system("git pull")

def push_to_client(api_key, device_id, render_path_without_extension, installation_id):
    os.system(
        f"""~/pixlet render {render_path_without_extension}.star\
        && ~/pixlet push\
        --background\
        --installation-id {installation_id}\
        --api-token "{api_key}" "{device_id}" {render_path_without_extension}.webp"""
    )


while True:
    git_pull()
    
    load_dotenv(find_dotenv())

    api_key = os.getenv("TIDBYT_API_KEY")
    device_id = os.getenv("TIDBYT_DEVICE_ID")
    timezone = os.getenv("TIMEZONE")
    quiet_hour_start_time = os.getenv("QUIET_HOUR_START_TIME")
    quiet_hour_end_time = os.getenv("QUIET_HOUR_END_TIME")
    quiet_hour_refresh_frequency_in_seconds = os.getenv("QUIET_HOUR_REFRESH_FREQUENCY_IN_SECONDS")
    non_quiet_hour_refresh_frequency_in_seconds = os.getenv("NON_QUIET_HOUR_REFRESH_FREQUENCY_IN_SECONDS")

    apps = glob.glob("../client/*.star")

    for app in apps:
        render_path_without_extension = app.split(".")[0]
        app_name_components = render_path_without_extension.split("/")[-1].split("_")
        installation_id = ''.join([s.capitalize() for s in app_name_components])

        push_to_client(
            api_key=api_key,
            device_id=device_id,
            render_path_without_extension=render_path_without_extension,
            installation_id=installation_id
        )

    quiet_hour_start_hour, quiet_hour_start_minute = quiet_hour_start_time.split(":")
    quiet_hour_end_hour, quiet_hour_end_minute = quiet_hour_end_time.split(":")

    if is_current_time_between(
        datetime_time(int(quiet_hour_start_hour), int(quiet_hour_start_minute)),
        datetime_time(int(quiet_hour_end_hour), int(quiet_hour_end_minute)),
        timezone):
        time.sleep(int(quiet_hour_refresh_frequency_in_seconds))
    else:
        time.sleep(int(non_quiet_hour_refresh_frequency_in_seconds))
