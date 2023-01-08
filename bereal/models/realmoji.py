from datetime import datetime


class MyRealmoji:
    def __init__(self, data):
        self.url = data["media"]["url"]
        self.emoji = data["emoji"]


class Realmoji:
    def __init__(self, data):
        from bereal.models.user import User  # To avoid circular import
        self.url = data["uri"]
        self.emoji = data["emoji"]
        self.user = User(data["user"])
        self.time = datetime.fromtimestamp(data["date"]["_seconds"])
