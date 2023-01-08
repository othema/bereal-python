from bereal import BeReal
from dotenv import load_dotenv
from os import getenv


def main():
    load_dotenv()

    bereal = BeReal()
    # bereal.login.send_code(getenv("PHONE_NUMBER"))
    # bereal.login.verify_code(input("Enter verification code: "))
    bereal.login.with_tokens(getenv("TOKEN"), getenv("REFRESH_TOKEN"))
    feed = bereal.feed.friends()

    for post in feed:
        print(f"{post.user.username}: {post.caption} ({post.back_camera})")
        for comment in post.comments:
            print(f"  - {comment.user.username}: {comment.body}")


main()
