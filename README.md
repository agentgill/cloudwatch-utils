# Cloudwatch - Utils

This is a collection of useful scripts for managing & interacting with AWS CloudWatch Logs

## Get Started

Clone this repo

Create a virtualenv on MacOS and Linux:

```bash
python3 -m venv .venv
```

Install dependencies

```bash
pip install -r requirements.txt
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```bash
source .venv/bin/activate
```

## Print Log Events

Useful Python Script for outputing Cloudwatch Logs

```bash
Usage: print_log_events.py <LOG_GROUP_NAME> [--start=<START>] [--end=<END>]
       print_log_events.py -h --help

Options:
  <LOG_GROUP_NAME>    Name of the CloudWatch log group.
  --start=<START>     Only print events with a timestamp after this time.
  --end=<END>         Only print events with a timestamp before this time.
  -h --help           Show this screen.
```

Output logs to terminal

```bash
python print_log_events.py '/aws/lambda/mylambda' --start="25 Janurary at 00:00 am" --end="25 January 2023 at 23:50 pm"
```

Output logs to local file

```bash
python print_log_events.py '/aws/lambda/mylambda' --start="25 January at 00:00 am" --end="25 January 2023 at 23:59 pm" > cloudwatch.log
```

Credits to Alex

- [Alex Chan](https://github.com/alexwlchan)
- [Fetching CloudWatch Logs](https://alexwlchan.net/2017/fetching-cloudwatch-logs/)
