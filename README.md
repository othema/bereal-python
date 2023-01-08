# Bereal API

## Installation
For now, you have to manually download the `bereal/` folder and add it to your project to use the API.
1. Download this repository (`git clone https://github.com/othema/bereal-python.git`)
2. Move the `bereal/` folder to your project

## Usage
All functions of the API are rooted in the `BeReal()` class. To start, instantiate it somewhere in your code.
```python
from bereal import BeReal

bereal = BeReal()
```

### Login
To use any functions of the API you must login first. There are two ways of doing this.
#### Login through phone verification
You would use this method if you haven't already logged in.
```python
from bereal import BeReal

bereal = BeReal()
bereal.login.send_code("<your phone number>")
bereal.login.verify_code(input("Enter verification code: "))
```

#### Login through saved ID's
You would use this method if you have already logged in the user and you don't want to send another verification code
```python
from bereal import BeReal

bereal = BeReal()
bereal.login.with_tokens(
    "<your token>",
    "<your refresh token>"
)
```

Your token and refresh token can be accessed through the client after a successful login like this:
```python
from bereal import BeReal

bereal = BeReal()
bereal.token
bereal.refresh_token
```

### Accessing your profile data
Your profile data can be accessed using the `me()` method. Here is an example how:
```python
from bereal import BeReal

bereal = BeReal()

# [Login]

me = bereal.me()

me.user_id
me.username
me.profile_picture  # URL to your profile picture
me.full_name
me.phone_number
me.birthday
me.realmojis  # Array of Realmoji() objects saved to your account
```

### Accessing your feed
As you may know, there are two feeds in BeReal. The friend feed and the discovery feed.

```python
from bereal import BeReal

bereal = BeReal()

# [Login]

friend_feed = bereal.feed.friends()
discovery_feed = bereal.feed.discovery()
```

Each function returns a list of `Post()` objects.

### Refreshing tokens
After a while, a login token can expire. To overcome this, you can call the `refresh()` method to generate a new login and refresh token without having to send another verification code.
```python
from bereal import BeReal

bereal = BeReal()

# [Login]

bereal.refresh()

bereal.token
bereal.refresh_token
```
You should save these tokens in a file if you want to allow the user to stay logged in throughout multiple uses of the program.

### `Post()` objects
Post objects can be returned from a feed retrieval and they contain data about a post.
```python
post = friend_feed[0]

# Methods
post.add_comment("<body>")  # Adds a comment to the post from the logged in user

# Attributes
post.post_id
post.back_camera
post.front_camera
post.caption  # The caption associated with the post
post.user  # A User() object of the user who posted
post.creation_time  # A datetime object
post.realmojis  # An array of Realemoji() objects
post.is_public  # If the post is viewable on the discovery feed
post.retakes  # Amount of retakes
post.comments  # An array of Comment() objects
```

### `Comment()` objects
**TODO**: Add deletion of comments through a `delete()` method

```python
comment = post.comments[0]

# Attributes
comment.comment_id
comment.user  # The author of the comment
comment.creation_time  # A datetime object
comment.body  # The comment text
```

### `Realmoji()` objects
Realmojis are reactions to a BeReal. A realmoji is an image of a user posing as one of 5 emojis:
- 👍
- 😀
- 😲
- 😍
- 😂

#### Accessing your saved realmojis
You can have saved realmojis on your account. When fetching these, 
```python
from bereal import BeReal

bereal = BeReal()

# [Login]

saved_realmoji = bereal.me().realmojis[0]
saved_realmoji.url  # URL of the realmoji image
saved_realmoji.emoji  # 👍, 😀, 😲, 😍 or 😂
```

#### Accessing realmojis on a post
```python
realmoji = post.realmojis[0]

realmoji.emoji  # 👍, 😀, 😲, 😍 or 😂
realmoji.url  # URL of the realmoji image
realmoji.user  # User who reacted with that realmoji
realmoji.time  # Datetime the post was reacted with the realmoji
```