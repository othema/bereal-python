import pendulum
import requests
from uuid import uuid4
from bereal.constants import *
from bereal.models.feed import Feed
from bereal.models.user import Me
from PIL import Image
from io import BytesIO
from datetime import datetime
from urllib.parse import quote_plus
from json import dumps


class BeReal:
    def __init__(self):
        self.login = Login(self)

        self.refresh_token = None
        self.token = None

        self.feed = None

    def post_bereal(self, front_file, back_file, caption=None):
        # Thanks to: https://github.com/notmarek/BeFake/
        # And: https://github.com/s-alad/toofake/

        def extension(image):
            mime_type = Image.MIME[image.format]
            if mime_type != "image/jpeg":
                if not image.mode == "RGB":
                    image = image.convert("RGB")
            return image

        def get_data(image):
            image_data = BytesIO()
            image.save(image_data, format="JPEG", quality=90)
            return image_data.getvalue()

        def load_file(path):
            with open(path, "rb") as f:
                image = extension(Image.open(BytesIO(f.read())))
                size = image.size
                data = get_data(image)
                return data, size

        def upload_image(file_data, front_camera):
            name = f"Photos/{self.me().user_id}/bereal/{uuid4()}-{int(datetime.now().timestamp())}{'-secondary' if front_camera else ''}.jpg"
            data = {
                "cacheControl": "public,max-age=172800",
                "contentType": "image/webp",
                "metadata": {"type": "bereal"},
                "name": name
            }
            headers = {
                "x-goog-upload-protocol": "resumable",
                "x-goog-upload-command": "start",
                "x-firebase-storage-version": "ios/9.4.0",
                "x-goog-upload-content-type": "image/webp",
                "content-type": "application/json",
                "x-firebase-gmpid": "1:405768487586:ios:28c4df089ca92b89",
                "Authorization": f"Firebase {self.token}",
                "x-goog-upload-content-length": str(len(file_data)),
            }
            params = {"uploadType": "resumable", "name": name}

            uri = f"https://firebasestorage.googleapis.com/v0/b/storage.bere.al/o/{quote_plus(name)}"
            initial_res = requests.post(uri, headers=headers, params=params, data=dumps(data))

            if initial_res.status_code != 200:
                raise Exception(f"Error initiating upload: {initial_res.status_code}")

            upload_url = initial_res.headers["x-goog-upload-url"]
            upload_headers = {
                "x-goog-upload-command": "upload, finalize",
                "x-goog-upload-protocol": "resumable",
                "x-goog-upload-offset": "0",
                "content-type": "image/jpeg",
            }
            upload_res = requests.put(
                url=upload_url,
                headers=upload_headers,
                data=file_data
            )
            if upload_res.status_code != 200:
                raise Exception(f"Error uploading image: {upload_res.status_code}, {upload_res.text}")
            return upload_res.json()

        front_data, front_size = load_file(front_file)
        back_data, back_size = load_file(back_file)
        front_upload = upload_image(front_data, True)
        back_upload = upload_image(back_data, False)

        front_url = f"https://{front_upload['bucket']}/{front_upload['name']}"
        back_url = f"https://{back_upload['bucket']}/{back_upload['name']}"

        now = pendulum.now()
        taken_at = f"{now.to_date_string()}T{now.to_time_string()}Z"

        payload = {
            "isPublic": False,
            "isLate": False,
            "retakeCounter": 0,
            "takenAt": taken_at,
            # "location": location,
            "caption": caption if caption is not None else "",
            "backCamera": {
                "bucket": "storage.bere.al",
                "height": back_size[1],
                "width": back_size[0],
                "path": back_url.replace("https://storage.bere.al/", ""),
            },
            "frontCamera": {
                "bucket": "storage.bere.al",
                "height": front_size[1],
                "width": front_size[0],
                "path": front_url.replace("https://storage.bere.al/", ""),
            }
        }
        complete_res = requests.post(
            url=API_URL + "/content/post",
            json=payload,
            headers={"authorization": self.token}
        )
        return complete_res.json()

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
