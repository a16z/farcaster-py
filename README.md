# farcaster-py

<div align="center">

[![Build status](https://github.com/a16z/farcaster-py/workflows/build/badge.svg?branch=master&event=push)](https://github.com/fmhall/farcaster/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/farcaster.svg)](https://pypi.org/project/farcaster/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/a16z/farcaster-py/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/a16z/farcaster-py/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/a16z/farcaster-py/releases)
[![License](https://img.shields.io/github/license/fmhall/farcaster)](https://github.com/a16z/farcaster-py/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

farcaster-py is a Python SDK for the Farcaster Protocol

</div>

## Installation

```bash
pip install -U farcaster
```

or install with `Poetry`

```bash
poetry add farcaster
```


## Usage
To access the Farcaster API you need to generate an access token. Here is one way to do that:

First install eth-account and dotenv:
```bash
pip install eth-account python-dotenv # Or 'poetry add eth-account python-dotenv'
```

Then you can use a script like this to generate the access token. Note that you can increase the expiration date of the token if you don't want to worry about rotation.

```python
import time
import os

from farcaster import MerkleApiClient
from farcaster.models import AuthParams
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from dotenv import load_dotenv

load_dotenv()
Account.enable_unaudited_hdwallet_features()
ETH_ACCOUNT_SIGNER: LocalAccount = Account.from_mnemonic(os.environ.get("<MNEMONIC_ENV_VAR>"))


now = int(time.time()*1000)
expiry = int(now + 600000) # This auth token will be valid for 10 minutes. You can increase this up to 1 year

client = MerkleApiClient(wallet=ETH_ACCOUNT_SIGNER)

auth_params = AuthParams(timestamp=now, expires_at=expiry)

response = client.create_new_auth_token(auth_params)

print(response)
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
response = fcc.get_cast(
        "0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f"
    )
print(response.cast.author.username) # "dwr"
```

Publish a cast

```python
from farcaster.models import CastsPostRequest

cast_body = CastsPostRequest(text="Hello world!")
response = fcc.post_cast(cast_body)
if response:
    print(response.cast.hash) # "0x...."
else:
    raise Exception("Failed to post cast")
```

Get a user by username

```python
response = fcc.get_user_by_username(
        "mason"
    )
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
from farcaster.models import CastsPostRequest

cast_body = CastsPostRequest(text="Hello world!")
response = fcc.post_cast(cast_body)
if response:
    print(response.cast.hash) # "0x...."
else:
    raise Exception("Failed to post cast")
```

and many, many more things. Documentation coming soon!



## 📈 Releases

You can see the list of available releases on the [GitHub Releases](https://github.com/fmhall/farcaster/releases) page.

We follow [Semantic Versions](https://semver.org/) specification.

We use [`Release Drafter`](https://github.com/marketplace/actions/release-drafter). As pull requests are merged, a draft release is kept up-to-date listing the changes, ready to publish when you’re ready. With the categories option, you can categorize pull requests in release notes using labels.

### List of labels and corresponding titles

|               **Label**               |  **Title in Releases**  |
| :-----------------------------------: | :---------------------: |
|       `enhancement`, `feature`        |       🚀 Features       |
| `bug`, `refactoring`, `bugfix`, `fix` | 🔧 Fixes & Refactoring  |
|       `build`, `ci`, `testing`        | 📦 Build System & CI/CD |
|              `breaking`               |   💥 Breaking Changes   |
|            `documentation`            |    📝 Documentation     |
|            `dependencies`             | ⬆️ Dependencies updates |

You can update it in [`release-drafter.yml`](https://github.com/fmhall/farcaster/blob/master/.github/release-drafter.yml).

GitHub creates the `bug`, `enhancement`, and `documentation` labels for you. Dependabot creates the `dependencies` label. Create the remaining labels on the Issues tab of your GitHub repository, when you need them.

## 🛡 License

[![License](https://img.shields.io/github/license/fmhall/farcaster)](https://github.com/fmhall/farcaster/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/fmhall/farcaster/blob/master/LICENSE) for more details.
