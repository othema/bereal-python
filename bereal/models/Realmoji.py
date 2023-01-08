class Realmoji:
    def __init__(self, data):
        self.url = data["media"]["url"]
        self.dimensions = (data["media"]["width"], data["media"]["height"])
        self.emoji = data["emoji"]
