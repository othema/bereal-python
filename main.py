from bereal import BeReal
from dotenv import load_dotenv
from os import getenv


def main():
    load_dotenv()

    bereal = BeReal()
    print(bereal.login.send_code(getenv("PHONE_NUMBER")))
    bereal.login.verify_code(input("Enter verification code: "))


main()
