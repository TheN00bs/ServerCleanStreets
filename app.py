from flask import Flask
from flask import request
import json
import pymongo
from flask import jsonify

global client, db, activeCollection, completedCollection, trashCollection




def connectToDB():
        global client, db, activeCollection, completedCollection, trashCollection
        client = pymongo.MongoClient("mongodb+srv://mahershi1999:mahershi1999@mahershi-6eyea.mongodb.net/<CleanStreets>?retryWrites=true&w=majority")
        db = client["CleanStreets"]
        activeCollection = db["activerequests"]
        completedCollection = db["competedrequests"]
        trashCollection = db["trashrequests"]

connectToDB()

app = Flask(__name__)

@app.route('/')
def default():
        return "Hello"

@app.route('/<email>')
def home(email):
        global activeCollection, completedCollection, trashCollection
        query = {"user": email}
        
        txt = {}
        reqHistory = list()
        
        doc = activeCollection.find(query)
        for x in doc:
                txt["id"] = str(x['_id'])
                txt["user"] = x['title']
                reqHistory.append(txt)

        doc = trashCollection.find(query)
        for x in doc:
                txt["id"] = str(x['_id'])
                txt["user"] = x['title']
                reqHistory.append(txt)
        doc = completedCollection.find(query)
        for x in doc:
                txt["id"] = str(x['_id'])
                txt["user"] = x['title']
                reqHistory.append(txt)

        x = jsonify(reqHistory)
        #x = json.dumps(reqHistory, cls=JSONEncoder)
        print(type(x))
        print(x)
        return x

        
        
        

@app.route('/newrequest', methods=['POST'])
def newRequest():
        reqJson = request.get_json()
        print(reqJson)

@app.route('/delrequest', methods=['POST'])
def deleteRequest():
        reqJson = request.get_json()
        print(reqJson)


if __name__ == "main":
        app.run()


