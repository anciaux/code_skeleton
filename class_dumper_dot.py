#!/usr/bin/python
# -*- coding: utf-8 -*-

" Module used to produces a GraphViz (.dot) file "
################################################################
import argparse
import subprocess
import os
from class_dumper import ClassDumper
################################################################


def _protect_str(string):
    return string.replace('<', r'\<').replace('>', r'\>')

################################################################


class ClassDumperDOT(ClassDumper):

    def __init__(self, output_file,
                 inheritance_flag=True,
                 colaboration_flag=True):

        ClassDumper.__init__(self)
        self.encaps_symbol = {'public': '+', 'private': '-', 'protected': '#'}
        self.inheritance_flag = inheritance_flag
        self.colaboration_flag = colaboration_flag
        self.output_file = output_file

    def dump_classes(self, classes):

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
        sstr += self.formatConstructors(_class)
        sstr += self.formatMethods(_class)
        sstr += self.formatMembers(_class)
        sstr += '}"];\n'
        if self.inheritance_flag:
            sstr += self._format_inheritance(_class)
        if self.colaboration_flag:
            sstr += self._format_compositions(_class)

        sstr += self.formatTypes(_class)
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
                sstr += '"{0}" '.format(mother) + " -> "
                + '"{0}" '.format(_class.name)
                sstr += ('[style="solid",color="midnightblue",'
                         'fontname="Helvetica"'
                         ',arrowtail="onormal",fontsize="10",dir="back"];\n')
            return sstr
        return ""

    def _format_constructors(self, _class):
        sstr = ""
        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            if _class.name in meths:
                if sstr == "":
                    sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths[_class.name]:
                    sstr += self.formatMethod(_class, cons)
                    sstr += "\\l"
            if '~' + _class.name in meths:
                if sstr == "":
                    sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths['~' + _class.name]:
                    sstr += self.formatMethod(_class, cons)
                    sstr += "\\l"

        return sstr

    def _format_methods(self, _class):

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            meths_names = set(meths.keys()) - set([_class.name, '~'
                                                   + _class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:

                for _name in meths_names:
                    for meth in meths[_name]:
                        if sstr == "":
                            sstr = "|"
                        sstr += self.encaps_symbol[encaps] + " "
                        sstr += self.formatMethod(_class, meth)
                        sstr += "\\l"

        return sstr

    def _format_members(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            membs = _class.getMembers(encaps)
            if len(membs) is not 0:

                for dummy_name, memb in membs.iteritems():
                    if sstr == "":
                        sstr = "|"
                    sstr += self.encaps_symbol[encaps] + " "
                    sstr += self.formatMember(_class, memb)
                    sstr += "\\l"

        return sstr

    def _format_compositions(self, _class):
        composition_set = set()
        for encaps in ['public', 'private', 'protected']:

            membs = _class.getMembers(encaps)
            if len(membs) is not 0:
                for _name, memb in membs.iteritems():
                    if memb.type in self.base_types:
                        continue
                    composition_set.add(self.baseType(memb.type))

        sstr = ""
        for t in composition_set:
            sstr += '"{0}" '.format(t) + " -> " + '"{0}" '.format(_class.name)
            sstr += ('[style="dashed",color="midnightblue",'
                     'fontname="Helvetica",arrowtail="odiamond",'
                     'fontsize="10",dir="back"];\n')

        return sstr

    def _format_types(self, _class):

        sstr = ""
        for encaps in ['public', 'private', 'protected']:
            if _class.types[encaps] is not None:

                for t in _class.types[encaps]:
                    if t in self.base_types:
                        continue
                    sstr += '"{0}" '.format(_class.name) + " -> "
                    + '"{0}" '.format(t)
                    sstr += ('[style="solid",color="black",'
                             'fontname="Helvetica",arrowtail="odiamond",'
                             'fontsize="10",dir="back"];\n')
        return sstr
        return ""

    def _format_method(self, _class, meth):
        arg_types = list(meth.args.iteritems())
        arg_types = [_protect_str(a) for b, a in arg_types]
        sstr = ""
        if meth.static:
            sstr += meth.static + " "
        if meth.ret:
            sstr += _protect_str(meth.ret) + " "
        sstr += meth.name + "(" + ",".join(arg_types) + ")"
        if meth.virtual == 'pure virtual':
            sstr += "=0"
        return sstr

    def _format_member(self, _class, memb):
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
    parser.add_argument('--colaboration_no', action='store_false',
                        help='Disable the collaboration output')
    parser.add_argument('--inheritance_no', action='store_false',
                        help='Disable the inheritance output')
    parser.add_argument('--classes', type=str,
                        help='The classes to output')

    args = parser.parse_args()
    args = vars(args)
    if args["output"] is None:
        args['output'] = os.path.splitext(args['class_file'])[0] +\
                         "." + args['format']

    if args["classes"] is not None:
        args["classes"] = args["classes"].split(',')

    inheritance_flag = True
    colaboration_flag = True
    if not args['inheritance_no']:
        inheritance_flag = False
    if not args['colaboration_no']:
        colaboration_flag = False

    class_file = args['class_file']
    del args['class_file']
    dot_file = os.path.splitext(class_file)[0] + ".dot"
    dumper_class = ClassDumperDOT(inheritance_flag, colaboration_flag, dot_file)
    dumper_class.dump(class_file, **args)
    exe = ['dot']
    option_format = ['-T'+args['format']]
    option_output = ['-o', args['output']]
    option_input = [dot_file]
    subprocess.call(exe+option_format+option_output+option_input)


if __name__ == '__main__':
    main()
