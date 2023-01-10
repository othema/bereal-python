from bereal.models.user import User
from bereal.models.comment import Comment
from bereal.models.realmoji import Realmoji
from datetime import datetime
from bereal.constants import *
import requests


class Post:
    def __init__(self, data, bereal, creation_override=None):
        self._bereal = bereal

        self.post_id = data["id"]
        self.user = User(data["user"])
        self.front_camera = data["secondaryPhotoURL"]
        self.back_camera = data["photoURL"]
        self.is_public = data["isPublic"]
        self.retakes = data["retakeCounter"]
        try:
            self.caption = data["caption"]
        except KeyError:
            self.caption = None
        if creation_override is None:
            self.creation_time = datetime.fromtimestamp(data["creationDate"]["_seconds"])
        else:
            self.creation_time = creation_override
        self.comments = [Comment(comment) for comment in data["comment"]]
        self.realmojis = [Realmoji(realmoji) for realmoji in data["realMojis"]]

    def add_comment(self, body):
        res = requests.post(
            url=API_URL + "/content/comments",
            data={"content": body},
            params={"postId": self.post_id},
            headers={"authorization": self._bereal.token}
        ).json()
        return Comment({  # The comment route returns a different format of comment so we need to format it ourselves
            "id": res["id"],
            "user": res["user"],
            "text": res["content"]
        }, datetime_override=res["postedAt"])

