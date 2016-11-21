#!/usr/bin/env python
# -*- coding: utf-8 -*-

" Mother class for all class dumpers "
################################################################
from abc import ABCMeta, abstractmethod
from class_reader import ClassReader
################################################################

class ClassDumper(object):

    " Mother class for all class dumpers "

    __metaclass__ = ABCMeta

    def __init__(self):
        self.base_types = ['int', 'double', 'float', 'unsigned int']
        self.base_types = self.base_types + \
        [e + ' *' for e in self.base_types] + \
        [e + ' &' for e in self.base_types]

    def dump(self, class_file, classes=None, **dummy_kwargs):

        " perform the dump "

        cls_reader = ClassReader()
        _classes = cls_reader.read(class_file)
        sstr = ""
        for _class in _classes:
            if classes is None:
                condition = True
            else:
                condition = (_class.name in classes)
            if condition:
                sstr += self.dump_file(_class)
            else:
                print "ignore class '{0}'".format(_class.name)

        return sstr

    @abstractmethod
    def dump_file(self, _class):

        " formats the provided class as a string: abstract method "

        raise Exception('pure virtual function')

    @classmethod
    def base_type(cls, _type):

        " todo:: "
        temp_type = _type.replace('&', '')
        temp_type = temp_type.replace('*', '')
        temp_type = temp_type.strip()
        return temp_type
