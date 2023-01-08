import requests
from bereal.constants import *
from bereal.models.post import Post


class Feed:
    def __init__(self, bereal):
        self._bereal = bereal

    def friends(self):
        res = requests.get(
            url=API_URL + "/feeds/friends",
            headers={"authorization": self._bereal.token}
        ).json()
        return [Post(post, self._bereal) for post in res]

    def discovery(self):
        res = requests.get(
            url=API_URL + "/feeds/discovery",
            headers={"authorization": self._bereal.token}
        ).json()
        return [Post(post, self._bereal) for post in res["posts"]]
