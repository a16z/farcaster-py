# farcaster-py

farcaster-py is a modern Python SDK for the Farcaster Protocol.

## Installation

```bash
pip install -U farcaster
```

or install with [Poetry](https://python-poetry.org/):

```bash
poetry add farcaster
```


## Usage

This SDK leverages the Warpcast API. [Warpcast](https://warpcast.com/) is one of many Farcaster [clients](https://github.com/a16z/awesome-farcaster#clients). As more APIs are created and hosted by different clients, these will be added to the SDK.

To use the Warpcast API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.

First, save your Farcaster mnemonic or private key to a `.env` file. Now you can initialize the client, and automatically connect to the Farcaster API!

```python
import os
from farcaster import Warpcast
from dotenv import load_dotenv

load_dotenv()

client = Warpcast(mnemonic=os.environ.get("<MNEMONIC_ENV_VAR>"))

print(client.get_healthcheck())
```

## Examples

Get a cast

```python
response = fcc.get_cast("0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f")
print(response.cast.author.username) # "dwr"
```

Publish a cast

```python
response = fcc.post_cast(text="Hello world!")
print(response.cast.hash) # "0x...."
```

Get a user by username

```python
user = fcc.get_user_by_username("mason")
print(user.username) # "mason"
```

Get a user's followers using a fid (farcaster ID)

```python
response = fcc.get_followers(fid=50)
print(response.users) # [user1, user2, user3]
```

Stream recent casts

```python
for cast in fcc.stream_casts():
    if cast:
        print(cast.text) # "Hello world!"
```

Get users who recently joined Farcaster

```python
response = fcc.get_recent_users()
print(response.users) # [user1, user2, user3]
```

Get your own user object

```python
user = fcc.get_me()
print(user.username) # "you"
```

Recast a cast

```python
response = fcc.recast("0x....")
print(response.cast.hash) # "0x...."
```

and many, many more things.

The full specification can be found on the [References](reference.md) page.

Still have questions? Chat with us [here](https://t.me/+aW_ucWeBVUZiNThh).
