import os
from dotenv import load_dotenv
from bereal import BeReal


def main():
    load_dotenv()

    bereal = BeReal()

    token = os.getenv("TOKEN")
    refresh_token = os.getenv("REFRESH_TOKEN")

    if not token:
        print("Please set TOKEN and REFRESH_TOKEN in your .env file, or login with phone number:")
        # bereal.login.send_code(input("Enter phone number: "))
        # bereal.login.verify_code(input("Enter verification code: "))
        return

    # Login using saved tokens
    bereal.login.with_tokens(token, refresh_token)
    bereal.refresh()

    print("Logged in successfully!")

    # Fetch profile
    me = bereal.me()
    print(f"Username: {me.username}")
    print(f"Full name: {me.full_name}")

    # Fetch friends feed
    feed = bereal.feed.friends()
    print(f"Retrieved {len(feed)} posts from friends:")
    for post in feed:
        caption = f' - "{post.caption}"' if post.caption else ""
        print(f"  @{post.user.username}{caption}")


if __name__ == "__main__":
    main()
