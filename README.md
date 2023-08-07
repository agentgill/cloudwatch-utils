# AWS CloudWatch - Utils

This is a collection of useful scripts for managing & interacting with AWS CloudWatch Logs & Metrics

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

## Get CloudWatch Log Events

Useful Python Script for outputing Cloudwatch Logs

```bash
usage: get-logs.py [-h] [--start START] [--end END] log_group

Print log event messages from a CloudWatch log group.

positional arguments:
  log_group      Name of the CloudWatch log group.

options:
  -h, --help     show this help message and exit
  --start START  Only print events with a timestamp after this time. (defaults to the start of today)
  --end END      Only print events with a timestamp before this time. (defaults to the end of today)
```

Output logs to terminal

```bash
python get_logs.py '/aws/lambda/mylambda' --start="25 Janurary at 00:00 am" --end="25 January 2023 at 23:50 pm"
```

```bash
python get_logs.py '/aws/lambda/mylambda' --start=Yesterday --end=Now
```

Output logs to local file

```bash
python get_logs.py '/aws/lambda/mylambda' --start="25 January at 00:00 am" --end="25 January 2023 at 23:59 pm" > cloudwatch.log
```

Credits to Alex

- [Alex Chan](https://github.com/alexwlchan)
- [Fetching CloudWatch Logs](https://alexwlchan.net/2017/fetching-cloudwatch-logs/)

## Get CloudWatch Metrics

Useful Python Script for outputing Cloudwatch Mertics. Example easily identify errors counts by functions.

```bash
usage: get-metrics.py [-h] [--profile [P]] [--hours [H]] [--metric [M]]

Process AWS profile and time period.

options:
  -h, --help     show this help message and exit
  --profile [P]  The AWS profile to use
  --hours [H]    The start time in hours
  --metric [M]   The metric name to fetch (Errors, Invocations, Duration, Throttles, ConcurrentExecutions, etc
```

## Get Cost Usage Metrics

Useful Python Script for outputing Daily Cost Usage Metrics

```bash
usage: get-cost-usage.py [-h] [--profile PROFILE] [metrics ...]

Get AWS cost and usage data for today.

positional arguments:
  metrics            Metrics to retrieve (UnblendedCost, BlendedCost, UsageQuantity, etc))

options:
  -h, --help         show this help message and exit
  --profile PROFILE  AWS profile to use
```
