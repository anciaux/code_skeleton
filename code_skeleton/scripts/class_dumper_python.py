#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module to dump a python project skeleton

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
import os
import argparse
from code_skeleton.class_dumper import ClassDumper
from code_skeleton.class_decriptor import Method
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


class ClassDumperPython(ClassDumper):

    " Produces a Python project ready to use "

    def __init__(self, output_dir):
        ClassDumper.__init__(self)
        self.output_dir = output_dir
        self.nb_tabulation = 0

    def dump_classes(self, classes):

        for _class in classes:
            basename = self._make_base_filename(_class.name)
            class_filename = os.path.join(self.output_dir, basename+".py")
            with open(class_filename, 'w') as _file:
                self.dump_class(_class, _file)

    def dump_class(self, _class, _file):

        " Dumps the class into the provided file "

        _file.write("""#!/usr/bin/env python
# -*- coding: utf-8 -*-

" todo:: documentation for module containing class {0}"

##########################################################################
from __future__ import print_function
##########################################################################

"""
                    .format(_class.name))
        imports_list = []
        if _class.inheritance is not None:
            imports_list = ["from " + self._make_base_filename(i)
                            + " import " + i  for i in _class.inheritance]
        imports = "\n".join(imports_list)
        if imports:
            _file.write("#"*74 + "\n")
            _file.write(imports)
            _file.write("\n" + "#"*74 + "\n\n")
        self._dump_class(_class, _file)
        _file.write("""

if __name__ == '__main__':
    test = {0}()
"""
                    .format(_class.name))

        return ""


    def _dump_class(self, _class, _file):

        sstr = self._format_class_declaration(_class)
        self._inc_tabulation()
        sstr += """
{0}\"\"\"
class {1}: Documentation TODO
{0}\"\"\"
""".format(self._get_tabulation(), _class.name)

        sstr += self._format_static_members(_class)
        sstr += self._format_constructors(_class)
        sstr += self._format_methods(_class)
        sstr += "\n"
        self._dec_tabulation()

        _file.write("\n")
        _file.write(sstr)
        _file.write("#"*74 + '\n')

    @classmethod
    def _format_class_declaration(cls, _class):
        sstr = "class " + _class.name

        if _class.inheritance is not None:
            sstr += "(" + ", ".join(_class.inheritance) + ")"
        else:
            sstr += "(object)"

        sstr += ":\n"
        return sstr

    def _format_constructors(self, _class):
        sstr = ""

        meths = {}
        for encaps in ['public', 'private', 'protected']:
            meths.update(_class.get_methods(encaps))

        if _class.name in meths:
            for meth in meths[_class.name]:
                meth.name = "__init__"
                sstr += self._format_method(meth, pass_flag=False)
                self._inc_tabulation()
                sstr += self._format_members(_class)
                sstr += self._get_tabulation() + "pass\n"
                self._dec_tabulation()
        else:
            meth = Method('__init__', "", "", 'public', '', '', '',
                          'default constructor')
            sstr += self._format_method(meth, pass_flag=False)
            self._inc_tabulation()
            sstr += self._format_members(_class)
            sstr += self._get_tabulation() + "pass\n"
            self._dec_tabulation()

        if '~' + _class.name in meths:
            for meth in meths['~' + _class.name]:
                meth.name = "__del__"
                sstr += self._format_method(meth)

        if sstr != "":
            sstr = """
{0}# ------------------------------------------------------------------ #
{0}# Constructors/Destructors                                           #
{0}# ------------------------------------------------------------------ #

""".format(self._get_tabulation()) + sstr

        return sstr

    def _format_methods(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.get_methods(encaps)
            meths_names = set(meths.keys()) - set([_class.name,
                                                   '~'+_class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:
                sstr += self._get_tabulation() + "# " + encaps + ":\n\n"
                for _name in meths_names:
                    for meth in meths[_name]:
                        sstr += self._format_method(meth)
                        sstr += "\n"

        if not sstr == "":
            sstr = """
{0}# ------------------------------------------------------------------ #
{0}# Methods                                                            #
{0}# ------------------------------------------------------------------ #

""".format(self._get_tabulation()) + sstr

        return sstr

    def _format_members(self, _class):
        sstr = ""

        # print _class.name,_class.members
        for encaps in ['public', 'private', 'protected']:

            membs = _class.get_members(encaps)
            if len(membs) is not 0:
                try:
                    _iter = membs.iteritems()
                except Exception as ex:
                    _iter = membs.items()

                for dummy_name, memb in _iter:
                    if memb.static == 'static':
                        continue
                    sstr += self._format_member(memb)
                    sstr += "\n"

        if sstr != "":
            sstr = """
{0}# Members ---------------------- #

""".format(self._get_tabulation()) + sstr

        return sstr

    def _format_static_members(self, _class):
        sstr = ""

        # print _class.name,_class.members
        for encaps in ['public', 'private', 'protected']:

            membs = _class.get_members(encaps)
            if len(membs) is not 0:
                try:
                    _iter = membs.iteritems()
                except Exception as ex:
                    _iter = membs.items()

                for dummy_name, memb in _iter:
                    if not memb.static == 'static':
                        continue
                    sstr += self._format_static_member(memb)
                    sstr += "\n"

        if sstr != "":
            sstr = """
{0}# Members ---------------------- ##

""".format(self._get_tabulation()) + sstr

        return sstr

    def _format_method(self, meth, pass_flag=True):

        sstr = ""

        name = meth.name
        first_param = "self"
        if meth.encapsulation == 'private':
            name = "__" + name
        if meth.encapsulation == 'protected':
            name = "_" + name
        if meth.static:
            sstr += self._get_tabulation() + "@classmethod\n"
            first_param = "cls"

        sstr += self._get_tabulation() + "def " + name + "("


        _iter = meth.args

        sstr += ", ".join([first_param] +
                          [b for dummy_a, b in list(_iter)])
        sstr += "):\n"

        self._inc_tabulation()

        if meth.virtual == 'pure virtual':
            sstr += (self._get_tabulation() +
                     "raise Exception('This is a pure virtual method')\n")

        sstr += ("{0}\"\"\"{1}: Documentation TODO \"\"\"\n"
                 .format(self._get_tabulation(), name))

        if pass_flag:
            sstr += self._get_tabulation() + "pass\n"

        self._dec_tabulation()

        return sstr

    def _format_member(self, memb):
        name = memb.name
        if memb.encapsulation == 'private':
            name = "__" + name
        if memb.encapsulation == 'protected':
            name = "_" + name

        sstr = self._get_tabulation() + "# " + memb.type + " " + name + "\n"
        sstr += self._get_tabulation() + "self." + name + " = None\n"
        return sstr

    def _format_static_member(self, memb):
        name = memb.name
        if memb.encapsulation == 'private':
            name = "__" + name
        if memb.encapsulation == 'protected':
            name = "_" + name

        sstr = self._get_tabulation() + "#" + memb.type + " " + name + "\n"
        sstr += self._get_tabulation() + name + " = None\n"
        return sstr

    def _get_tabulation(self):
        return "    " * self.nb_tabulation

    def _inc_tabulation(self):
        self.nb_tabulation += 1

    def _dec_tabulation(self):
        self.nb_tabulation -= 1


################################################################

def main():

    parser = argparse.ArgumentParser(
        description='CPP project producer for class representation')
    parser.add_argument('--class_file', '-c',
                        help='The class file to process', required=True)
    parser.add_argument('--output_dir', '-o',
                        help='The directory where to put produced files',
                        required=True)

    args = parser.parse_args()
    args = vars(args)
    os.makedirs(args['output_dir'])
    dumper_class = ClassDumperPython(args['output_dir'])

    dumper_class.dump(args['class_file'])


if __name__ == '__main__':
    main()
