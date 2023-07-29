import argparse
import boto3
from datetime import datetime, timedelta

# Create an argument parser
parser = argparse.ArgumentParser(description="Process AWS profile and time period.")

# Add an argument for the AWS profile
parser.add_argument(
    "--profile",
    metavar="P",
    type=str,
    nargs="?",
    default="default",
    help="The AWS profile to use",
)

# Add an argument for the start time in hours
parser.add_argument(
    "--hours",
    metavar="H",
    type=int,
    nargs="?",
    default=12,
    help="The start time in hours",
)

# Add an argument for the metric name
parser.add_argument(
    "--metric",
    metavar="M",
    type=str,
    nargs="?",
    default="Errors",
    help="The metric name to fetch (Errors, Invocations, Duration, Throttles, ConcurrentExecutions, etc )",
)


# Parse the command-line arguments
args = parser.parse_args()

# Create a session using your AWS profile
session = boto3.Session(profile_name=args.profile)

# Create CloudWatch and Lambda clients
cloudwatch = session.client("cloudwatch")
lambda_client = session.client("lambda")

# Get the current time and the time N hours ago in ISO 8601 format
end_time = datetime.utcnow()
start_time = end_time - timedelta(hours=args.hours)

# Get a list of all function names
response = lambda_client.list_functions()
function_names = [function["FunctionName"] for function in response["Functions"]]

# Iterate over all functions
for function_name in function_names:
    # Fetch the error metrics
    metric_statistics = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName=args.metric,  # use the provided metric
        Dimensions=[
            {"Name": "FunctionName", "Value": function_name},
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=args.hours * 3600,  # Convert hours to seconds for the period
        Statistics=["Sum"],
    )

    if (
        metric_statistics["Datapoints"]
        and metric_statistics["Datapoints"][0]["Sum"] > 0
    ):
        sum_stat = metric_statistics["Datapoints"][0]["Sum"]
        unit_stat = metric_statistics["Datapoints"][0]["Unit"]
        print(
            f"Function: {function_name} had {sum_stat} {args.metric} ({unit_stat}) in the last {args.hours} hours"
        )
        # print(metric_statistics)  # commented out as per request
