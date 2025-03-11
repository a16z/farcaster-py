# farcaster-py

**Note**: This project is not actively maintained, but we welcome external contributions and forks. If you’d like to contribute, please open a PR or fork this repository.


<div align="center">

[![Build status](https://github.com/a16z/farcaster-py/workflows/build/badge.svg?branch=main&event=push)](https://github.com/a16z/farcaster-py/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/farcaster.svg)](https://pypi.org/project/farcaster/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/a16z/farcaster-py/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/a16z/farcaster-py/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/a16z/farcaster-py/releases)
[![License](https://img.shields.io/github/license/a16z/farcaster-py)](https://github.com/a16z/farcaster-py/blob/main/LICENSE)
![Coverage Report](assets/images/coverage.svg)
[![chat](https://img.shields.io/badge/chat-telegram-blue)](https://t.me/+aW_ucWeBVUZiNThh)

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

This SDK leverages the Warpcast API. [Warpcast](https://warpcast.com/) is one of many Farcaster [clients](https://github.com/a16z/awesome-farcaster#clients). As more APIs are created and hosted by different clients, these will be added to the SDK.

To use the Warpcast API you need to have a Farcaster account. We will use the mnemonic or private key of the Farcaster custody account (not your main wallet) to connect to the API.

First, save your Farcaster mnemonic or private key to a `.env` file. Now you can initialize the client, and automatically connect to the Farcaster API!

```python
import os
from farcaster import Warpcast
from dotenv import load_dotenv # can be installed with `pip install python-dotenv`

load_dotenv()

client = Warpcast(mnemonic=os.environ.get("<MNEMONIC_ENV_VAR>"))

print(client.get_healthcheck())
```

## Examples

Get a cast

```python
response = client.get_cast("0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f")
print(response.cast.author.username) # "dwr"
```

Publish a cast

```python
response = client.post_cast(text="Hello world!")
print(response.cast.hash) # "0x...."
```

Get a user by username

```python
user = client.get_user_by_username("mason")
print(user.username) # "mason"
```

Get a user's followers using a fid (farcaster ID)

```python
response = client.get_followers(fid=50)
print(response.users) # [user1, user2, user3]
```

Stream recent casts

```python
for cast in client.stream_casts():
    if cast:
        print(cast.text) # "Hello world!"
```

Get users who recently joined Farcaster

```python
response = client.get_recent_users()
print(response.users) # [user1, user2, user3]
```

Get your own user object

```python
user = client.get_me()
print(user.username) # "you"
```

Recast a cast

```python
response = client.recast("0x....")
print(response.cast.hash) # "0x...."
```

and many, many more things. The full specification can be found on the [Reference page](https://a16z.github.io/farcaster-py/reference).

*Please note that support for Python 3.8 is no longer actively maintained. Python 3.9, or 3.10+ are recommended.*
## 🛡 License

[![License](https://img.shields.io/github/license/a16z/farcaster-py)](https://github.com/a16z/farcaster-py/blob/main/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/a16z/farcaster-py/blob/main/LICENSE) for more details.

## Disclaimer

_This code is being provided as is. No guarantee, representation or warranty is being made, express or implied, as to the safety or correctness of the code. It has not been audited and as such there can be no assurance it will work as intended, and users may experience delays, failures, errors, omissions or loss of transmitted information. Nothing in this repo should be construed as investment advice or legal advice for any particular facts or circumstances and is not meant to replace competent counsel. It is strongly advised for you to contact a reputable attorney in your jurisdiction for any questions or concerns with respect thereto. a16z is not liable for any use of the foregoing, and users should proceed with caution and use at their own risk. See [our disclosures page](https://a16z.com/disclosures) for more info._
