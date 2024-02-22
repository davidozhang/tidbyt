import os
import time

from datetime import datetime
import pytz

while True:
    os.system("""./pixlet render main.star && ./pixlet push --background --installation-id Flights --api-token {{API_KEY}} "agreeably-boss-glad-cougar-2e5" ./main.webp""")

    pacificTimeNow = datetime.now(pytz.timezone("America/Los_Angeles"))

    if 0 < pacificTimeNow.hour <= 2:
        time.sleep(60)
    elif 2 < pacificTimeNow.hour < 8:
        time.sleep(3600)
    else:
        time.sleep(30)
