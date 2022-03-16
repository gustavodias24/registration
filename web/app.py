from flask import Flask,request,jsonify
from pymongo import MongoClient
from flask_cors import CORS
import bcrypt

client = MongoClient("mongodb://db:27017")
db2 = client.aNewDB
db = client.SimilarityDB
count = db2['count']
users = db['users']

app = Flask(__name__)
CORS(app)

count.insert_one({
    'count':0
})
def userExist(username):
    if users.find({"username":username})[0]["password"] != 0:
        return True
    else:
        return False

@app.route("/",methods=["GET"])
def acess():
    prev = count.find({})[0]['count']
    newb = prev + 1
    count.update_one({},{"$set":{"count":newb}})
    return jsonify({
        "status":200,
        "count":newb
    })

@app.route("/restart",methods=["GET"])
def restart():
    count.update_one({}, {"$set": {"count": 0}})
    return jsonify({
        "status":200,
        "msg":"restert with exit!"
    })


@app.rout("/set",methods=["POST"])
def set():
    date = request.get_json()
    n = date['n']

@app.route("/register",methods=["POST"])
def register():
    datas = request.get_json()

    username = datas["username"]
    password = datas["password"]

    if userExist(username):
        retjson = {
            "status":301,
            "msg":"user as exist"
        }
        return jsonify(retjson)

    hash_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

    users.insert_one({
        "username": username,
        "password": hash_pw,
        "tokens": 6
    })

    return jsonify({
        "status": 200,
        "msg": f"username {username} create!"
    })

@app.route("/consult",methods=["GET"])
def cosult():
    return jsonify({"users" : users.find({})})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    #app.run()
