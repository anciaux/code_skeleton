#!/usr/bin/python

import inspect
import imp
import re
import subprocess,os,sys
import class_decriptor as cd
tmp_directory = '/tmp'
from class_dumper_classes import ClassDumperClasses

################################################################
def getClassEncapsulation(name):
#    print "CCCCCCCCCCCc " + name
    if re.match('_(.*?)_(.*)',name):
        m = re.match('_(.*?)_(.*)',name)
        name = m.group(2)
        if name[0] == '_':
            encaps = 'private'
            name = name[1:]
        else:              encaps = 'protected'
        return name,encaps        
    return name,'public'

################################################################
def getEncapsulation(name):
#    print "CCCCCCCCCCCc " + name
    if re.match('_(.*)',name):
        m = re.match('_(.*)',name)
        name = m.group(1)
        if name[0] == '_':
            encaps = 'private'
            name = name[1:]
        else: encaps = 'protected'
        return name,encaps        
    return name,'public'

################################################################
def analyzeFile(fnames,class_cache={},**kwargs):
    print fnames
    modfile = fnames
    modname = os.path.basename(modfile)
    modname = os.path.splitext(modname)[0]
    mymod = imp.load_source(modname,modfile)

    exclude_members = ['__module__','__doc__']
    for k,v, in mymod.__dict__.iteritems():
        if inspect.isclass(v):
            print k
            c = cd.ClassDescriptor(k,inheritance=None)
            for name,m in inspect.getmembers(v) :
                #print name
                if name in exclude_members: continue
                if inspect.ismethod(m):
                    args = [("PyObject",a) for a in inspect.getargspec(m).args if not a == 'self']
#                    print name
                    encaps = 'public'
                    if name == '__init__':
                        name = k
                        lines = inspect.getsourcelines(m)
#                        print lines
                        for l in lines[0]:
                            m = re.match('\s*self\.(.*)=(.*)',l)
                            if m:
                                name = m.group(1)
                                member,encaps_member = getEncapsulation(name)
#                                print member,encaps
                                c.addMember(member,"PyObject",encaps,"","")                                
                                
                    elif re.match('__.*__',name): pass
                    else:
                        name,encaps = getClassEncapsulation(name)

                    c.addMethod(name,args,"PyObject",encaps,"","","","")
            class_cache[k] = c
    return class_cache


################################################################
def analyzeFiles(dirname,extension_list = ['.py'],output=None,import_dir=None,**kwargs):

    if import_dir is not None:
        if type(import_dir) == str: import_dir = import_dir.split(':')
        for p in import_dir:
            path = os.path.expanduser(p)
            sys.path.append(path)

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
    parser.add_argument('--output','-o', type=str,help='filename to store output')
    parser.add_argument('--import_dir','-i', type=str,help='directories to scan for imports')

    args = parser.parse_args()
    args = vars(args)
    src_dir = args['sources']
    
    analyzeFiles(src_dir,**args)
    
