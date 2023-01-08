from bereal.models.user import User
from datetime import datetime


class Comment:
    def __init__(self, data):
        self.comment_id = data["id"]
        self.user = User(data["user"])
        self.body = data["text"]
        self.creation_time = datetime.fromtimestamp(data["creationDate"]["_seconds"])
