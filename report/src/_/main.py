from datetime import datetime, timedelta
import argparse
from typing import Callable, NoReturn
from pathlib import Path
import re

""" This function build_report takes two arguments files and order, both strings. It returns a tuple of two dictionaries
 - one contains information about all the racers, and the other contains information about only the fastest racers. This 
function reads input data from files and calculates the time differences between start and end times of each racer."""


def build_report(files: Path, order: str) -> [dict, dict]:
    start_file = files / 'start.log'
    end_file = files / 'end.log'
    abbreviations_file = files / 'abbreviations.txt'
    racers: dict = {}
    with open(start_file, 'r') as file:
        for line in file:
            time_start = re.search(r"\d{2}:\d{2}:\d{2}\.\d{3}", line)
            abr = line.strip()[:3]
            racers[abr] = {'time_start': time_start.group() if time_start else None}

    with open(end_file, 'r') as file:
        for line in file:
            time_end = re.search(r"\d{2}:\d{2}:\d{2}\.\d{3}", line)
            abr = line.strip()[:3]
            racers[abr]['time_end'] = time_end.group() if time_end else None

    with open(abbreviations_file, 'rb') as file:
        for line in file:
            line = line.rstrip(b'\r\n')
            line = line.decode('utf-8', 'ignore')
            abr, name, team = line.split('_')
            racers[abr]['name'] = name
            racers[abr]['team'] = team

    for abbrs, times in racers.items():
        start_time = datetime.strptime(times['time_start'], '%H:%M:%S.%f')
        end_time = datetime.strptime(times['time_end'], '%H:%M:%S.%f')
        time_diff = end_time - start_time
        racers[abbrs].update({'time_diff': time_diff})

        if time_diff > timedelta(0):
            racers[abbrs].update({'valid': "Time entry is valid"})
        else:
            racers[abbrs].update({'valid': "Time entry is invalid"})

    valid_entries = {abrs: info for abrs, info in racers.items() if info['valid'] == "Time entry is valid"}
    if order == 'asc':
        fastest_racers = dict(sorted(valid_entries.items(), key=lambda x: x[1]['time_diff']))
    else:
        fastest_racers = dict(sorted(valid_entries.items(), key=lambda x: x[1]['time_diff'], reverse=True))
    return racers, fastest_racers


"""The function print_report below takes the results of the best racers and print it. The first 15 racers printed before
the line. Only valid time entry is taken into account"""


def print_report(files: Path, order: str) -> NoReturn:
    racers = build_report(files, order)[1]
    report_lines = []
    for i, (abbrs, info) in enumerate(racers.items(), start=1):
        name = info['name']
        team = info['team']
        time_diff = info['time_diff']
        line = f"{i}. {abbrs} | {name.ljust(20)} | {team.ljust(30)} | {time_diff}"
        report_lines.append(line)

    if len(report_lines) >= 15:
        report_lines.insert(15, '-' * 100)

    report = '\n'.join(report_lines)
    print(report)


"""The function takes arguments in the command line and amend output. Based on the passed arguments it can print report, 
or print full info for a single driver, and change the sort order of the report."""


def print_driver_info(files: Path, order: str, driver: str) -> NoReturn:
    records = build_report(files, order)[0]
    matching_records = [record for record in records.values() if record["name"] == driver]
    if matching_records:
        for record in matching_records:
            print(f"Driver {driver} info:")
            for key, value in record.items():
                print(f"\t{key}: {value}")
    else:
        print(f"No records found for driver {driver}.")


def main() -> NoReturn:
    default_folder = Path(__file__).resolve().parent.parent.parent / 'data'
    parser = argparse.ArgumentParser(description='Print the report of Monaco Racing 2018')
    parser.add_argument('-f', '--files', default=default_folder, type=Path, help='Input path to folder')
    parser.add_argument('-o', '--order', choices=['asc', 'desc'], default='asc', help='Sorting order (default: asc)')
    parser.add_argument('-d', '--driver_info', type=str, help='Specify the driver name to print driver info')
    args = parser.parse_args()
    if args.driver_info:
        print_driver_info(args.files, args.order, args.driver_info)
    else:
        print_report(args.files, args.order)


if __name__ == "__main__":
    main()
