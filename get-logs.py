#!/usr/bin/env python3
# -*- encoding: utf-8

import boto3
import argparse
import maya
from datetime import datetime, timedelta
import os


def get_log_events(log_group, start_time=None, end_time=None):
    """Generate all the log events from a CloudWatch group.

    :param log_group: Name of the CloudWatch log group.
    :param start_time: Only fetch events with a timestamp after this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.
    :param end_time: Only fetch events with a timestamp before this time.
        Expressed as the number of milliseconds after midnight Jan 1 1970.

    """
    client = boto3.client("logs")
    kwargs = {
        "logGroupName": log_group,
        "limit": 10000,
    }

    if start_time is not None:
        kwargs["startTime"] = start_time
    if end_time is not None:
        kwargs["endTime"] = end_time

    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp["events"]
        try:
            kwargs["nextToken"] = resp["nextToken"]
        except KeyError:
            break


def milliseconds_since_epoch(time_string):
    dt = maya.when(time_string)
    seconds = dt.epoch
    return seconds * 1000


def today_start_end():
    now = datetime.now()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1, microseconds=-1)
    return (start.isoformat(), end.isoformat())


def create_log_filename(log_group, start_time, end_time):
    log_name = os.path.basename(log_group)
    start_time_str = datetime.fromtimestamp(start_time / 1000).strftime("%Y%m%d%H%M%S")
    end_time_str = datetime.fromtimestamp(end_time / 1000).strftime("%Y%m%d%H%M%S")
    return f"{log_name}_{start_time_str}_{end_time_str}.log"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print log event messages from a CloudWatch log group."
    )
    parser.add_argument("log_group", type=str, help="Name of the CloudWatch log group.")
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Only print events with a timestamp after this time. (defaults to the start of today)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Only print events with a timestamp before this time. (defaults to the end of today)",
    )

    args = parser.parse_args()

    log_group = args.log_group

    if args.start:
        try:
            start_time = milliseconds_since_epoch(args.start)
        except ValueError:
            exit(f"Invalid datetime input as --start: {args.start}")
    else:
        start_time, _ = today_start_end()
        start_time = milliseconds_since_epoch(start_time)

    if args.end:
        try:
            end_time = milliseconds_since_epoch(args.end)
        except ValueError:
            exit(f"Invalid datetime input as --end: {args.end}")
    else:
        _, end_time = today_start_end()
        end_time = milliseconds_since_epoch(end_time)

    log_filename = create_log_filename(log_group, start_time, end_time)

    print(f"log_group: {log_group}")
    print(f"log_filename: {log_filename}")

    with open(log_filename, "w") as f:
        f.write(f"start_time: {start_time}\n")
        f.write(f"end_time: {end_time}\n")

        print(f"start_time: {start_time}")
        print(f"end_time: {end_time}")

        logs = get_log_events(
            log_group=log_group, start_time=start_time, end_time=end_time
        )

        for event in logs:
            message = event["message"].rstrip()
            print(message)
            f.write(message + "\n")
