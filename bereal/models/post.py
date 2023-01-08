from bereal.models.user import User
from bereal.models.comment import Comment
from bereal.models.realmoji import Realmoji
from datetime import datetime


class Post:
    def __init__(self, data):
        self.post_id = data["id"]
        self.user = User(data["user"])
        self.front_camera = data["photoURL"]
        self.back_camera = data["secondaryPhotoURL"]
        self.is_public = data["isPublic"]
        self.retakes = data["retakeCounter"]
        try:
            self.caption = data["caption"]
        except KeyError:
            self.caption = None
        self.creation_time = datetime.fromtimestamp(data["creationDate"]["_seconds"])
        self.comments = [Comment(comment) for comment in data["comment"]]
        self.realmojis = [Realmoji(realmoji) for realmoji in data["realMojis"]]

