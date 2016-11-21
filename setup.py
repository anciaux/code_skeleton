#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
@file   setup.py

@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  This is the setup script for the code_skeleton
        python package. It allows to run the package's unit tests,
        build its sphinx documentation and install it.

@section LICENCE

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from setuptools import setup, find_packages


setup(name="code_skeleton",
      packages=find_packages(),
      version="0.0.0",
      author="Guillaume Anciaux",
      author_email="guillaume.anciaux@epfl.ch",
      description=("Code classes solution and Code generator"),
      license="""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
""",
      test_suite="tests")
