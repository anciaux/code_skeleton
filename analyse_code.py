#!/usr/bin/python

import subprocess,os,sys
import class_decriptor as cd
tmp_directory = '/tmp'
from class_dumper_classes import ClassDumperClasses

################################################################
import pygccxml.parser as gccparser
from pygccxml import declarations

################################################################
def cleanName(n,**kwargs):
    n = str(n)
    if ('template' in kwargs) and kwargs['template'] is False: 
        n = declarations.templates.name(str(n))
    if ('namespace' in kwargs) and kwargs['namespace'] is False: 
        ns = n.split('::')
        if len(ns) > 1: n = ns[-1]
    n = str(n)
    return n
################################################################
def analyzeFile(fnames,include_paths=None,cflags=None,class_cache={},dec_dir=None,required_namespace=None,**kwargs):
    if type(fnames) is not list: fnames = [fnames]
#    print fnames
    #parsing source file
    #configure GCC-XML parser
    #print include_paths
    if cflags is None: cflags = ''
    config = gccparser.gccxml_configuration_t( include_paths=include_paths,cflags=cflags, ignore_gccxml_output=True)
    try:
        decls = gccparser.parse( fnames, config)
    except Exception as e:
        print "Could not parse files '{0}'".format(fnames)
        print e
        return class_cache
    
    global_ns = declarations.get_global_namespace( decls )
    if required_namespace is not None:
        try: required_namespace = global_ns.namespace(required_namespace)
        except: return class_cache
    else: required_namespace = global_ns

        
    for class_ in required_namespace.classes():
        if dec_dir is not None:
            dec_file = declarations.declaration_files(class_)
            #print class_
            #print list(dec_file)
            #print dec_dir
            #print [os.path.dirname(f) for f in dec_file]
            flags = [dec_dir == os.path.dirname(f) for f in dec_file]
            flag = False
            for f in flags: flag |= f
            #print flags
            if not flag: continue 
            

        #print class_
        class_.name = cleanName(class_.name,**kwargs)
        inheritance = [cleanName(base.related_class.name,**kwargs) for base in class_.bases]
        #print inheritance
        if inheritance == []: inheritance = None
        c = cd.ClassDescriptor(class_.name,inheritance=inheritance)


        for memb in class_.vars(allow_empty=True):
            name = memb.name
            static = ""
            if memb.type_qualifiers.has_static: static = 'static'
            _type = cleanName(memb.type,**kwargs)
            encapsulation = memb.access_type
            c.addMember(name,_type,encapsulation,static,"")            
            
        for foo in class_.member_functions(allow_empty=True):
            name = foo.name
            static = ""
            if foo.has_static: static = 'static'
            const = foo.has_const
            virtual = foo.virtuality
            if virtual == 'not virtual': virtual = ''

            ret = cleanName(foo.return_type,**kwargs)
            encapsulation = foo.access_type
            args = foo.arguments
            
            args = [(cleanName(a.type,**kwargs),a.name) for a in args]
            c.addMethod(name,args,ret,encapsulation,virtual,static,const,"")
            #print c
        class_cache[class_.name] = c
    return class_cache
    

################################################################
def analyzeFiles(dirname,extension_list = ['.hh','.hpp'],output=None,**kwargs):
    read_classes = {}
    if os.path.isfile(dirname): files = [dirname]
    else:
        files = []
        for f in os.listdir(dirname):
            base,ext = os.path.splitext(f)
            if ext in extension_list: files.append(os.path.join(dirname,f))
            
    if os.path.isfile(dirname): dirname = None
    for f in files:
        analyzeFile(f,class_cache=read_classes,dec_dir=dirname,**kwargs)
    if output is not None:
        dumper_class = ClassDumperClasses(output)
        classes = [c for k,c in read_classes.iteritems()]
        dumper_class.dump(classes=classes)

    
################################################################
if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Code analyzer to produce .classes description')
    parser.add_argument('--sources','-s', help='The directory where the sources are loacted',required=True)
    parser.add_argument('--includes','-I', type=str,help='The needed includes')
    parser.add_argument('--cflags','-f', type=str,help='The needed flags')
    parser.add_argument('--template','-t', action='store_false',help='Remove templates from analysis')
    parser.add_argument('--namespace','-n', action='store_false',help='Remove namespaces from analysis')
    parser.add_argument('--output','-o', type=str,help='filename to store output')
    parser.add_argument('--required_namespace','-rn', type=str,help='filter classes based on namespace')
    

    args = parser.parse_args()
    args = vars(args)
    src_dir = args['sources']
    inc_dirs = None
    cflags = args['cflags']
    if cflags is not None: cflags = cflags.replace('\-','-')
    args['cflags'] = cflags
    if args['includes'] is not None: inc_dirs = args['includes'].split(';')
    
    analyzeFiles(src_dir,include_paths=inc_dirs,**args)
    
