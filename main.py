from bereal import BeReal
from dotenv import load_dotenv
from os import getenv

SPAM_AMOUNT = 20


def main():
    load_dotenv()

    bereal = BeReal()
    # bereal.login.send_code(input("Enter phone number: "))
    # bereal.login.verify_code(input("Enter verification code: "))

    bereal.login.with_tokens(getenv("TOKEN"), getenv("REFRESH_TOKEN"))
    bereal.refresh()
    print(bereal.token)
    print(bereal.refresh_token)

    feed = bereal.feed.friends()
    for post in feed:
        if post.user.username == "izzygarbett":
            for _ in range(SPAM_AMOUNT):
                post.add_comment("Test")
                print("Spam")


main()
