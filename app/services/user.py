from app.stores.user import create_signUp_store, create_login_store
from app.utils.user_validation import user_validator
from app.utils.create_token import generate_token

# create signUp
def create_signUp_service(data):
    try:
        result = create_signUp_store(data)
        if result:
            return {"user_id": result[0], "message": result[1]}
    except Exception as e:
        return {"error":str(e)}


def create_login_service(data):
    try:
        user_data = user_validator(data['email'], data['password'])
        if not user_data:
            return {"error": "Invalid email or password"}

        user_id = user_data['user_id']
        # result = create_login_store(user_id, data)
        token = generate_token(user_id)
        # print("res: ", result)
        # return {"id": result[0], "user_id": user_id, "message": result[1], "token": token}
        return {"user_id": user_id, "message": "User Login Successfull!", "token": token}
    except Exception as e:
        print('Login Error:', str(e))
        return {"error": str(e)}