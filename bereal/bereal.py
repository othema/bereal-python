import requests
from bereal.constants import *
from bereal.models.feed import Feed
from bereal.models.user import Me
from bereal.models.realmoji import MyRealmoji


class BeReal:
    def __init__(self):
        self.login = Login(self)

        self.refresh_token = None
        self.token = None

        self.me = None
        self.feed = None

    def refresh(self):
        if self.refresh_token is None:
            raise Exception("No refresh token")
        res = requests.post(
            "https://securetoken.googleapis.com/v1/token",
            params={"key": GOOGLE_API_KEY},
            data={
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token"
            }
        ).json()

        self.token = res["id_token"]
        self.refresh_token = res["refresh_token"]
        return self.me()

    def me(self):
        res = requests.get(
            url=API_URL + "/person/me",
            headers={"authorization": self.token}
        ).json()
        return Me(res)

    def on_login(self):
        self.feed = Feed(self)


class Login:
    def __init__(self, bereal):
        self._bereal = bereal
        self._otp_session = None

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
        self._otp_session = res["sessionInfo"]
        return res

    def verify_code(self, code):
        if self._otp_session is None:
            raise Exception("No OTP session is open")
        res = requests.post(
            url="https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPhoneNumber",
            params={"key": GOOGLE_API_KEY},
            data={
                "sessionInfo": self._otp_session,
                "code": code,
                "operation": "SIGN_UP_OR_IN"
            }
        ).json()

        self._bereal.token = res["idToken"]
        self._bereal.refresh_token = res["refreshToken"]
        self._bereal.on_login()

    def with_tokens(self, token, refresh_token):
        self._bereal.token = token
        self._bereal.refresh_token = refresh_token
        self._bereal.on_login()
