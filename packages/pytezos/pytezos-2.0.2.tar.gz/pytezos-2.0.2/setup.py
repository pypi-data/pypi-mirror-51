# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytezos',
 'pytezos.michelson',
 'pytezos.operation',
 'pytezos.rpc',
 'pytezos.tools']

package_data = \
{'': ['*'], 'pytezos.tools': ['templates/*']}

install_requires = \
['base58>=1.0.3,<2.0.0',
 'fastecdsa>=1.7.1,<2.0.0',
 'loguru',
 'mnemonic',
 'netstruct',
 'pendulum',
 'ply',
 'pyblake2>=1.1.2,<2.0.0',
 'pysodium>=0.7.1,<0.8.0',
 'requests>=2.21.0,<3.0.0',
 'secp256k1>=0.13.2,<0.14.0',
 'simplejson',
 'tqdm']

setup_kwargs = {
    'name': 'pytezos',
    'version': '2.0.2',
    'description': 'Python toolkit for Tezos',
    'long_description': '# PyTezos\n\n[![PyPI version](https://badge.fury.io/py/pytezos.svg?)](https://badge.fury.io/py/pytezos)\n[![Build Status](https://travis-ci.org/baking-bad/pytezos.svg?branch=master)](https://travis-ci.org/baking-bad/pytezos)\n[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](https://www.python.org)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nPython SDK for Tezos: RPC, cryptography, operations, smart contract interaction\n\n### Requirements\n\n* git\n* python 3.6+\n* pip 19.0.1+\n\nYou will also probably need to install several cryptographic packets.\n\n#### Linux\n\nUse apt or your favourite package manager\n```\n$ sudo apt install libsodium-dev libsecp256k1-dev libgmp-dev\n```\n\n#### MacOS\n\nInstall homebrew (if not yet)\n```\n$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"\n```\n\nThen the following libraries\n```\n$ brew tap cuber/homebrew-libsecp256k1\n$ brew install libsodium libsecp256k1 gmp\n```\n\n#### Windows\n\n1. Download MinGW from [https://sourceforge.net/projects/mingw/](https://sourceforge.net/projects/mingw/)\n2. From "Basic Setup" choose `mingw-developer-toolkit` `mingw32-base` `mingw32-gcc-g++` `msys-base`\n3. Make sure `C:\\MinGW\\bin` is added to your `PATH`\n4. Download the latest libsodium-X.Y.Z-msvc.zip from [https://download.libsodium.org/libsodium/releases/](https://download.libsodium.org/libsodium/releases/).\n5. Extract the Win32/Release/v120/dynamic/libsodium.dll fromt the zip file\n6. Copy libsodium.dll to C:\\Windows\\System32\\libsodium.dll\n\n### Installation\n\n```\n$ pip install pytezos\n```\n\n### Usage\n\nRead [quick start guide](https://baking-bad.github.io/pytezos), or just enjoy surfing the interactive documentation using Python console/Jupyter:\n```python\n>>> from pytezos import pytezos\n>>> pytezos\n<pytezos.client.PyTezosClient object at 0x7f904cf339e8>\n\nProperties\n.key -> tz1grSQDByRpnVs7sPtaprNZRp531ZKz6Jmm\n.shell -> https://tezos-dev.cryptonomic-infra.tech/ (alphanet)\n\nHelpers\n.account()\n.activate_account()\n.ballot()\n.contract()\n.delegation()\n.double_baking_evidence()\n.double_endorsement_evidence()\n.endorsement()\n.operation()\n.operation_group()\n.origination()\n.proposals()\n.reveal()\n.seed_nonce_revelation()\n.transaction()\n.using()\n```\n\n### About\nThe project was initially started by Arthur Breitman, now it\'s maintained by Baking Bad team.\nPyTezos development is supported by Tezos Foundation.\n',
    'author': 'Michael Zaikin',
    'author_email': 'mz@baking-bad.org',
    'url': 'https://baking-bad.github.io/pytezos/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
