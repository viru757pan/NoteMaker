import bcrypt
from datetime import datetime
from config import DB_CONFIG

# SignUp Implementation
# Create User
def create_signUp_store(data):
    with DB_CONFIG.cursor() as cursor:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
        
        query = "INSERT INTO SignUp(username, email, password) VALUES (%s, %s, %s)"
        values = (data["username"], data["email"], hashed_password.decode('utf-8'))
        
        cursor.execute(query, values)
        DB_CONFIG.commit()
        return cursor.lastrowid, "SignUp created successfully"
    
# Login Implementation
# Create Login
def create_login_store(user_id, data):
    with DB_CONFIG.cursor() as cursor:
        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())

        login_time = datetime.now()
        query="INSERT INTO Login(user_id, email, password, login_time) VALUES (%s, %s, %s, %s)"
        values = (user_id, data['email'], hashed_password, login_time)

        cursor.execute(query, values)
        DB_CONFIG.commit()
        return cursor.lastrowid, "Login created successfully"