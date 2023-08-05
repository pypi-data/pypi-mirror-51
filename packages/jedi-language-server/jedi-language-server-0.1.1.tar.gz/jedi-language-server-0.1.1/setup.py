# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jedi_language_server']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'jedi>=0.15.1,<0.16.0', 'pygls>=0.8.0,<0.9.0']

entry_points = \
{'console_scripts': ['jedi-language-server = jedi_language_server.cli:cli']}

setup_kwargs = {
    'name': 'jedi-language-server',
    'version': '0.1.1',
    'description': 'A language server for Jedi!',
    'long_description': '# jedi-language-server\n\n[![image-version](https://img.shields.io/pypi/v/jedi-language-server.svg)](https://python.org/pypi/jedi-language-server)\n[![image-license](https://img.shields.io/pypi/l/jedi-language-server.svg)](https://python.org/pypi/jedi-language-server)\n[![image-python-versions](https://img.shields.io/pypi/pyversions/jedi-language-server.svg)](https://python.org/pypi/jedi-language-server)\n\nA [Language Server](https://microsoft.github.io/language-server-protocol/) for [Jedi](https://jedi.readthedocs.io/en/latest/).\n\n## Installation\n\n```bash\n# With pip\npip install jedi-language-server\n\n# With poetry\npoetry add jedi-language-server\n```\n\n## Motivation\n\nMy motivation goes here...\n\n## Usage\n\nIt currently works only over IO.\n\n```bash\njedi-language-server\n```\n\n## Local Development\n\nLocal development for this project is quite simple.\n\n**Dependencies**\n\nInstall the following tools manually.\n\n* [Poetry](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n*Recommended*\n\n* [pyenv](https://github.com/pyenv/pyenv)\n\n**Set up development environment**\n\n```bash\nmake setup\n```\n\n**Run Tests**\n\n```bash\nmake test\n```\n\n## Written by\n\nSamuel Roeca *samuel.roeca@gmail.com*\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'url': 'https://github.com/pappasam/jedi-language-server',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
