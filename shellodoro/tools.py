from operator import itemgetter
from datetime import datetime, timedelta
import subprocess
import json
from plyer import notification
from sys import platform


def send_notify(text: str):
    '''Function to sending notifications to user'''
    if platform == 'win32':
        notification.notify(
            message=text,
            app_name='Shellodoro',
            title='Shellodoro')
    # Linux and other UNIX OS`s
    else:
        subprocess.Popen(['notify-send', "Shellodoro", text,
                          '-a', 'Shellodoro',
                          '-i', 'terminal'])


def ftime(seconds: int):
    '''Time formatting function for pomodoro timer'''
    m = seconds//60
    s = seconds - m*60
    format_m = str(m) if m >= 10 else f'0{m}'
    format_s = str(s) if s >= 10 else f'0{s}'
    return f'{format_m}:{format_s}'


def to_graph(data: dict):
    data = data['days']
    cur_day = datetime.today().weekday() + 1
    now = datetime.now()
    week_ago = now - timedelta(days=7)
    for i in range(
            sorted(data, key=itemgetter('pomodoros'))[-1]['pomodoros'], 0, -1):
        print(
            '|',
            *['#' if day['pomodoros'] >= i else ' '
              for day in data[cur_day:] + data[:cur_day]], sep='   '
        )
    print('  ', *[day['name'][:3]
          for day in data[cur_day:] + data[:cur_day]])
    print('  ', week_ago.strftime('%d.%m.%Y'), '-', now.strftime('%d.%m.%Y'))


def add_pomodoro():
    with open('stats.json', 'r') as f:
        json_inner = f.read()
    with open('stats.json', 'w') as f:
        pomodoros = json.loads(json_inner)['days']
        cur_day = datetime.today().weekday()
        pomodoros[cur_day]['pomodoros'] += 1
        json.dump({'days': pomodoros}, f, indent=4)


def get_json(filename: str):
    with open(filename, 'r') as f:
        json_inner = f.read()
        obj = json.loads(json_inner)
    return obj
