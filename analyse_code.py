#!/usr/bin/python

import subprocess,os,sys
import class_decriptor as cd
tmp_directory = '/tmp'

################################################################
import pygccxml.parser as gccparser
from pygccxml import declarations
################################################################
def analyzeFile(fnames,include_paths=None,cflags=None,class_cache={}):
    if type(fnames) is not list: fnames = [fnames]
#    print fnames
    #parsing source file
    #configure GCC-XML parser
    print include_paths
    if cflags is None: cflags = ''
    config = gccparser.gccxml_configuration_t( include_paths=include_paths,cflags=cflags, ignore_gccxml_output=True)
    decls = gccparser.parse( fnames, config)
    global_ns = declarations.get_global_namespace( decls )
    akantu = global_ns.namespace('akantu')
    
    for class_ in akantu.classes():
        print class_
        print declarations.declaration_files(class_)
        inheritance = [base.related_class.name for base in class_.bases]
        print inheritance
        if inheritance == []: inheritance = None
        c = cd.ClassDescriptor(class_.name,inheritance=inheritance)
        for foo in class_.member_functions(allow_empty=True):
            name = foo.name
            static = foo.has_static
            const = foo.has_const
            virtual = foo.virtuality
            if virtual == 'not virtual': virtual = ''
            ret = str(foo.return_type)
            encapsulation = foo.access_type
            args = foo.arguments
            args = [(a.name,str(a.type)) for a in args]
            c.addMethod(name,args,ret,encapsulation,virtual,static,const,"")
        class_cache[class_.name] = c
    return class_cache
    

################################################################
def analyzeFiles(dirname,extension_list = ['.hh','.hpp'],include_paths=None,cflags=None):
    read_classes = {}
    for f in os.listdir(dirname):
        base,ext = os.path.splitext(f)
        if ext in extension_list:
            analyzeFile(os.path.join(dirname,f),include_paths=include_paths,cflags=cflags,class_cache=read_classes)
    print read_classes.keys()
            
################################################################
if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Code analyzer to produce .classes description')
    parser.add_argument('--sources','-s', help='The directory where the sources are loacted',required=True)
    parser.add_argument('--includes','-I', type=str,help='The needed includes')
    parser.add_argument('--cflags','-f', type=str,help='The needed flags')
    

    args = parser.parse_args()
    args = vars(args)
#    print args
    src_dir = args['sources']
    inc_dirs = None
    cflags = args['cflags']
    cflags = cflags.replace('\-','-')
#    print cflags
    if args['includes'] is not None: inc_dirs = args['includes'].split(';')
    
    analyzeFiles(src_dir,include_paths=inc_dirs,cflags=cflags)
    
