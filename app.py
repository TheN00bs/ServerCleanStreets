from flask import Flask
from flask import request
import json
import pymongo
from flask import jsonify
from bson import ObjectId

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
        reqHistory = []
        
        doc = activeCollection.find(query)
        for x in doc:
                print(x)
                txt["id"] = str(x['_id'])
                txt["title"] = x['title']
                print("TXT: " + str(txt))
                reqHistory.append(txt.copy())
                print("Req: " + str(reqHistory))

        doc = trashCollection.find(query)
        for x in doc:
                txt["id"] = str(x['_id'])
                txt["title"] = x['title']
                reqHistory.append(txt.copy())
        doc = completedCollection.find(query)
        for x in doc:
                txt["id"] = str(x['_id'])
                txt["title"] = x['title']
                reqHistory.append(txt.copy())

        print("Here...")
        print(reqHistory)
        x = jsonify(reqHistory)
        #x = json.dumps(reqHistory, cls=JSONEncoder)
        print(type(x))
        print(x)
        return x

        
@app.route('/<email>/<id>')
def returnReqData(email, id):
        global activeCollection, completedCollection, trashCollection
        id = ObjectId(id)
        doc = activeCollection.find_one({"_id": id})
        if doc is None:
                doc = completedCollection.find_one({"_id": id})
        if doc is None:
                doc = trashCollection.find_one({"_id": id})
        
        print(doc)
        print(type(doc))

        return doc


        
@app.route('/newrequest', methods=['POST'])
def newRequest():
        reqJson = request.get_json()
        print(reqJson)
        id = activeCollection.insert(reqJson)
        
        txt = dict()
        txt["title"] = reqJson["title"]
        txt["id"] = str(id)
        return txt
        


"""@app.route('/delrequest', methods=['POST'])
def deleteRequest():
        reqJson = request.get_json()
        print(reqJson)
        return "Success"
"""


if __name__ == "main":
        app.run()


