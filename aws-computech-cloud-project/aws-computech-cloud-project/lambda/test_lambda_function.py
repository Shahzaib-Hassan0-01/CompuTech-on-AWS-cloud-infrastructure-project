"""Local tests: python -m unittest discover lambda"""
import json
import unittest

from lambda_function import lambda_handler


def body(resp):
    return json.loads(resp["body"])


class TestHandler(unittest.TestCase):
    def test_console_event(self):
        r = lambda_handler({"number": 5}, None)
        self.assertEqual(r["statusCode"], 200)
        self.assertEqual(body(r)["doubled_number"], 10)

    def test_api_gateway_query_string(self):
        event = {"queryStringParameters": {"number": "20"}}
        r = lambda_handler(event, None)
        self.assertEqual(r["statusCode"], 200)
        self.assertEqual(body(r)["doubled_number"], 40)

    def test_decimal(self):
        r = lambda_handler({"number": "2.5"}, None)
        self.assertEqual(body(r)["doubled_number"], 5)

    def test_missing_number(self):
        r = lambda_handler({"queryStringParameters": None}, None)
        self.assertEqual(r["statusCode"], 400)

    def test_not_a_number(self):
        r = lambda_handler({"number": "abc"}, None)
        self.assertEqual(r["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
