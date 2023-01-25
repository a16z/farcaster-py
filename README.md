# farcaster-py

<div align="center">

[![Build status](https://github.com/a16z/farcaster-py/workflows/build/badge.svg?branch=master&event=push)](https://github.com/a16z/farcaster-py/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/farcaster.svg)](https://pypi.org/project/farcaster/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/a16z/farcaster-py/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/a16z/farcaster-py/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/a16z/farcaster-py/releases)
[![License](https://img.shields.io/github/license/a16z/farcaster-py)](https://github.com/a16z/farcaster-py/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

farcaster-py is a modern Python SDK for the Farcaster protocol<br></br>

Full documentation can be found [here](https://a16z.github.io/farcaster-py)

</div>

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

and many, many more things. The full specification can be found on the [Reference page](https://a16z.github.io/farcaster-py/reference).

## 🛡 License

[![License](https://img.shields.io/github/license/fmhall/farcaster)](https://github.com/a16z/farcaster-py/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/a16z/farcaster-py/blob/main/LICENSE) for more details.
