from app.models.user import SignUp
from app.models.notes import Notes
from config import DB_CONFIG

# Create Notes
def create_store(user_id, data):
    with DB_CONFIG.cursor() as cursor:
        query="INSERT INTO Notes(user_id, title, description) VALUES (%s, %s, %s)"
        values=(user_id, data["title"], data["description"])
        cursor.execute(query, values)
        DB_CONFIG.commit()
        return cursor.lastrowid
     
# Get Notes
def get_store(user_id):
    with DB_CONFIG.cursor() as cursor:
        query="SELECT * FROM Notes WHERE user_id=%s"
        cursor.execute(query, (user_id,))
        return cursor.fetchall()

# Update Notes
def update_store(user_id, notes_id, data):
    with DB_CONFIG.cursor() as cursor:
        query="UPDATE Notes SET title=%s, description=%s WHERE user_id=%s AND notes_id=%s"
        values=(data['title'], data["description"], user_id, notes_id)
        cursor.execute(query, values)
        DB_CONFIG.commit()
        return cursor.rowcount

# Delete Notes  
def delete_store(user_id, notes_id):
    with DB_CONFIG.cursor() as cursor:
        query="DELETE FROM Notes WHERE user_id=%s AND notes_id=%s"
        cursor.execute(query, (user_id, notes_id,))
        DB_CONFIG.commit()
        return cursor.rowcount