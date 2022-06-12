from flask import Flask

app = Flask(__name__)


@app.route("/test-endpoint")
def test_endpoint():
    return {"text": "This is the response from the Flask backend"}
