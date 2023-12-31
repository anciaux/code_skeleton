#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Descriptor for classes

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

from __future__ import print_function
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


class Typename(object):

    " Describes a typename "

    def __init__(self, name, encapsulation):
        self.name = name
        self.encapsulation = encapsulation

################################################################


class Method(object):

    " Describes a method "

    def __init__(self, name, args, ret, encapsulation,
                 virtual, static, const, comments):

        self.name = name
        self.virtual = virtual
        self.static = static
        self.args = list()
        self.args += args
        self.ret = ret
        self.encapsulation = encapsulation
        if self.encapsulation == '':
            self.encapsulation = 'public'
        self.comments = comments
        self.const = const
        # print "creating method {0}".format(name)
        # print self.__dict__

    def __str__(self):
        sstr = self.encapsulation + " "
        if not self.virtual == '':
            sstr += self.virtual + " "

        sstr += self.ret + " " + self.name + "("
        pairs = list(self.args)
        pairs = [b + " " + a for a, b in pairs]
        sstr += ", ".join(pairs)
        sstr += ")"
        return sstr

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self))

################################################################


class Member(object):

    " Descriptor of a method "

    def __init__(self, name, _type, encapsulation, static, comments):
        self.name = name
        self.type = _type
        self.encapsulation = encapsulation
        self.static = static
        self.comments = comments

    def __str__(self):
        return self.encapsulation + " " + self.type + " " + self.name

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

################################################################


class ClassDescriptor(object):

    " Describe a class "

    def __init__(self, name, inheritance=None):
        self.name = name
        self.inheritance = inheritance
        self.members = {'private': {}, 'public': {}, 'protected': {}}
        self.methods = {'private': {}, 'public': {}, 'protected': {}}
        self.types = {'private': {}, 'public': {}, 'protected': {}}

    def add_method(self, name, args, ret, encapsulation,
                   virtual, static, const, comments):
        " append a method to the class "

        new_method = Method(name, args, ret, encapsulation,
                            virtual, static, const, comments)
        if name not in self.methods[encapsulation]:
            self.methods[encapsulation][name] = set()
        self.methods[encapsulation][name].add(new_method)

    def add_member(self, name, _type, encapsulation, static, comments):
        " append a member to the class "

        new_member = Member(name, _type, encapsulation, static, comments)
        self.members[encapsulation][name] = new_member

    def add_type(self, name, encapsulation):
        " add a type to the list of typenames "

        new_type = Typename(name, encapsulation)
        self.types[encapsulation][name] = new_type

    def get_members(self, encapsulation=None):
        " return the members "

        return self.members[encapsulation]

    def get_types(self, encapsulation=None):
        " return the typenames "
        return self.types[encapsulation]

    def get_methods(self, encapsulation=None):
        " return the methods "
        return self.methods[encapsulation]

    def __str__(self):
        sstr = "Class " + self.name + "\n"
        if self.inheritance:
            sstr += "Inherit: "
            sstr += ",".join(self.inheritance) + "\n"

        sstr += "Methods:\n"

        try:
            _iter = self.methods.iteritems()
        except Exception as ex:
            _iter = self.methods.items()

        for encaps, meths in _iter:
            sstr += encaps + ":\n"
            try:
                _iter = meths.iteritems()
            except Exception as ex:
                _iter = meths.items()
            for dummy_name, m_list in _iter:
                for method in m_list:
                    sstr += str(method) + "\n"
        sstr += "\n"
        sstr += "Members:\n"
        try:
            _iter1 = self.members.iteritems()
        except Exception as ex:
            _iter1 = self.members.items()
        for encaps, membs in _iter1:
            sstr += encaps + ":\n"
            try:
                _iter2 = membs.iteritems()
            except Exception as ex:
                _iter2 = membs.items()
            for dummy_name, memb in _iter2:
                sstr += str(memb) + "\n"
        return sstr

################################################################
