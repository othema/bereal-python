from bereal import BeReal
from dotenv import load_dotenv
from os import getenv


def main():
    load_dotenv()

    bereal = BeReal()
    # bereal.login.send_code(getenv("PHONE_NUMBER"))
    # bereal.login.verify_code(input("Enter verification code: "))
    bereal.login.with_token(getenv("TOKEN"))
    print(bereal.me.realmojis[0].url)


main()
