"""
MyFirstLambda - doubles a number.

Works with both ways the function gets invoked:
  1. Console test event:          {"number": 5}
  2. API Gateway HTTP API (v2.0):  GET /default/MyFirstLambda?number=20
     -> the value arrives in event["queryStringParameters"]["number"] as a string

Bug fixed from the original lab version: it only checked event["number"],
so every call through API Gateway returned "No number provided" even when
?number=20 was in the URL.
"""
import json


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    number = event.get("number")

    if number is None:
        params = event.get("queryStringParameters") or {}
        number = params.get("number")

    if number is None:
        return _response(400, {"message": "No number provided. Try ?number=5"})

    try:
        value = float(number)
    except (TypeError, ValueError):
        return _response(400, {"message": f"'{number}' is not a valid number"})

    doubled = value * 2
    if doubled.is_integer():
        doubled = int(doubled)

    return _response(200, {
        "message": "Hello from Lambda!",
        "input": number,
        "doubled_number": doubled,
    })
