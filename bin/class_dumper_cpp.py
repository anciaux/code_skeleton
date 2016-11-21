#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module used to produces a C++ project skeleton

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
import os
import argparse
from class_dumper import ClassDumper
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

class ClassDumperCPP(ClassDumper):

    " Produces a C++ project ready to use with CMake/Makfiles "

    def __init__(self, output_dir, **kwargs):
        ClassDumper.__init__(self, **kwargs)
        self.output_dir = output_dir
        self.stage = None

    def dump_classes(self, classes):

        for _class in classes:
            self._dump_header(_class)
            self._dump_cc_file(_class)

        self._dump_main()
        self._dump_makefile(classes)
        self._dump_cmake(classes)

        return ""

    def _dump_makefile(self, classes):
        make_filename = os.path.join(self.output_dir, 'Makefile')
        cc_files = [self._make_base_filename(c.name) + ".cc" for c in classes]
        obj_files = [self._make_base_filename(c.name) + ".o" for c in classes]
        header_files = [self._make_base_filename(c.name) + ".hh" for c in classes]
        sstr = """
CXXFLAGS=-g -Wall
CC_FILES     = {0}
OBJ_FILES    = {1}
HEADER_FILES = {2}

EXEC=main

$(EXEC): $(OBJ_FILES) main.o
\tg++ -g $(OBJ_FILES) main.o -o $@

.o: $(HEADER_FILES)
\tg++ -c $(CXXFLAGS) $^ -o $@

clean:
\trm -f *.o *~ $(EXEC)

""".format(" ".join(cc_files), " ".join(obj_files), " ".join(header_files))

        with open(make_filename, 'w') as _file:
            _file.write(sstr)

    def _dump_cmake(self, classes):
        make_filename = os.path.join(self.output_dir, 'CMakeLists.txt')
        cc_files = [self._make_base_filename(c.name) + ".cc" for c in classes]

        sstr = """
cmake_minimum_required (VERSION 2.6)
project (GeneratedFromCodeGenerator)

add_executable(main
main.cc
{0})
""".format("\n".join(cc_files))

        with open(make_filename, 'w') as _file:
            _file.write(sstr)


    def _dump_main(self):
        main_filename = os.path.join(self.output_dir, "main.cc")
        with open(main_filename, 'w') as _file:
            _file.write("""
#include <cstdio>
#include <cstdlib>
#include <iostream>

int main(int argc, char ** argv){

/// ... your code here ...

  return EXIT_FAILURE;
}""")

    def _dump_header(self, _class):

        basename = self._make_base_filename(_class.name)
        header_filename = os.path.join(self.output_dir, basename+".hh")

        self.stage = 'header'
        sstr = self._format_class_declaration(_class)
        sstr += self._format_constructors(_class)
        sstr += self._format_methods(_class)
        sstr += self._format_members(_class)
        sstr += "};\n"

        with open(header_filename, 'w') as _file:
            # print header_filename
            _file.write("#ifndef __" + basename.upper() + "__HH__\n")
            _file.write("#define __" + basename.upper() + "__HH__\n\n")
            _file.write("/* " + '-'*74 + " */\n")

            if _class.inheritance is not None:
                for herit in _class.inheritance:
                    _file.write("#include \"" + self._make_base_filename(herit) + ".hh\"\n")

                    # if c.members is not None:
                    #     for encaps,membs in c.members.iteritems():
                    #         for name,m in membs.iteritems():
                    #             if m.type in self.base_types: continue
                    #             f.write("#include \"" +
                    #              self.make_base_filename(self.baseType(m.type)) + ".hh\"\n")
            _file.write(sstr)
            _file.write("\n/* " + '-'*74 + " */\n")
            _file.write("#endif //__" + basename.upper() + "__HH__\n")




    def _dump_cc_file(self, _class):

        basename = self._make_base_filename(_class.name)
        cc_filename = os.path.join(self.output_dir, basename+".cc")
        header_filename = os.path.join(self.output_dir, basename+".hh")

        self.stage = 'CC'
        sstr = self._format_constructors(_class)
        sstr += self._format_methods(_class)

        with open(cc_filename, 'w') as _file:
            # print CC_filename
            _file.write("#include \"" + os.path.basename(header_filename) + "\"\n")
            _file.write('/* ' + '-'*74 + ' */\n\n')
            _file.write(sstr)

    @classmethod
    def _format_class_declaration(cls, _class):
        sstr = """
/**
  * Documentation TODO
  */

"""

        sstr += "class " + _class.name

        if _class.inheritance is not None:
            sstr += ": public " + ", public ".join(_class.inheritance)

        sstr += "{\n"
        return sstr



    def _format_constructors(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            if _class.name in meths:
                if self.stage == 'header':
                    sstr += encaps + ':\n\n'
                for meth in meths[_class.name]:
                    sstr += self._format_method(_class, meth)
            if '~' + _class.name in meths:
                if self.stage == 'header' and sstr == "":
                    sstr += encaps + ':\n\n'
                for meth in meths['~' + _class.name]:
                    sstr += self._format_method(_class, meth)


        if not sstr == "" and self.stage == 'header':
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Constructors/Destructors                                                 */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr


    def _format_methods(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            meths_names = set(meths.keys()) - set([_class.name, '~' + _class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:
                if self.stage == 'header':
                    sstr += encaps + ':\n\n'

                for _name in meths_names:
                    for meth in meths[_name]:
                        sstr += self._format_method(_class, meth)
                sstr += "\n"

        if not sstr == "" and self.stage == 'header':
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Methods                                                                  */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr


    def _format_members(self, _class):
        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            membs = _class.getMembers(encaps)
            if len(membs) is not 0:
                if self.stage == 'header':
                    sstr += encaps + ':\n\n'

                for dummy_name, memb in membs.iteritems():
                    sstr += self._format_member(memb)
                sstr += "\n"

        if not sstr == "" and self.stage == 'header':
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Members                                                                  */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr



    def _format_method(self, _class, meth):

        if self.stage == 'header':
            sstr = "  //! Documentation TODO\n"
            sstr += "  "

            if meth.static:
                sstr += meth.static + " "
            if meth.virtual in ['virtual', 'pure virtual']:
                sstr += "virtual "
            if not meth.ret == "":
                sstr += meth.ret + " "
            sstr += meth.name + "("
            sstr += ", ".join([a + " " + b
                               for b, a in list(meth.args.iteritems())])
            sstr += ")"
            if meth.virtual == 'pure virtual':
                sstr += "=0"
            sstr += ";\n"

        if self.stage == 'CC':
            sstr = ""
            if meth.virtual == 'pure virtual':
                return ""

            sstr += meth.ret + " " + _class.name + "::" + meth.name + "("
            sstr += ", ".join([a + " " + b
                               for b, a in list(meth.args.iteritems())])
            sstr += "){\n\n}\n\n"
            sstr += "\n"
            sstr += """
/* --------------------------------------------------------------------------- */

"""


        return sstr

    @classmethod
    def _format_member(cls, memb):
        sstr = "  //!Documentation TODO\n"
        sstr += "  "
        if memb.static == 'static':
            sstr += 'static '
        sstr += memb.type + " " + memb.name + ";\n"
        return sstr


################################################################

def main():

    parser = argparse.ArgumentParser(description='CPP project producer for class representation')
    parser.add_argument('--class_file', '-c', help='The class file to process', required=True)
    parser.add_argument('--output_dir', '-o',
                        help='The directory where to put produced files', required=True)

    args = parser.parse_args()
    args = vars(args)
    os.makedirs(args['output_dir'])
    dumper_class = ClassDumperCPP(args['output_dir'])

    dumper_class.dump(args['class_file'])


if __name__ == '__main__':
    main()
