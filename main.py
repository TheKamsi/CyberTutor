import random
from twilio.rest import Client
from datetime import datetime
from info import TwilioInfo
import schedule
import time

# Twilio account credentials
credentials = TwilioInfo()

client = Client(credentials.sid, credentials.token)

# File to read from
FILE = 'acronyms.txt'

def get_random_acronym():
    with open(FILE) as f:
        acronyms = f.read().split('\n\n')

    today = datetime.now().date()

    #Pick a random acronym once per day
    if 'last_picked' not in globals() or globals()['last_picked'] != today:
        globals()['last_picked'] = today
        acronym_choice = random.choice(acronyms)
    else:
        acronym_choice = None

    return acronym_choice

def send_random_acronym():
    acronym_of_day = get_random_acronym()

    if acronym_of_day:
        message = client.messages.create(
                body=acronym_of_day,
                from_='+18669907140',
                to='+12564794267'
            )
    else:
        print('No new message today')

    print("Message sent!")

send_random_acronym()
#Schedule the job to run every 1 minute
schedule.every(1).hours.do(send_random_acronym)

# Infinite loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
