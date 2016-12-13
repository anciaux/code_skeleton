#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module used to produces a GraphViz (.dot) file

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
import subprocess
import os
from code_skeleton.class_dumper import ClassDumper
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


def _protect_str(string):
    return string.replace('<', r'\<').replace('>', r'\>')

################################################################


class ClassDumperDOT(ClassDumper):

    " Dumper to DOT (GraphViz format) "

    def __init__(self, output_file,
                 inheritance_flag=True,
                 collaboration_flag=True):

        if not isinstance(output_file, str):
            raise Exception('invalid filename: {0}'.format(output_file))

        ClassDumper.__init__(self)
        self.encaps_symbol = {'public': '+', 'private': '-', 'protected': '#'}
        self.inheritance_flag = inheritance_flag
        self.collaboration_flag = collaboration_flag
        self.output_file = output_file

    def dump_classes(self, classes, **kwargs):

        fout = open(self.output_file, 'w')

        sstr = 'digraph "test"\n{'
        sstr += """
edge [fontname="Helvetica",fontsize="10",
      labelfontname="Helvetica", labelfontsize="10"];
node [fontname="Helvetica",fontsize="10",shape=record];
"""

        fout.write(sstr)

        for _class in classes:
            self.dump_class(_class, fout)

        fout.write("}")
        fout.close()

    def dump_class(self, _class, _file):

        " dumps a class into the provided file "

        sstr = self._format_class_declaration(_class)
        sstr += self._format_constructors(_class)
        sstr += self._format_methods(_class)
        sstr += self._format_members(_class)
        sstr += '}"];\n'
        if self.inheritance_flag:
            sstr += self._format_inheritance(_class)
        if self.collaboration_flag:
            sstr += self._format_compositions(_class)

        sstr += self._format_types(_class)
        _file.write(sstr)
        return sstr

    @classmethod
    def _format_class_declaration(cls, _class):

        sstr = '"{0}" '.format(_class.name)
        sstr += '[label="{' + format(_class.name) + "\\n"
        return sstr

    @classmethod
    def _format_inheritance(cls, _class):
        if _class.inheritance is not None:
            sstr = ""
            for mother in _class.inheritance:
                sstr += ('"{0}" '.format(mother) + " -> "
                         '"{0}" '.format(_class.name))
                sstr += ('[style="solid",color="midnightblue",'
                         'fontname="Helvetica"'
                         ',arrowtail="onormal",fontsize="10",dir="back"];\n')
            return sstr
        return ""

    def _format_constructors(self, _class):
        sstr = ""
        for encaps in ['public', 'private', 'protected']:

            meths = _class.get_methods(encaps)
            if _class.name in meths:
                if sstr == "":
                    sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths[_class.name]:
                    sstr += self._format_method(cons)
                    sstr += "\\l"
            if '~' + _class.name in meths:
                if sstr == "":
                    sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths['~' + _class.name]:
                    sstr += self._format_method(cons)
                    sstr += "\\l"

        return sstr

    def _format_methods(self, _class):

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.get_methods(encaps)
            meths_names = set(meths.keys()) - set([_class.name, '~'
                                                   + _class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:

                for _name in meths_names:
                    for meth in meths[_name]:
                        if sstr == "":
                            sstr = "|"
                        sstr += self.encaps_symbol[encaps] + " "
                        sstr += self._format_method(meth)
                        sstr += "\\l"

        return sstr

    def _format_members(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            membs = _class.get_members(encaps)
            if len(membs) is not 0:

                try:
                    _iter = membs.iteritems()
                except Exception as ex:
                    _iter = membs.items()

                for dummy_name, memb in _iter:
                    if sstr == "":
                        sstr = "|"
                    sstr += self.encaps_symbol[encaps] + " "
                    sstr += self._format_member(memb)
                    sstr += "\\l"

        return sstr

    def _format_compositions(self, _class):
        composition_set = set()
        for encaps in ['public', 'private', 'protected']:

            membs = _class.get_members(encaps)
            if len(membs) is not 0:

                try:
                    _iter = membs.iteritems()
                except Exception as ex:
                    _iter = membs.items()

                for dummy_name, memb in _iter:
                    if memb.type in self.base_types:
                        continue
                    composition_set.add(self.base_type(memb.type))

        sstr = ""
        for comp in composition_set:
            sstr += '"{0}" '.format(comp) + " -> " + '"{0}" '.format(_class.name)
            sstr += ('[style="dashed",color="midnightblue",'
                     'fontname="Helvetica",arrowtail="odiamond",'
                     'fontsize="10",dir="back"];\n')

        return sstr

    def _format_types(self, _class):

        sstr = ""
        for encaps in ['public', 'private', 'protected']:
            if _class.types[encaps] is not None:

                for _type in _class.types[encaps]:
                    if _type in self.base_types:
                        continue
                    sstr += '"{0}" '.format(_class.name) + " -> " \
                            + '"{0}" '.format(_type)
                    sstr += ('[style="solid",color="black",'
                             'fontname="Helvetica",arrowtail="odiamond",'
                             'fontsize="10",dir="back"];\n')
        return sstr

    @classmethod
    def _format_method(cls, meth):

        try:
            _iter = meth.args.iteritems()
        except Exception as ex:
            _iter = meth.args.items()

        arg_types = list(_iter)
        arg_types = [_protect_str(a) for dummy_b, a in arg_types]
        sstr = ""
        if meth.virtual == 'virtual' or\
           meth.virtual == 'pure virtual':
            sstr += 'virtual '

        if meth.static:
            sstr += meth.static + " "
        if meth.ret:
            sstr += _protect_str(meth.ret) + " "
        sstr += meth.name + "(" + ",".join(arg_types) + ")"
        if meth.virtual == 'pure virtual':
            sstr += "=0"
        return sstr

    @classmethod
    def _format_member(cls, memb):
        sstr = ""
        if memb.static == 'static':
            sstr += 'static '
        return sstr + _protect_str(memb.type) + " " + memb.name

################################################################


def main():

    parser = argparse.ArgumentParser(
        description='DOT graph producer for class representation')
    parser.add_argument('--class_file', '-c',
                        help='The class file to process', required=True)
    parser.add_argument('--format', '-f', default="pdf",
                        help='The format of the produced graph file')
    parser.add_argument('--output', '-o',
                        help='The file to be produced')
    parser.add_argument('--collaboration_no', action='store_false',
                        help='Disable the collaboration output')
    parser.add_argument('--inheritance_no', action='store_false',
                        help='Disable the inheritance output')
    parser.add_argument('--class_filter', type=str,
                        help='The classes to output')

    args = parser.parse_args()
    args = vars(args)
    if args["output"] is None:
        args['output'] = os.path.splitext(args['class_file'])[0] +\
                         "." + args['format']

    if args["class_filter"] is not None:
        args["class_filter"] = args["class_filter"].split(',')

    inheritance_flag = True
    collaboration_flag = True
    if not args['inheritance_no']:
        inheritance_flag = False
    if not args['collaboration_no']:
        collaboration_flag = False

    class_file = args['class_file']
    del args['class_file']
    dot_file = os.path.splitext(class_file)[0] + ".dot"
    dumper_class = ClassDumperDOT(dot_file, inheritance_flag,
                                  collaboration_flag)
    dumper_class.dump(class_file, **args)
    exe = ['dot']
    option_format = ['-T'+args['format']]
    option_output = ['-o', args['output']]
    option_input = [dot_file]
    subprocess.call(exe+option_format+option_output+option_input)


if __name__ == '__main__':
    main()
