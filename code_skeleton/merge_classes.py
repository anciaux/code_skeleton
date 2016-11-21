#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module for merging class representations

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
import argparse
from code_skeleton.class_dumper_classes    import ClassDumperClasses
from code_skeleton.class_reader    import ClassReader
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


def merge(files, output_filename):

    "takes a list of files and produce a single one"
    print (files)
    classes = []
    for class_file in files:
        cls_reader = ClassReader()
        classes.append(cls_reader.read(class_file))

    print (len(classes), " files to merge")

    merged_classes = {}

    for _class in classes:
        for c in _class:
            name = c.name
            if c.name not in merged_classes:
                merged_classes[c.name] = c

            else:
                pclass = merged_classes[c.name]
                for encaps, methods in c.methods.iteritems():
                    for mname, method in methods.iteritems():
                        if mname in pclass.methods[encaps]:
                            if not pclass.methods[encaps][mname] == method:
                                print ("Warming: ", ((c.name, encaps, mname)))
                        else:
                            pclass.methods[encaps][mname] = method

                for encaps, members in c.members.iteritems():
                    for mname, member in members.iteritems():
                        if mname in pclass.members[encaps]:
                            if not pclass.members[encaps][mname] == member:
                                print ("Warming: ", ((c.name, encaps, mname)))
                            else:
                                pclass.members[encaps][mname] = member



    #for c in merged_classes:
    #    print merged_classes[c].name


    dumper_class = ClassDumperClasses('output_filename')
    fout = open(dumper_class.output_file, 'w')
    for name, _class in merged_classes.iteritems():
        dumper_class.dumpClass(_class, fout)


################################################################

def main():
    parser = argparse.ArgumentParser(description='Classes descriptor merge')
    parser.add_argument('class_files', nargs='+', help='The class files to merge')
    parser.add_argument('--output_file', '-o',
                        help='The file where to put the classes description', required=True)

    args = parser.parse_args()
    args = vars(args)

    class_files = args['class_files']
    output_file = args['output_file']

    merge(class_files, output_file)


if __name__ == '__main__':
    main()
