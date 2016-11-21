#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Mother class for all class dumpers

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

################################################################
from __future__ import print_function
import re
from abc import ABCMeta, abstractmethod
from code_skeleton.class_reader import ClassReader
################################################################
__author__ = "Guillaume Anciaux"
__copyright__ = "Copyright EPFL"
__credits__ = ["Guillaume Anciaux"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Guillaume Anciaux"
__email__ = "guillaume.anciaux@epfl.ch"
__status__ = "Beta"
################################################################


class ClassDumper(object):

    " Mother class for all class dumpers "

    __metaclass__ = ABCMeta

    def __init__(self, selected_classes=None):
        self.base_types = ['int', 'double', 'float', 'unsigned int']
        self.base_types = self.base_types + \
        [e + ' *' for e in self.base_types] + \
        [e + ' &' for e in self.base_types]

        self.selected_classes = selected_classes
        if self.selected_classes is None:
            self.selected_classes = []

    def dump(self, class_file=None, **kwargs):

        " perform the dump "

        _all_classes = []

        if class_file is not None:
            cls_reader = ClassReader()
            _all_classes = cls_reader.read(class_file)

        classes = []

        for _class in _all_classes:
            if not self.selected_classes:
                condition = True
            else:
                print (self.selected_classes)
                condition = (_class.name in self.selected_classes)
            if condition:
                classes.append(_class)
            else:
                print("ignore class '{0}'".format(_class.name))

        self.dump_classes(classes, **kwargs)

    @abstractmethod
    def dump_classes(self, classes, **kwargs):

        " formats the provided class as a string: abstract method "

        raise Exception('pure virtual function')

    @classmethod
    def base_type(cls, _type):

        " todo:: "
        temp_type = _type.replace('&', '')
        temp_type = temp_type.replace('*', '')
        temp_type = temp_type.strip()
        return temp_type

    @classmethod
    def _make_base_filename(cls, class_name):
        name = re.sub(r'([0-9]|[A-Z0-9])', r'_\g<1>', class_name)
        name = name.lower()

        if name[0] == '_':
            name = name[1:]
        return name

