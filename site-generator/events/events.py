#!/usr/bin/env python3
from calendar import monthcalendar
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import json


def get_last_weekday_of_mounth(year: int, month: int, n: int):

    month = monthcalendar(year, month)
    if month[-1][n]:
        return month[-1][-2]
    else:
        return month[-2][-2]


def new_event(name: str, location: str, time: str, date: str):
    return {
        "name": name,
        "location": location,
        "time": time,
        "date": date
    }


str_path = "./events.json"


def read_data(path=str_path):
    path = Path(path)
    if not path.exists():

        with open(path, "w") as file:
            file.write("[]")
        print("Created: " + str_path)

    with open(path, "r") as file:
        string = file.read()
        return json.loads(string)


def write_data(data, path=str_path):
    path = Path(path)
    with open(path, "w") as file:
        string = json.dumps(data, indent=4)
        file.write(string)


def new_command():
    data = read_data()
    event = new_event(input("Name: "), input("Location: "),
                      input("Time: "), input("Date: "))

    data.append(event)
    write_data(data)


def date_time_from_event(event):
    d, m = event['date'].split('/')
    return datetime(2024, int(m), int(d))


def valid_event(event):
    event_time = date_time_from_event(event)
    yesterday = datetime.today() - timedelta(days=1)
    return event_time >= yesterday


def gen_command(args):
    data = read_data(args.input)
    events = []

    for event_data in data:

        # Should be a string
        a = event_data['date'].split()
        if len(a) == 3:
            interval, pos, day = a
            if interval == "every" and pos == "last" and day == "sat":
                for n in range(0, args.count):
                    event = new_event(**event_data)
                    date = datetime.now()

                    y = date.year + n // 12
                    m = (date.month + n) % 12

                    last_sat = get_last_weekday_of_mounth(
                        y, m, 5)
                    event['date'] = str(last_sat) + '/' + str(m)
                    events.append(event)
            else:
                print("WIP")
                exit()
        else:
            events.append(event_data)

    events = filter(valid_event, events)
    events = sorted(events, key=date_time_from_event)
    write_data(events, args.output)


parser = argparse.ArgumentParser(description='Event handeling helper')
subparsers = parser.add_subparsers(required=True)

gen_parser = subparsers.add_parser('gen', help='gen')

gen_parser.add_argument('-c', '--count', type=int, default=3,
                        help="Amount of mounths to generate")

gen_parser.add_argument('-out', '--output', type=str, default='./out.json',
                        help="Output file")

gen_parser.add_argument('-in', '--input', type=str, default='./events.json',
                        help="Input file")

gen_parser.set_defaults(func=gen_command)

new_parser = subparsers.add_parser('new', help='new')
new_parser.set_defaults(func=new_command)


args = parser.parse_args()
args.func(args)
