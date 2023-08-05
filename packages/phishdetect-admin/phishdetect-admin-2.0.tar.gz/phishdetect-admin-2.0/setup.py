#!/usr/bin/env python3
# PhishDetect
# Copyright (c) 2018-2019 Claudio Guarnieri.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from setuptools import setup

description = "Web application to administer a PhishDetect Node"
requires = (
    'Flask',
    'requests',
    'PyYAML',
)

setup(
    name='phishdetect-admin',
    version='2.0',
    author='Claudio Guarnieri',
    author_email='nex@nex.sx',
    description=description,
    long_description=description,

    scripts=['bin/phishdetect-admin',],
    install_requires=requires,
    packages=['phishdetectadmin',],
    package_data={'phishdetectadmin': 'phishdetectadmin/templates/*.html'},
    include_package_data=True,
    keywords='security phishing phishdetect',
    license='GPLv3',
    classifiers=[
    ],
)
