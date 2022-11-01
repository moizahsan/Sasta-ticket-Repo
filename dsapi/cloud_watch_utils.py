import boto3

client = boto3.client("cloudwatch", region_name="ap-southeast-1",)


def api_hit_matric(url_path, status_code, response_time):
    client.put_metric_data(
        Namespace="datascience-api",
        MetricData=[
            {
                "MetricName": "api_hits",
                "Dimensions": [
                    {"Name": "path", "Value": url_path},
                    {"Name": "status", "Value": str(status_code)},
                ],
                "Value": response_time,
                "Unit": "Seconds",
            },
        ],
    )
