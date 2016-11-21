#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module to dump a classes file

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
import argparse
from class_dumper import ClassDumper
################################################################

class ClassDumperClasses(ClassDumper):
    " Class emplyed to output to classes text format "

    def __init__(self, output_file, **kwargs):
        ClassDumper.__init__(self, **kwargs)
        self.output_file = output_file
        self.nb_tabulation = 0


    def dump_classes(self, classes):

        " dumps classes "

        fout = open(self.output_file, 'w')
        for _class in classes:
            self.dump_class(_class, fout)

    def dump_class(self, _class, _file):

        " dumps a class into the provided file "

        sstr = self.format_class_declaration(_class)
        self._inc_tabulation()
        sstr += self.format_constructors(_class)
        sstr += self.format_methods(_class)
        sstr += self.format_members(_class)
        sstr += "\n"
        self._dec_tabulation()
        _file.write(sstr)

    @classmethod
    def format_class_declaration(cls, _class):

        " forge a str representing the class "

        sstr = "class " + _class.name

        if _class.inheritance is not None:
            sstr += "(" + ", ".join(_class.inheritance) + ")"

        sstr += "\n"
        return sstr



    def format_constructors(self, _class):

        " forge a str representing the constructor "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:
            meths = _class.getMethods(encaps)
            if _class.name in meths:
                for meth in meths[_class.name]:
                    sstr += self._format_method(_class, meth)

        for encaps in ['public', 'private', 'protected']:
            meths = _class.getMethods(encaps)
            if '~' + _class.name in meths:
                for meth in meths['~' + _class.name]:
                    sstr += self._format_method(_class, meth)

        return sstr


    def format_methods(self, _class):

        " forge a str representing methods "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            meths_names = set(meths.keys()) - set([_class.name, '~' + _class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:
                for _name in meths_names:
                    for meth in meths[_name]:
                        sstr += self._format_method(_class, meth)

        return sstr


    def format_members(self, _class):

        " forge a str representing members "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            membs = _class.getMembers(encaps)
            if len(membs) is not 0:
                for dummy_n, memb in membs.iteritems():
                    sstr += self._format_member(_class, memb)
                    sstr += "\n"
        return sstr



    def _format_method(self, dummy_class, meth):

        sstr = self._get_tabulation()
        sstr += meth.encapsulation + " "
        if meth.static:
            sstr += meth.static + " "
        if meth.virtual:
            sstr += meth.virtual + " "
        if meth.ret:
            sstr += meth.ret + " "

        sstr += meth.name + "("
        sstr += ", ".join([a + " " + b
                           for b, a in list(meth.args.iteritems())])
        sstr += ")"
        if meth.const:
            sstr += " const"
        sstr += ";\n"

        self._inc_tabulation()
        self._dec_tabulation()

        return sstr

    def _format_member(self, dummy_class, memb):

        sstr = self._get_tabulation()
        sstr += memb.encapsulation + " "
        if memb.static == 'static':
            sstr += memb.static
        sstr += memb.type + " " + memb.name + ';'
        return sstr

    def _get_tabulation(self):
        return "  " * self.nb_tabulation

    def _inc_tabulation(self):
        self.nb_tabulation += 1

    def _dec_tabulation(self):
        self.nb_tabulation -= 1

################################################################

def main():
    parser = argparse.ArgumentParser(
        description='Classes descriptor format producer for class representation')

    parser.add_argument('--class_file', '-c', help='The class file to process', required=True)
    parser.add_argument('--output_file', '-o',
                        help='The file where to put the classes description', required=True)

    args = parser.parse_args()
    args = vars(args)
    dumper_class = ClassDumperClasses(args['output_file'])
    dumper_class.dump(class_file=args['class_file'])


if __name__ == '__main__':
    main()
