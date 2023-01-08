import requests
from bereal.constants import *


class BeReal:
    def __init__(self):
        self.login = Login(self)
        self.token = None


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
