# -*- coding: utf-8 -*-
u"""
Copyright 2019 Alvaro Lopez-Gil Navajas
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from distutils.core import setup


def read_file(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='emails_finder',
    packages=['emails_finder'],
    version=read_file('VERSION').strip(),
    license='MIT',
    description='',
    author='alopezna5',
    url='https://github.com/alopezna5/google_emails_finder',
    download_url='https://github.com/alopezna5/mASAPP_CI/archive/0.2.tar.gz0',
    keywords=['CRM', 'CLIENT', 'EMAIL', 'DATABASE'],
    install_requires=read_file('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            'emails_finder = emails_finder.__main__:main',
        ]
    }
)
