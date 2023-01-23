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
To use the Farcaster API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.

First install dotenv:
```bash
pip install python-dotenv # Or 'poetry add python-dotenv'
```
Next, save your Farcaster mnemonic or private key to a `.env` file. Now you can initialize the client, and automatically connect to the Farcaster API!

```python
import os
from farcaster import MerkleApiClient
from dotenv import load_dotenv

load_dotenv()

client = MerkleApiClient(mnemonic=os.environ.get("<MNEMONIC_ENV_VAR>"))

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
from farcaster.models import CastsPostRequest

cast_body = CastsPostRequest(text="Hello world!")
response = fcc.post_cast(cast_body)
print(response.cast.hash) # "0x...."
```

Get a user by username

```python
response = fcc.get_user_by_username("mason")
print(response.user.username) # "mason"
```

Get a user's followers using a fid (farcaster ID)

```python
response = fcc.get_followers(fid=50)
print(response.users) # [user1, user2, user3]
```

Get users who recently joined Farcaster

```python
response = fcc.get_recent_users()
print(response.users) # [user1, user2, user3]
```

Get your own user object

```python
response = fcc.get_me()
print(response.user.username) # "you"
```

Recast a cast

```python
response = fcc.recast("0x....")
print(response.cast.hash) # "0x...."
```

and many, many more things.

The full specification can be found on the [References](reference.md) page.
