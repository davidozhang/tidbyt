import os
import time

import pytz

from datetime import datetime
from dotenv import load_dotenv, find_dotenv

while True:
    load_dotenv(find_dotenv())

    api_key = os.getenv("API_KEY")
    os.system(
        f"""~/pixlet render ~/tidbyt/pixlet/flights.star && ~/pixlet push --background --installation-id Flights --api-token "{api_key}" "agreeably-boss-glad-cougar-2e5" ~/tidbyt/pixlet/flights.webp"""
    )

    pacificTimeNow = datetime.now(pytz.timezone("America/Los_Angeles"))

    if 0 < pacificTimeNow.hour <= 2:
        time.sleep(60)
    elif 2 < pacificTimeNow.hour < 8:
        time.sleep(3600)
    else:
        time.sleep(30)

