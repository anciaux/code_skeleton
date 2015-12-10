#!/usr/bin/python

################################################################
import os, re, sys
import argparse
from class_dumper    import ClassDumper
from class_dumper_classes    import ClassDumperClasses
from class_reader    import ClassReader
from class_decriptor import Method
################################################################

def merge(files,output):
    print files 
    classes = []
    for class_file in files:
        cls_reader = ClassReader()
        classes.append(cls_reader.read(class_file))

    print len(classes)," files to merge"

    merged_classes = {}

    for _c in classes:
        for c in _c:
            name = c.name
            if c.name not in merged_classes: merged_classes[c.name] = c
            else:
                pclass = merged_classes[c.name]
                for encaps,methods in c.methods.iteritems():
                    for mname,method in methods.iteritems():
                        if mname in pclass.methods[encaps]:
                            if not pclass.methods[encaps][mname] == method:
                                print "Warming: ",((c.name,encaps,mname))
                        else:
                            pclass.methods[encaps][mname] = method

                for encaps,members in c.members.iteritems():
                    for mname,member in members.iteritems():
                        if mname in pclass.members[encaps]:
                            if not pclass.members[encaps][mname] == member:
                                print "Warming: ",((c.name,encaps,mname))
                            else:
                                pclass.members[encaps][mname] = member

                        

    #for c in merged_classes:
    #    print merged_classes[c].name


    dumper_class = ClassDumperClasses('merged_file.classes')
    fout = open(dumper_class.output_file,'w')
    for name,c in merged_classes.iteritems():
        dumper_class.dumpClass(c,fout)


################################################################
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Classes descriptor merge')
    parser.add_argument('class_files', nargs='+', help='The class files to merge')
    parser.add_argument('--output_file','-o' , help='The file where to put the classes description',required=True)

    args = parser.parse_args()
    args = vars(args)
    

    class_files = args['class_files']
    output_file = args['output_file']

    merge(class_files,output_file)

    
