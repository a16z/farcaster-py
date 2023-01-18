# farcaster-py

farcaster-py is a modern Python SDK for the Farcaster Protocol.

## Installation

```bash
pip install -U farcaster
```

or install with `Poetry`

```bash
poetry add farcaster
```


## Usage
To use the Farcaster API you need to generate an access token. Here is one way to do that:

First install eth-account and dotenv:
```bash
pip install eth-account python-dotenv # Or 'poetry add eth-account python-dotenv'
```

Then you can use a script like this to generate the access token. Note that you can increase the expiration date of the token if you don't want to worry about rotation.

```py title="script.py"
import time
import os

from farcaster import MerkleApiClient
from eth_account.account import Account
from dotenv import load_dotenv

load_dotenv()
Account.enable_unaudited_hdwallet_features()
ETH_ACCOUNT_SIGNER = Account.from_mnemonic(os.environ.get("<MNEMONIC_ENV_VAR>"))

client = MerkleApiClient(wallet=ETH_ACCOUNT_SIGNER)

expiry_ms = int(time.time() + 600)*1000 # This auth token will be valid for 10 minutes. You can increase this up to 1 year

access_token = client.create_new_auth_token(expires_at=expiry_ms)

print(access_token) # "MK-...."
```

Save the auth token somewhere like a `.env` file in your working directory.

From now on you can initialize your client like this:

```python
from farcaster import MerkleApiClient
from dotenv import load_dotenv

load_dotenv()

client = MerkleApiClient(access_token=os.environ.get("<AUTH_ENV_VAR>"))

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
