#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author Guillaume Anciaux <guillaume.anciaux@epfl.ch>

@brief  analyze a python code

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
import inspect
import imp
import re
import os
import sys
import class_decriptor as cd
from class_dumper_classes import ClassDumperClasses
################################################################

def get_class_encapsulation(name):
    # print "CCCCCCCCCCCc " + name
    if re.match('_(.*?)_(.*)', name):
        match = re.match('_(.*?)_(.*)', name)
        name = match.group(2)
        if name[0] == '_':
            encaps = 'private'
            name = name[1:]
        else:
            encaps = 'protected'
        return name, encaps
    return name, 'public'

################################################################
def get_encapsulation(name):

    # print "CCCCCCCCCCCc " + name
    if re.match('_(.*)', name):
        match = re.match('_(.*)', name)
        name = match.group(1)
        if name[0] == '_':
            encaps = 'private'
            name = name[1:]
        else: encaps = 'protected'
        return name, encaps
    return name, 'public'

################################################################
def analyze_file(fnames, class_cache={}, **kwargs):

    print fnames
    modfile = fnames
    modname = os.path.basename(modfile)
    modname = os.path.splitext(modname)[0]
    mymod = imp.load_source(modname, modfile)

    exclude_members = ['__module__', '__doc__']
    for k, v, in mymod.__dict__.iteritems():
        if inspect.isclass(v):
            print k
            class_desc = cd.ClassDescriptor(k, inheritance=None)
            for name, memb in inspect.getmembers(v):
                #print name
                if name in exclude_members:
                    continue
                if inspect.ismethod(memb):
                    args = [("PyObject", a) for a in inspect.getargspec(memb).args
                            if not a == 'self']
                    # print name
                    encaps = 'public'
                    if name == '__init__':
                        name = k
                        lines = inspect.getsourcelines(memb)
#                        print lines
                        for line in lines[0]:
                            match = re.match(r'\s*self\.(.*)=(.*)', line)
                            if match:
                                name = match.group(1)
                                member, dummy_encaps_member = get_encapsulation(name)
                                # print member,encaps
                                class_desc.addMember(member, "PyObject", encaps, "", "")

                    elif re.match('__.*__', name):
                        pass
                    else:
                        name, encaps = get_class_encapsulation(name)

                    class_desc.addMethod(name, args, "PyObject", encaps, "", "", "", "")
            class_cache[k] = class_desc
    return class_cache


################################################################
def analyzeFiles(dirname,extension_list = ['.py'],output=None,import_dir=None,**kwargs):

    if import_dir is not None:
        if isinstance(import_dir, str):
            import_dir = import_dir.split(':')
        for _dir in import_dir:
            path = os.path.expanduser(_dir)
            sys.path.append(path)

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
        analyze_file(filename, class_cache=read_classes, dec_dir=dirname, **kwargs)
    if output is not None:
        dumper_class = ClassDumperClasses(output)
        classes = [c for dummy_k, c in read_classes.iteritems()]
        dumper_class.dump(classes=classes)


################################################################
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Code analyzer to produce .classes description')
    parser.add_argument('--sources', '-s',
                        help='The directory where the sources are loacted', required=True)
    parser.add_argument('--output', '-o', type=str, help='filename to store output')
    parser.add_argument('--import_dir', '-i', type=str, help='directories to scan for imports')

    args = parser.parse_args()
    args = vars(args)
    src_dir = args['sources']

    analyzeFiles(src_dir, **args)

################################################################
if __name__ == '__main__':
    main()
