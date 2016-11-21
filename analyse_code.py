#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  Module in charge of analysing a code

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
import pygccxml.parser as gccparser
from pygccxml import declarations
import class_decriptor as cd
from class_dumper_classes import ClassDumperClasses
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

TMP_DIRECTORY = '/tmp'
################################################################


def clean_name(_name, **kwargs):
    _name = str(_name)
    if ('template' in kwargs) and kwargs['template'] is False:
        _name = declarations.templates.name(str(_name))
    if ('namespace' in kwargs) and kwargs['namespace'] is False:
        namespace = _name.split('::')
        if len(namespace) > 1:
            _name = namespace[-1]
    _name = str(_name)
    return _name
################################################################

def analyzeFile(fnames, include_paths=None, cflags=None, class_cache={},
                dec_dir=None, required_namespace=None, **kwargs):

    if not isinstance(fnames, list):
        fnames = [fnames]

    # print fnames
    # parsing source file
    # configure GCC-XML parser
    # print include_paths

    if cflags is None:
        cflags = ''

    config = gccparser.gccxml_configuration_t(include_paths=include_paths,
                                              cflags=cflags,
                                              ignore_gccxml_output=True)
    try:
        decls = gccparser.parse(fnames, config)
    except Exception as ex:
        print "Could not parse files '{0}'".format(fnames)
        print ex
        raise
        # return class_cache

    global_ns = declarations.get_global_namespace(decls)
    if required_namespace is not None:
        try:
            required_namespace = global_ns.namespace(required_namespace)
        except Exception as ex:
            return class_cache
    else:
        required_namespace = global_ns


    for class_ in required_namespace.classes():
        if dec_dir is not None:
            dec_file = declarations.declaration_files(class_)
            #print class_
            #print list(dec_file)
            #print os.path.abspath(dec_dir)
            #print [os.path.dirname(f) for f in dec_file]
            flags = [os.path.abspath(dec_dir) == os.path.abspath(os.path.dirname(f))
                     for f in dec_file]
            flag = False
            for _flag in flags:
                flag |= _flag
            #print flags
            #print flag
            if not flag:
                continue


        print class_
        print class_.name
        class_.name = clean_name(class_.name, **kwargs)
        inheritance = [clean_name(base.related_class.name, **kwargs) for base in class_.bases]
        #print inheritance
        if inheritance == []:
            inheritance = None
        c = cd.ClassDescriptor(class_.name, inheritance=inheritance)

        for memb in class_.vars(allow_empty=True):
            name = memb.name
            static = ""
            if memb.type_qualifiers.has_static:
                static = 'static'
            _type = clean_name(memb.type, **kwargs)
            encapsulation = memb.access_type
            c.addMember(name, _type, encapsulation, static, "")

        for cons in class_.constructors():
            name = cons.name
            static = ""
            const = cons.has_const
            virtual = cons.virtuality
            if virtual == 'not virtual':
                virtual = ''

            ret = ""
            encapsulation = cons.access_type
            args = cons.arguments

            args = [(clean_name(a.type, **kwargs), a.name) for a in args]
            c.addMethod(name, args, ret, encapsulation, virtual, static, const, "")

        for func in class_.member_functions(allow_empty=True):
            name = func.name
            static = ""
            if func.has_static:
                static = 'static'
            const = func.has_const
            virtual = func.virtuality
            if virtual == 'not virtual':
                virtual = ''

            ret = clean_name(func.return_type, **kwargs)
            encapsulation = func.access_type
            args = func.arguments

            args = [(clean_name(a.type, **kwargs), a.name) for a in args]
            c.addMethod(name, args, ret, encapsulation, virtual, static, const, "")
        class_cache[class_.name] = c
    return class_cache


################################################################
def analyze_files(dirname, extension_list=None, output=None, **kwargs):

    if extension_list is None:
        extension_list = ['.hh', '.hpp']
        
    if output is None:
        raise Exception('output is not provided')
    read_classes = {}
    if os.path.isfile(dirname):
        files = [dirname]
    else:
        files = []
        for filename in os.listdir(dirname):
            dummy_base, ext = os.path.splitext(filename)
            if ext in extension_list:
                files.append(os.path.join(dirname, filename))

    if os.path.isfile(dirname):
        dirname = None
    for filename in files:
        analyzeFile(filename, class_cache=read_classes, dec_dir=dirname, **kwargs)

    print read_classes.keys()


    if output is not None:
        dumper_class = ClassDumperClasses(output)
        classes = [c for dummy_k, c in read_classes.iteritems()]
        dumper_class.dump(classes=classes)


################################################################
def main():

    parser = argparse.ArgumentParser(description='Code analyzer to produce .classes description')
    parser.add_argument('--sources', '-s',
                        help='The directory where the sources are loacted',
                        required=True)
    parser.add_argument('--includes', '-I', type=str, help='The needed includes')
    parser.add_argument('--cflags', '-f', type=str, help='The needed flags')
    parser.add_argument('--template', '-t', action='store_false',
                        help='Remove templates from analysis')
    parser.add_argument('--namespace', '-n', action='store_false',
                        help='Remove namespaces from analysis')
    parser.add_argument('--output', '-o', type=str,
                        help='filename to store output')
    parser.add_argument('--required_namespace', '-rn', type=str,
                        help='filter classes based on namespace')


    args = parser.parse_args()
    args = vars(args)
    src_dir = args['sources']
    inc_dirs = None
    cflags = args['cflags']
    if cflags is not None:
        cflags = cflags.replace('\-','-')
    args['cflags'] = cflags
    if args['includes'] is not None:
        inc_dirs = args['includes'].split(';')

    analyze_files(src_dir, include_paths=inc_dirs, **args)

################################################################

if __name__ == '__main__':
    main()
