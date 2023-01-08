class User:
    def __init__(self, data):
        self.user_id = data["id"]
        self.username = data["username"]
        try:
            self.profile_picture = data["profilePicture"]["url"]
        except KeyError:
            self.profile_picture = None


class Me(User):
    def __init__(self, data):
        from bereal.models.realmoji import MyRealmoji  # To avoid circular import
        super().__init__(data)
        self.phone_number = data["phoneNumber"]
        self.full_name = data["fullname"]
        self.birthday = data["birthdate"]
        self.realmojis = [MyRealmoji(realmoji) for realmoji in data["realmojis"]]
