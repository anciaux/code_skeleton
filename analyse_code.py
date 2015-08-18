#!/usr/bin/python

import subprocess,os,sys
import class_decriptor as cd
tmp_directory = '/tmp'
from class_dumper_classes import ClassDumperClasses

################################################################
import pygccxml.parser as gccparser
from pygccxml import declarations
################################################################
def analyzeFile(fnames,include_paths=None,cflags=None,class_cache={}):
    if type(fnames) is not list: fnames = [fnames]
#    print fnames
    #parsing source file
    #configure GCC-XML parser
    #print include_paths
    if cflags is None: cflags = ''
    config = gccparser.gccxml_configuration_t( include_paths=include_paths,cflags=cflags, ignore_gccxml_output=True)
    decls = gccparser.parse( fnames, config)
    global_ns = declarations.get_global_namespace( decls )
    akantu = global_ns.namespace('akantu')
    
    for class_ in akantu.classes():
        print class_
        #print declarations.declaration_files(class_)
        class_.name = declarations.templates.name(class_.name)
        inheritance = [base.related_class.name for base in class_.bases]
        #print inheritance
        if inheritance == []: inheritance = None
        c = cd.ClassDescriptor(class_.name,inheritance=inheritance)

        def cleanName(n):
            n = declarations.templates.name(str(n))
            ns = n.split('::')
            if len(ns) > 1: n = ns[-1]
            if not type(n) == str: raise Exception(str(n) + " - " + str(ns))
            return n

        for memb in class_.vars(allow_empty=True):
            name = memb.name
            static = ""
            if memb.type_qualifiers.has_static: static = 'static'
            _type = cleanName(memb.type)
            encapsulation = memb.access_type
            c.addMember(name,_type,encapsulation,static,"")            
            
        for foo in class_.member_functions(allow_empty=True):
            name = foo.name
            static = ""
            if foo.has_static: static = 'static'
            const = foo.has_const
            virtual = foo.virtuality
            if virtual == 'not virtual': virtual = ''

            ret = cleanName(foo.return_type)
            encapsulation = foo.access_type
            args = foo.arguments
            
            args = [(cleanName(a.type),a.name) for a in args]
            c.addMethod(name,args,ret,encapsulation,virtual,static,const,"")
            #print c
        class_cache[class_.name] = c
    return class_cache
    

################################################################
def analyzeFiles(dirname,extension_list = ['.cc','.cpp'],include_paths=None,cflags=None):
    read_classes = {}
    for f in os.listdir(dirname):
        base,ext = os.path.splitext(f)
        if ext in extension_list:
            analyzeFile(os.path.join(dirname,f),include_paths=include_paths,cflags=cflags,class_cache=read_classes)
    dumper_class = ClassDumperClasses('test.classes')
    classes = [c for k,c in read_classes.iteritems()]
    dumper_class.dump(classes=classes)

    
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
    if cflags is not None:
        cflags = cflags.replace('\-','-')
#    print cflags
    if args['includes'] is not None: inc_dirs = args['includes'].split(';')
    
    analyzeFiles(src_dir,include_paths=inc_dirs,cflags=cflags)
    
