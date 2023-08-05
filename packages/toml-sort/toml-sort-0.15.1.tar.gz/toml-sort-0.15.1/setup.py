# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['toml_sort']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'tomlkit>=0.5.5']

entry_points = \
{'console_scripts': ['toml-sort = toml_sort.cli:cli']}

setup_kwargs = {
    'name': 'toml-sort',
    'version': '0.15.1',
    'description': 'Toml sorting library',
    'long_description': '# toml-sort\n\n[![image-version](https://img.shields.io/pypi/v/toml-sort.svg)](https://python.org/pypi/toml-sort)\n[![image-license](https://img.shields.io/pypi/l/toml-sort.svg)](https://python.org/pypi/toml-sort)\n[![image](https://img.shields.io/pypi/pyversions/toml-sort.svg)](https://python.org/pypi/toml-sort)\n\nA command line utility to sort and format your toml files. Requires Python 3.6 or greater.\n\n## Installation\n\n```bash\n# With pip\npip install toml-sort\n\n# With poetry\npoetry add toml-sort\n```\n\n## Motivation\n\n This library strives to sort TOML files by providing the following features:\n\n* Sort tables and Arrays of Tables (AoT)\n* Option to sort non-tables / non-AoT\'s, or not\n* Preserve inline comments\n* Option to preserve top-level document comments, or not\n* Standardize whitespace and indentation\n\nI wrote this library because I couldn\'t find any "good" sorting utilities for TOML files.\n\n## Usage\n\nThis project can be used as either a command line utility or a Python library.\n\n### Command line interface\n\nPrint detailed help\n\n    toml-sort --help\n\nRead from stdin, write to stdout:\n\n    cat input.toml | toml-sort\n\nRead from file on disk, write to file on disk:\n\n    toml-sort -o output.toml input.toml\n\nRead from file on disk, write to stdout\n\n    toml-sort input.toml\n\nRead from stdin, write to file on disk\n\n    cat input.toml | toml-sort -o output.toml\n\n## Example\n\nThe following example shows the input, and output, from the CLI with default options.\n\n### Unformatted, unsorted input\n\n```toml\n# My great TOML example\n\n  title = "The example"\n\n[[a-section.hello]]\nports = [ 8001, 8001, 8002 ]\ndob = 1979-05-27T07:32:00Z # First class dates? Why not?\n\n\n\n  [b-section]\n  date = "2018"\n  name = "Richard Stallman"\n\n[[a-section.hello]]\nports = [ 80 ]\ndob = 1920-05-27T07:32:00Z # Another date!\n\n                          [a-section]\n                          date = "2019"\n                          name = "Samuel Roeca"\n```\n\n### Formatted, sorted output\n\n```toml\n# My great TOML example\n\ntitle = "The example"\n\n[a-section]\ndate = "2019"\nname = "Samuel Roeca"\n\n[[a-section.hello]]\nports = [ 8001, 8001, 8002 ]\ndob = 1979-05-27T07:32:00Z # First class dates? Why not?\n\n[[a-section.hello]]\nports = [ 80 ]\ndob = 1920-05-27T07:32:00Z # Another date!\n\n[b-section]\ndate = "2018"\nname = "Richard Stallman"\n```\n\n## Local Development\n\nLocal development for this project is quite simple.\n\n**Dependencies**\n\nInstall the following tools manually.\n\n* [Poetry](https://github.com/sdispater/poetry#installation)\n* [GNU Make](https://www.gnu.org/software/make/)\n\n*Recommended*\n\n* [pyenv](https://github.com/pyenv/pyenv)\n\n**Set up development environment**\n\n```bash\nmake setup\n```\n\n**Run Tests**\n\n```bash\nmake test\n```\n\n## Written by\n\nSamuel Roeca *samuel.roeca@gmail.com*\n',
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'url': 'https://github.com/pappasam/toml-sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
