# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydantic_settings', 'pydantic_settings.loaders']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'pydantic>=0.31.1,<0.32.0',
 'pyyaml>=5.1.2,<6.0.0',
 'tomlkit>=0.5.5,<0.6.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pydantic-settings',
    'version': '0.1.0a2',
    'description': 'Hipster-orgazmic tool to mange application settings',
    'long_description': '# Pydantic settings\n> Hipster-orgazmic tool to mange application settings\n\n[![Build Status](https://travis-ci.com/danields761/pydantic-settings.svg?branch=master)](https://travis-ci.com/danields761/pydantic-settings)\n[![PyPI version](https://badge.fury.io/py/pydantic-settings.svg)](https://badge.fury.io/py/pydantic-settings)\n\nLibrary which extends [**pydantic**](https://github.com/samuelcolvin/pydantic) functionality in scope of application settings. *Pydantic* already have settings\nimplementation, e.g. `pydantic.BaseSettings`, but from my point it\'s missing some useful features:\n\n1. Overriding settings values by environment variables even for nested fields\n2. Providing detailed information about value location inside a loaded file or environment variable, which helps to point user his mistake\n3. Documenting model fields isn\'t feels comfortable, but it\'s really essential to write comprehensive documentation for application settings\n\n> **_NOTE:_** Despite the fact that project already implements most of his features, it\'s still considered to be on alpha stage\n\n## Installation\n\nUsing pip:\n\n```sh\npip install pydantic-settings\n```\n\n## Usage example\n\n### Override values by env variables\n\nAllows to override values for nested fields if they are represented as *pydantic* model. Generally speaking, nested `attrs` and `dataclass` models also supported, but they are not supported by *pydantic*. \n\nHere is example:\n\n```python\nfrom pydantic import BaseModel, ValidationError\nfrom pydantic_settings import BaseSettingsModel\n\nclass Nested(BaseModel):\n    foo: int\n\nclass Settings(BaseSettingsModel):\n    nested: Nested\n\n\ntry:\n    Settings.from_env({\'APP_nested_FOO\': \'NOT AN INT\'})\nexcept ValidationError as e:\n    assert e.raw_errors[0].env_loc == \'APP_nested_FOO\'  # shows exact env variable name\n```\n\n### Point exact error file location\n\n```python\nfrom pydantic import BaseModel, IntegerError\nfrom pydantic_settings import BaseSettingsModel, LoadingValidationError, load_settings, FileLocation\n\nclass Nested(BaseModel):\n    foo: int\n\nclass Settings(BaseSettingsModel):\n    nested: Nested\n\nconf_text = """\nnested:\n    foo: \'NOT AN INT\'\n"""\n\ntry:\n    load_settings(Settings, conf_text, type_hint=\'yaml\')\nexcept LoadingValidationError as e:\n    assert e.raw_errors[0].loc == (\'nested\', \'foo\')\n    assert e.raw_errors[0].text_loc == FileLocation(line=3, col=10, end_line=3, end_col=22)\n    assert isinstance(e.raw_errors[0].exc, IntegerError)\n\n```\n\n\n### Extracts fields documentation\n\nAllows to extract *Sphinx* style attributes documentation by processing AST tree of class definition\n\n```python\nfrom pydantic_settings import BaseSettingsModel\n\nclass Foo(BaseSettingsModel):\n    class Config:\n        build_attr_docs = True\n\n    bar: str\n    """here is docs"""\n\n    #: this style is\'t supported, but probably will be added in future\n    baz: int\n\nassert Foo.__fields__[\'bar\'].schema.description == \'here is docs\'\nassert Foo.__fields__[\'baz\'].schema.description is None  # :(\n```\n\n## Development setup\n\nProject requires [**poetry**](https://github.com/sdispater/poetry) for development setup.\n\n* If you aren\'t have it already\n\n```sh\npip install poetry\n``` \n\n* Install project dependencies\n\n```sh\npoetry install\n```\n\n* Run tests\n\n```sh\npoetry run pytest .\n```\n\n* Great, all works! Expect one optional step:\n\n* Install [**pre-commit**](https://github.com/pre-commit/pre-commit) for pre-commit hooks\n\n```sh\npip install pre-commit\npre-commit install\n```\n\nThat will install pre-commit hooks, which will check code with *flake8* and *black*.\n\n> *NOTE* project uses **black** as code formatter, but i\'am personally really dislike their\n> *"double quoted strings everywhere"* style, that\'s why `black -S` should be used (anyway it\'s configured in *pyproject.toml* file)  ',
    'author': 'Daniel Daniels',
    'author_email': 'danields761@gmail.com',
    'url': 'https://github.com/danields761/pydantic-settings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
