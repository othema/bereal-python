from bereal.models.user import User
from datetime import datetime


class Comment:
    def __init__(self, data, datetime_override=None):
        self.comment_id = data["id"]
        self.user = User(data["user"])
        self.body = data["text"]
        if datetime_override is None:
            self.creation_time = datetime.fromtimestamp(data["creationDate"]["_seconds"])
        else:
            self.creation_time = datetime_override

