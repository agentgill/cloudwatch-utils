#!/usr/bin/env python3
import boto3
import argparse
from datetime import datetime


def main(aws_profile, metrics):
    session = boto3.Session(profile_name=aws_profile)
    client = session.client("ce", region_name="us-east-1")

    today = datetime.today()
    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": today.strftime("%Y-%m-01"),
            "End": today.strftime("%Y-%m-%d"),
        },
        Granularity="MONTHLY",
        Metrics=metrics,
        GroupBy=[
            {"Type": "DIMENSION", "Key": "SERVICE"},
        ],
    )
    costs = []
    for result in response["ResultsByTime"]:
        for group in result["Groups"]:
            cost_data = [group["Keys"][0]]
            for metric in metrics:
                cost_data.append(float(group["Metrics"][metric]["Amount"]))
            costs.append(cost_data)

    # Sort list of lists by first metric amount
    costs.sort(key=lambda x: x[1], reverse=True)

    # Print sorted costs
    for cost_data in costs:
        print(", ".join(str(amount) for amount in cost_data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get AWS cost and usage data for today."
    )
    parser.add_argument("--profile", type=str, help="AWS profile to use")
    parser.add_argument("metrics", nargs="+", help="Metrics to retrieve")
    args = parser.parse_args()
    main(args.profile, args.metrics)
