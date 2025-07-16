import bcrypt
from config import DB_CONFIG

def user_validator(email, password):
    with DB_CONFIG.cursor() as cursor:
        query = "SELECT user_id, username, password FROM SignUp WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            db_password = user[2]  # Hashed password from DB

            # ✅ bcrypt password check
            if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                return {"user_id": user[0], "username": user[1]}

    return False  # Return False if user not found or password doesn't match


def user_validator_notes(user_id):
    with DB_CONFIG.cursor() as cursor:
        query="SELECT user_id FROM SignUp WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        signUp_id = cursor.fetchone()

        if not signUp_id:
            return False
        else:
            return True
