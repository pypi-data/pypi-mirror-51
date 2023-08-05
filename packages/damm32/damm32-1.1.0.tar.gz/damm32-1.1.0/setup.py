# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['damm32']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'damm32',
    'version': '1.1.0',
    'description': 'A pure-python implementation of the Damm Algorithm in Base 32.',
    'long_description': '# Damm32\n\n[![CircleCI](https://circleci.com/gh/pyinv/damm32.svg?style=svg)](https://circleci.com/gh/pyinv/damm32)\n[![Maintainability](https://api.codeclimate.com/v1/badges/476968b8744ce5ed9ed3/maintainability)](https://codeclimate.com/github/pyinv/damm32/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/476968b8744ce5ed9ed3/test_coverage)](https://codeclimate.com/github/pyinv/damm32/test_coverage)\n\nPython implementation of the Damm Algorithm in Base 32\n\nBy default, it uses an alphabet as specified in [RFC 4648](https://tools.ietf.org/html/rfc4648) which contains 32 alphanumeric characters, with similar looking characters removed. The padding symbol is not included.\n\n## Installation\n\nThe package is available on [PyPI](https://pypi.org/project/damm32/) and can be installed using pip.\n\n`pip install damm32`\n\nAlternatively, you can clone the repository and use the module.\n\n## Usage\n\nThe module contains a single class called `Damm32`, this class implements the methods for the checksum.\n\n```\nfrom damm32 import Damm32\n\nd32 = Damm32()\n\ndigit = d32.calculate("HELLO")\n\nd32.verify("HELLO" + digit)\n\n```\n\nYou can also pass an list of length 32 to the constructor for the class to specify your alphabet.\n\n```\nfrom damm32 import Damm32\n\nd32 = Damm32([\'A\', \'B\', \'C\', \'D\', \'E\', \'F\', \'G\', \'H\', \'I\', \'J\', \'K\', \'L\', \'M\', \'N\', \'O\', \'P\', \'Q\', \'R\', \'S\', \'T\', \'U\', \'V\', \'W\', \'X\', \'Y\', \'Z\', \'2\', \'3\', \'4\', \'5\', \'6\', \'7\'])\n\n```\n',
    'author': 'Dan Trickey',
    'author_email': 'dan@trickey.io',
    'url': 'https://github.com/pyinv/damm32',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
