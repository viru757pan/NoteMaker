class Notes:
    def __init__(self, notes_id, title, description):
        self.notes_id = notes_id
        self.title = title
        self.description = description
    
    def to_dict(self):
        return{
            "notes_id":self.notes_id,
            "title":self.title,
            "description":self.description
        }