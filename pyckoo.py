from datetime import datetime, timedelta
import time 
import winsound
import pyttsx3
import sched
import sys

DAY = 86400
HOUR = 3600
MIN = 60
tts = pyttsx3.init()
tts.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
tts.setProperty('rate', 150)
tts.setProperty('volume', 1.25)
scheduler = sched.scheduler(time.time, time.sleep)
alarm_filename = 'alarm.wav'
type_of_alarm = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] is not None else 'code'

def get_time_in_string(hour, min):
    if hour == 12 and min == 0: return "it's noon"
    if hour == 0 and min == 0: return "it's midnight"
    hour_12 = 12 if hour == 12 else hour % 12
    print(hour_12)
    next_hour_12 = 1 if hour_12 == 12 else hour_12 + 1
    print(next_hour_12)
    match min:
        case 0:  return "%s o'clock." % (hour_12)
        case 1:  return "1 minute past %s o'clock." % (hour_12)
        case 15: return "quarter past %s o'clock." % (hour_12)
        case 30: return "half past %s o'clock." % (hour_12)
        case 45: return "quarter to %s o'clock." % (next_hour_12)
        case 59: return "1 minute to o'clock." % (next_hour_12)
    if min < 30 and min > 1: return "%s minutes past %s o'clock." % (min, hour_12)
    if min > 30 and min < 59: return "%s minutes to %s o'clock." % (60 - min, next_hour_12)
    raise Exception('No such time: %s hours and %s minutes.' % (hour, min))

def read_aloud(text):
    tts.say(text)
    tts.runAndWait()

def schedule_next():
    curr_time = time.localtime()
    curr_hour = curr_time.tm_hour
    curr_min = curr_time.tm_min
    curr_sec = curr_time.tm_sec
    delta = (timespan_in_min - curr_min % timespan_in_min) * MIN - curr_sec

    time_text = get_time_in_string(curr_hour, curr_min)
    winsound.PlaySound(alarm_filename, winsound.SND_FILENAME)
    read_aloud(time_text)
    scheduler.enter(delta, 1, schedule_next)
    scheduler.run()

def play_alarm():
    winsound.PlaySound(alarm_filename, winsound.SND_FILENAME)

def play_alarm_until():
    winsound.PlaySound(alarm_filename, winsound.SND_FILENAME + winsound.SND_LOOP + winsound.SND_ASYNC)
    wait_input_to_exit = input('Press enter to exit.')

def timer(hour=0, min=0, sec=0):
    delta = hour * HOUR + min * MIN + sec
    scheduler.enter(delta, 1, play_alarm)
    scheduler.run()

def alarm(hour, min):
    curr_time = time.localtime()
    curr_time_sec_total = curr_time.tm_hour * HOUR + curr_time.tm_min * MIN + curr_time.tm_sec
    alarm_time = hour * HOUR + min * MIN 
    if curr_time_sec_total < alarm_time:
        scheduler.enter(alarm_time - curr_time_sec_total, 1, play_alarm_until)
    else:    
        scheduler.enter(DAY - curr_time_sec_total + alarm_time, 1, play_alarm)
    scheduler.run()

if type_of_alarm == 'cuckoo':
    timespan_in_min = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] is not None else int('15')
    timespan_in_sec = timespan_in_min * MIN
    schedule_next()
elif type_of_alarm == 'timer':
    alarm_time = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] is not None else '0:01:00'
    hour, min, sec = [int(x) for x in alarm_time.split(':')]
    timer(hour, min, sec)
elif type_of_alarm == 'alarm1':
    alarm_time = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] is not None else '1:23'
    hour, min = [int(x) for x in alarm_time.split(':')]
    alarm(hour, min)
elif type_of_alarm == 'code':
    pass
else: raise Exception('No such timer was implemented')
