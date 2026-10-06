"""
Flask wrapper that serves the CompuTech page on Elastic Beanstalk.

The Elastic Beanstalk Python platform looks for a WSGI callable named
`application` in `application.py` by default, which is why the Flask
object is called `application` rather than `app`.
"""
from flask import Flask, send_from_directory

application = Flask(__name__, static_folder="static", static_url_path="")


@application.route("/")
def index():
    return send_from_directory(application.static_folder, "index.html")


@application.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    # Local testing only: python application.py -> http://127.0.0.1:5000
    application.run(debug=True)
