from flask import Flask, jsonify, request, Blueprint
from app.services.user import create_signUp_service, create_login_service

user_bp = Blueprint("user_bp", __name__)

# SignUp User
@user_bp.route("/SignUp", methods=["POST"])
def create_signUp():
    data = request.get_json()
    res = create_signUp_service(data)

    if "error" in res:
        return jsonify(res), 404
    return jsonify({"message":"User Created Successfully!", "res":res["user_id"]}), 200

# Login User
@user_bp.route("/Login", methods=["POST"])
def create_login():
    data = request.get_json()
    res = create_login_service(data)

    if "error" in res:
        print('res:', res)
        return jsonify(res), 404
    # print('res/login:', res)
    return jsonify({"message":"User Login Successfull!", "id":res["id"], "user_id":res["user_id"]}), 200