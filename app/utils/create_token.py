import jwt
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("JWT_SECRET_KEY")

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# print("Token:- ", generate_token(1))