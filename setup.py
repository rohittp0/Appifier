'''
    This is a utility to search for .desktop files and create desktop entries.
    Copyright (C) 2021  Rohit T P

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see https://www.gnu.org/licenses/
'''
from setuptools import setup
from appify.__init__ import VERSION

PACKAGE_NAME = "appify"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requires = f.read().splitlines()


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Rohit T P",
    author_email="tprohit9@gmail.com",
    description="A utility to search for .desktop files and create desktop entries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohittp0/Appify",
    packages=[PACKAGE_NAME],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Topic :: Utilities"
    ],
    entry_points={
        "console_scripts": [f"{PACKAGE_NAME}={PACKAGE_NAME}.__main__:main"]
    },
    include_package_data=True,
    install_requires=requires,
    python_requires='>=3.6',
)
