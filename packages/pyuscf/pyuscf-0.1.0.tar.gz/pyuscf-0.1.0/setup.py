# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyuscf']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'pyuscf',
    'version': '0.1.0',
    'description': 'The Unofficial USCF Member Services Area (MSA) package.',
    'long_description': "The Unofficial USCF Member Service Area (MSA) API.\n\nThe United States Chess Federation (USCF) website for publicly available\nchess member information. The package is nothing more than a client, but there\nare some limitations on searching for chess members' information.\n\nVisit www.uschess.org for further information on the limitations.",
    'author': 'Juan Antonio Sauceda',
    'author_email': 'jasgordo@gmail.com',
    'url': 'https://gitlab.com/skibur/pyuscf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
