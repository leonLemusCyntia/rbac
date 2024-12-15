from flask import Flask, jsonify, abort, request
import requests


app = Flask(__name__)
port = 3001


@app.route("/")
def home():
    return "Hello, this is a Payments Flask Microservice"

@app.route("/payments", methods=["GET", "POST"])
def payments():
    user_id = request.args["user_id"]
    if request.method == 'GET':
        if  get_rbac_auth(user_id, "READ_PAYMENTS") == 403:
            abort(403)
        return jsonify({"payments": [{"id": 3}, {"id": 4}]})
    elif request.method == 'POST':
        if  get_rbac_auth(user_id, "INSERT_PAYMENTS") == 403:
            abort(403)
        return jsonify({"payments": [{"id": 3}, {"id": 4}]})
    else:
        abort(501)
        

def get_rbac_auth(user_id, permission):
    return requests.get("http://rbac:3000/rbac-auth", params={"user_id": user_id, "permission": permission}).status_code


   

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)