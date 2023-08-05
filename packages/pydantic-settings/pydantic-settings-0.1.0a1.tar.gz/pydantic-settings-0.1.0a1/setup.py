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
    'version': '0.1.0a1',
    'description': 'Hipster-orgazmic tool to mange application settings',
    'long_description': '# Pydantic Settings\n\nLibrary which extends **pydantic** functionality in scope of application settings.\n\nPydantic already have settings implementation, e.g. `pydantic.BaseSettings`, but from my point it\'s missing some useful features, listed below.\n\n## Features\n\n1. Point exact location of a failed field in the text\n2. Override file values by environment variables, even if a field is nested\n\nAllow to override values for nested fields if they are represented as *pydantic* model, `dataclass` or `attrs` dataclass. Here is example:\n\n```python\n@dataclass\nclass Nested:\n    foo: int\n\nclass Settings(SettingsModel):\n    nested: Nested\n\n\ntry:\n    Settings.from_env({\'APP_NESTED_FOO\': \'NOT AN INT\'})\nexcept ValidationError as e:\n    assert e.raw_errors[0].env_loc = \'APP_NESTED_FOO\'\n```\n\n3. Shows right environment variable name for failed field\n\n```python\ntry:\n    Settings.from_env({\'APP_nested_FOO\': \'NOT AN INT\'})\nexcept ValidationError as e:\n    assert e.raw_errors[0].env_loc = \'APP_nested_FOO\'\n```\n\n4. Extracts field documentation from *Sphinx* style attributes documentation by processing AST tree of class definition\n\n```python\nclass Foo(SettingsModel):\n    class Config:\n        extract_docs = True\n\n    bar: str\n    """here is docs"""\n\n    #: this style is\'t supported, but probably will be added in future\n    baz: int\n\nassert Foo.__field__[\'bar\'].schema.description == \'here is docs\'\nassert Foo.__field__[\'baz\'].schema.description == \'\'  # :(\n```\n\n5. Render documentation examples with commentaries taken from fields description\n\n```python\nclass Settings(SettingsModel):\n    host: str = \'localhost\'\n    """\n    Self domain name\n    """\n\n    auth_secret: SecretStr\n    """\n    Secret key used to encrypt user tokens with HMAC-SHA256\n    """\n\n\nEXAMPLE_SETTINGS = Settings(\n    host=\'host.name\',\n    auth_secret=\'5O5qOWiM5qnvUwvQtP1_bUTonSIn7I7C66eqVGL2it0=\',\n)\n\nassert dumper(EXAMPLE_SETTINGS, \'yaml\') == """\n# Self domain name\nhost: host.name\n\n# Secret key used to encrypt user tokens with HMAC-SHA256\nauth_secret: 5O5qOWiM5qnvUwvQtP1_bUTonSIn7I7C66eqVGL2it0\n"""\n```\n\n## Development status\n\n1. partially, only *json* and *yaml* supported for now\n2. doesn\'t supports overriding inside list, case-sensitive implementation\n3. done\n4. done (*attr* classes not supported for now)\n5. not started',
    'author': 'Daniel Daniels',
    'author_email': 'danields761@gmail.com',
    'url': 'https://github.com/danields761/pydantic-settings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
