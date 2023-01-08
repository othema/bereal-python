from bereal import BeReal
from dotenv import load_dotenv
from os import getenv


def main():
    load_dotenv()

    bereal = BeReal()
    bereal.login.send_code(input("Enter phone number: "))
    bereal.login.verify_code(input("Enter verification code: "))

    print(bereal.me().realmojis)


main()
