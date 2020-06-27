from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/')
def default():
    return "Hello"

@app.route('/newrequest', methods=['POST'])
def requestHandler():
        reqJson = request.get_json()
        print(reqJson)

"""@app.route('/delrequest', methods=['POST'])
def requestHandler():
        reqJson = request.get_json()
        print(reqJson)
"""

if __name__ == "main":
    app.run()