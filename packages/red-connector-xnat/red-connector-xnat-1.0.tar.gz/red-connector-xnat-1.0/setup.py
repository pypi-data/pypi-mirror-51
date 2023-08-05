# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['red_connector_xnat']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.0,<4.0', 'requests>=2.18,<3.0']

entry_points = \
{'console_scripts': ['red-connector-xnat-http = red_connector_xnat.main:main']}

setup_kwargs = {
    'name': 'red-connector-xnat',
    'version': '1.0',
    'description': 'RED Connector XNAT is part of the Curious Containers project.',
    'long_description': '# RED Connector XNAT\n\nRED Connector XNAT is part of the Curious Containers project.\n\nFor more information please refer to the Curious Containers [documentation](https://www.curious-containers.cc/).\n\n## Acknowledgements\n\nThe Curious Containers software is developed at [CBMI](https://cbmi.htw-berlin.de/) (HTW Berlin - University of Applied Sciences). The work is supported by the German Federal Ministry of Economic Affairs and Energy (ZIM project BeCRF, grant number KF3470401BZ4), the German Federal Ministry of Education and Research (project deep.TEACHING, grant number 01IS17056 and project deep.HEALTH, grant number 13FH770IX6) and HTW Berlin Booster.\n\n',
    'author': 'Christoph Jansen',
    'author_email': 'Christoph.Jansen@htw-berlin.de',
    'url': 'https://www.curious-containers.cc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
