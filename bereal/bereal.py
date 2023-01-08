import requests
from bereal.constants import *
from bereal.models.Realmoji import Realmoji


class BeReal:
    def __init__(self):
        self.login = Login(self)
        self.token = None

        self.me = None

    def _get_me(self):
        res = requests.get(
            url=API_URL + "/person/me",
            headers={"authorization": self.token}
        ).json()
        self.me = Me(res)


class Me:
    def __init__(self, data):
        self.user_id = data["id"]
        self.phone_number = data["phoneNumber"]
        self.username = data["username"]
        self.full_name = data["fullname"]
        self.birthday = data["birthdate"]
        self.profile_picture = data["profilePicture"]["url"]
        self.realmojis = [Realmoji(realmoji) for realmoji in data["realmojis"]]


class Login:
    def __init__(self, bereal):
        self.bereal = bereal
        self.otp_session = None

    def send_code(self, phone_number):
        res = requests.post(
            url="https://www.googleapis.com/identitytoolkit/v3/relyingparty/sendVerificationCode",
            params={"key": GOOGLE_API_KEY},
            data={
                "phoneNumber": phone_number,
                "iosReceipt": IOS_RECEIPT,
                "iosSecret": IOS_SECRET
            },
            headers=HEADERS
        ).json()
        print(res)
        self.otp_session = res["sessionInfo"]
        return res

    def verify_code(self, code):
        if self.otp_session is None:
            raise Exception("No OTP session is open")
        res = requests.post(
            url="https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPhoneNumber",
            params={"key": GOOGLE_API_KEY},
            data={
                "sessionInfo": self.otp_session,
                "code": code,
                "operation": "SIGN_UP_OR_IN"
            }
        ).json()
        self.bereal.token = res["idToken"]
        self.bereal._get_me()

    def with_token(self, token):
        self.bereal.token = token
        self.bereal._get_me()
