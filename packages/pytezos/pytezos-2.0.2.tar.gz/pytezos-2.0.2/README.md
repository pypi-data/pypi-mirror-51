# PyTezos

[![PyPI version](https://badge.fury.io/py/pytezos.svg?)](https://badge.fury.io/py/pytezos)
[![Build Status](https://travis-ci.org/baking-bad/pytezos.svg?branch=master)](https://travis-ci.org/baking-bad/pytezos)
[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python SDK for Tezos: RPC, cryptography, operations, smart contract interaction

### Requirements

* git
* python 3.6+
* pip 19.0.1+

You will also probably need to install several cryptographic packets.

#### Linux

Use apt or your favourite package manager
```
$ sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev
```

#### MacOS

Install homebrew (if not yet)
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then the following libraries
```
$ brew tap cuber/homebrew-libsecp256k1
$ brew install libsodium libsecp256k1 gmp
```

#### Windows

1. Download MinGW from [https://sourceforge.net/projects/mingw/](https://sourceforge.net/projects/mingw/)
2. From "Basic Setup" choose `mingw-developer-toolkit` `mingw32-base` `mingw32-gcc-g++` `msys-base`
3. Make sure `C:\MinGW\bin` is added to your `PATH`
4. Download the latest libsodium-X.Y.Z-msvc.zip from [https://download.libsodium.org/libsodium/releases/](https://download.libsodium.org/libsodium/releases/).
5. Extract the Win32/Release/v120/dynamic/libsodium.dll fromt the zip file
6. Copy libsodium.dll to C:\Windows\System32\libsodium.dll

### Installation

```
$ pip install pytezos
```

### Usage

Read [quick start guide](https://baking-bad.github.io/pytezos), or just enjoy surfing the interactive documentation using Python console/Jupyter:
```python
>>> from pytezos import pytezos
>>> pytezos
<pytezos.client.PyTezosClient object at 0x7f904cf339e8>

Properties
.key -> tz1grSQDByRpnVs7sPtaprNZRp531ZKz6Jmm
.shell -> https://tezos-dev.cryptonomic-infra.tech/ (alphanet)

Helpers
.account()
.activate_account()
.ballot()
.contract()
.delegation()
.double_baking_evidence()
.double_endorsement_evidence()
.endorsement()
.operation()
.operation_group()
.origination()
.proposals()
.reveal()
.seed_nonce_revelation()
.transaction()
.using()
```

### About
The project was initially started by Arthur Breitman, now it's maintained by Baking Bad team.
PyTezos development is supported by Tezos Foundation.
