# Basic command line stopwatch

import argparse


import time
from datetime import date
import sys
import itertools
import gspread
from oauth2client.service_account import ServiceAccountCredentials


parser = argparse.ArgumentParser(description='Display a stopwatch while counting your breaths.  Upload the data to a Google Sheet.', epilog='Whatever an enemy can do to an enemy, or whatever a foe can do to a foe, what the ill directed mind can do to you... is even worse. --Buddha, Dhammapada, #42')
parser.add_argument("-b", "--breaths", help="Optional breath count #", dest="breath_count")
args = parser.parse_args()


def human_time(seconds):
    """Returns a human-friendly representation of the number of seconds."""
    assert seconds >= 0
    hours = seconds / (60 * 60)
    minutes = (seconds / 60) % 60
    seconds = seconds % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)


def print_time(ts):
    print('\r%s ' % human_time(ts), end='')
    sys.stdout.flush()
    time.sleep(1)


def stopwatch(breath_number):
    """Basic stopwatch.  Not perfectly accurate."""
    ts = 0
    try:
        for ts in itertools.count():
            print_time(ts)
    except KeyboardInterrupt:
        print('Session completed')
        update_sheet(ts, breath_number)


def update_sheet(ts, breath_number):
    myDate = date.today()
    dateStr = str(myDate.month) + "/" + str(myDate.day) + "/" + str(myDate.year)
    elapsed = human_time(ts)

    new_row = [dateStr, elapsed, breath_number]
    
    scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Breath-a07644f00238.json', scope)
    gc = gspread.authorize(credentials)

    wks = gc.open("Breath").sheet1
    wks.append_row(new_row, value_input_option='RAW')




if __name__ == "__main__":
    if args.breath_count:
        stopwatch(args.breath_count)
    else:
        print("Enter Breath Number")
        breath_number = input('-->')
        stopwatch(int(breath_number))
