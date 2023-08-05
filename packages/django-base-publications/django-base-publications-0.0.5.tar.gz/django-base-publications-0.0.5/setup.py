# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_base_publications',
 'django_base_publications.migrations',
 'django_base_publications.models']

package_data = \
{'': ['*'], 'django_base_publications': ['locale/ru/LC_MESSAGES/*']}

install_requires = \
['django-autoslug>=1.9,<2.0',
 'django>=1.11,<3.0',
 'funcy>=1.13,<2.0',
 'ipython>=7.7,<8.0']

setup_kwargs = {
    'name': 'django-base-publications',
    'version': '0.0.5',
    'description': '',
    'long_description': None,
    'author': 'Дмитрий',
    'author_email': 'acrius@mail.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
