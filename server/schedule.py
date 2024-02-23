import os
import time

import pytz

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

while True:
    load_dotenv(find_dotenv())

    api_key = os.getenv("API_KEY")
    timezone = os.getenv("TIMEZONE")
    quiet_hour_start = os.getenv("QUIET_HOUR_START")
    quiet_hour_end = os.getenv("QUIET_HOUR_END")

    os.system(
        f"""~/pixlet render ~/tidbyt/pixlet/flights.star && ~/pixlet push --background --installation-id Flights --api-token "{api_key}" "agreeably-boss-glad-cougar-2e5" ~/tidbyt/pixlet/flights.webp"""
    )

    now = datetime.now(pytz.timezone(timezone))

    if int(quiet_hour_start) < now.hour < int(quiet_hour_end):
        time.sleep(3600)
    else:
        time.sleep(30)
