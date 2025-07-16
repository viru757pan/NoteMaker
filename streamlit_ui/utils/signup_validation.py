import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import DB_CONFIG  # ✅ Now it works

def is_valid_email(email):
    # Simple email regex
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password):
    # At least one lowercase, one uppercase, one digit, one special char, min 8 chars
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password) is not None

        
def get_user_id(id):
    with DB_CONFIG.cursor() as cursor:
        query="SELECT user_id FROM Login WHERE id = %s"
        cursor.execute(query, (id,))
        signUp_id = cursor.fetchone()
        
        if not signUp_id:
            return None
        else:
            return signUp_id