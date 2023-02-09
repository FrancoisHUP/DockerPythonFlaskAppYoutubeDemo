from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    a = "hey "  + "its working !"
    return "<p>Hello, World! :D " + a + "</p>"
