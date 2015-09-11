#!/usr/bin/python

import inspect
import imp
import subprocess,os,sys
import class_decriptor as cd
tmp_directory = '/tmp'
from class_dumper_classes import ClassDumperClasses

################################################################
def analyzeFile(fnames,**kwargs):
    print fnames
    modfile = fnames
    modname = os.path.basename(modfile)
    modname = os.path.splitext(modname)[0]
    mymod = imp.load_source(modname,modfile)
    for k,v, in mymod.__dict__.iteritems():
        if inspect.isclass(v):
            print k
            for n,m in inspect.getmembers(v):
                print n


################################################################
def analyzeFiles(dirname,extension_list = ['.py'],output=None,**kwargs):
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

    args = parser.parse_args()
    args = vars(args)
    src_dir = args['sources']
    
    analyzeFiles(src_dir,**args)
    
