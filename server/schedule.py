import os
import time

while True:
    os.system("""./pixlet render main.star && ./pixlet push --background --api-token "API_TOKEN" "agreeably-boss-glad-cougar-2e5" ./main.webp""")
    time.sleep(120)
