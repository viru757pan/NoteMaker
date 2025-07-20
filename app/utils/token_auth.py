import jwt
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        print(auth_header)
        if not auth_header:
            return jsonify({"error": "Token Missing!"}), 401
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token Expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid User!"}), 401
        return f(user_id=user_id, *args, **kwargs)
    return decorated
        