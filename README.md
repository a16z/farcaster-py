# farcaster

<div align="center">

[![Build status](https://github.com/fmhall/farcaster/workflows/build/badge.svg?branch=master&event=push)](https://github.com/fmhall/farcaster/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/farcaster.svg)](https://pypi.org/project/farcaster/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/fmhall/farcaster/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/fmhall/farcaster/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/fmhall/farcaster/releases)
[![License](https://img.shields.io/github/license/fmhall/farcaster)](https://github.com/fmhall/farcaster/blob/master/LICENSE)
![Coverage Report](assets/images/coverage.svg)

farcaster is a Python  SDK for the Farcaster Protocol

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
Set ENV vars:

`RINKEBY_PKEY`: Your private key

`RINKEBY_NETWORK_ADDR`: Alchemy, Infura, or local RPC for Rinkeby

```python
import os
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from farcaster.client import FarcasterClient

ETH_ACCOUNT_SIGNATURE: LocalAccount = Account.from_key(os.environ.get("RINKEBY_PKEY"))

fcc = FarcasterClient(
    os.getenv("RINKEBY_NETWORK_ADDR"), signature_account=ETH_ACCOUNT_SIGNATURE
)

print(fcc.get_profile("dwr"))
```
## Examples

### Get a profile from a username
```python
fcc.get_profile("dwr")
```
### Get casts from a username
```python
fcc.get_casts("dwr")
### Verify a cast
```python
casts = fcc.get_casts("v")
fcc.verify_cast(casts[-1])
```
### Get host address from a username
```python
fcc.get_host_addr("dwr")
```
### Get user from an address
```python
fcc.lookup_by_address("0xC6C0b79d0034A9A44c01c7695EaE26c9A7d23e40")
```
### Get username from an address
```python
fcc.get_username("0xC6C0b79d0034A9A44c01c7695EaE26c9A7d23e40")
```
### Get all users
```python
fcc.get_all_users()
```
### Get all usernames
```python
fcc.get_all_usernames()
```
### Publish a Cast
```python
fcc.publish_cast("Hello world! This cast was published from the Python SDK")
```
### Register a user
```python
fcc.register("xxx")
```
### Transfer an account to a new address
```python
fcc.transfer("xxx")
```


## Makefile usage

[`Makefile`](https://github.com/fmhall/farcaster/blob/master/Makefile) contains a lot of functions for faster development.

<details>
<summary>1. Download and remove Poetry</summary>
<p>

To download and install Poetry run:

```bash
make poetry-download
```

To uninstall

```bash
make poetry-remove
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

Install requirements:

```bash
make install
```

Pre-commit hooks coulb be installed after `git init` via

```bash
make pre-commit-install
```

</p>
</details>

<details>
<summary>3. Codestyle</summary>
<p>

Automatic formatting uses `pyupgrade`, `isort` and `black`.

```bash
make codestyle

# or use synonym
make formatting
```

Codestyle checks only, without rewriting files:

```bash
make check-codestyle
```

> Note: `check-codestyle` uses `isort`, `black` and `darglint` library

Update all dev libraries to the latest version using one comand

```bash
make update-dev-deps
```

<details>
<summary>4. Code security</summary>
<p>

```bash
make check-safety
```

This command launches `Poetry` integrity checks as well as identifies security issues with `Safety` and `Bandit`.

```bash
make check-safety
```

</p>
</details>

</details>

<details>
<summary>5. Type checks</summary>
<p>

Run `mypy` static type checker

```bash
make mypy
```

</p>
</details>

<details>
<summary>6. Tests with coverage badges</summary>
<p>

Run `pytest`

```bash
make test
```

</p>
</details>

<details>
<summary>7. All linters</summary>
<p>

Of course there is a command to ~~rule~~ run all linters in one:

```bash
make lint
```

the same as:

```bash
make test && make check-codestyle && make mypy && make check-safety
```

</p>
</details>

<details>
<summary>8. Docker</summary>
<p>

```bash
make docker-build
```

which is equivalent to:

```bash
make docker-build VERSION=latest
```

Remove docker image with

```bash
make docker-remove
```

More information [about docker](https://github.com/fmhall/farcaster/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup</summary>
<p>
Delete pycache files

```bash
make pycache-remove
```

Remove package build

```bash
make build-remove
```

Delete .DS_STORE files

```bash
make dsstore-remove
```

Remove .mypycache

```bash
make mypycache-remove
```

Or to remove all above run:

```bash
make cleanup
```

</p>
</details>

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
