# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dj']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'delegator.py>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['dj = dj:__main__.run']}

setup_kwargs = {
    'name': 'dj-command',
    'version': '0.3.0',
    'description': 'Run Django management commands with a simple `dj {command_name}`. Can also use aliases for commands defined in a simple config file.',
    'long_description': '# Why?\nIt is available everywhere if you install via `pip`, has cute aliases defined in a JSON file (`.dj-config.json`) per project, will run as many commands as you want, and defaults to Django management commands if an alias cannot be found.\n\nNote that calling a long-running processes (e.g. `runserver`) will prevent any other commands from being run.\n\n# Example .dj-config.json\n```\n{\n\t"commands": [\n\t\t{\n\t\t\t"name": "m",\n\t\t\t"help": "Does the migration dance",\n\t\t\t"execute": "./manage.py makemigrations && ./manage.py migrate",\n\t\t},\n\t\t{\n\t\t\t"name": "r",\n\t\t\t"help": "Runserver",\n\t\t\t"execute": "./manage.py runserver",\n\t\t\t"long_running": true\n\t\t}\n\t]\n}\n```\n\n# Basic arguments and options\n- `dj --help` to see all of the options\n- `dj --list` to see all of the available custom commands\n- `dj {command_name}` to run a custom command or Django management command (e.g. `dj migrate`)\n- `dj {command_name} --dry_run` to show what commands would run without actually executing them\n\n# How to work on the source\n1. Clone the repo\n1. Run the source locally: `poetry run python dj`\n1. Test the source: `poetry run pytest`\n1. Build and install locally: `poetry build && pip3 install --user --upgrade --force-reinstall dist/dj_command-0.1.0-py3-none-any.whl`\n1. Test with `~/.local/bin/dj migrate`\n1. Publish the source to pypi: `poetry publish --build --username USERNAME --password PASSWORD`\n\n# Acknowledgements\n- [poetry](https://poetry.eustace.io/): please, please, please continue to wrangle the complexity of 1) creating Python projects, and 2) installing dependencies; seriously, it\'s baffling out there without you\n- [click](https://click.palletsprojects.com/): ridiculously full-featured library to help implement CLI programs in Python; it has all the bells and most of the whistles\n- [attrs](https://www.attrs.org/): would you like easy classes in Python? yes, please\n- [delegator.py](https://github.com/amitt001/delegator.py): dealing with subprocess is a pain, but delegator hides all the ugly cruft behind a nice API\n\n# Prior art\nThis isn\'t a new idea and there are a few other implementations out there that do similar things. But, uh, I like mine. 😀\n- [dj-cmd](https://pypi.org/project/dj-cmd/)\n- [Django-dj](https://github.com/h4l/Django-dj)\n- [dj-cli](https://pypi.org/project/dj-cli/)\n',
    'author': 'Adam Hill',
    'author_email': 'adamghill@yahoo.com',
    'url': 'https://github.com/adamghill/dj',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
