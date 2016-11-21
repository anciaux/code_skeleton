#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
from class_dumper import ClassDumper
from class_reader import ClassReader
################################################################

class ClassDumperClasses(ClassDumper):
    " Class emplyed to output to classes text format "

    def __init__(self, output_file):
        ClassDumper.__init__(self)
        self.output_file = output_file
        self.nb_tabulation = 0

    def dump(self, class_file=None, classes=None):
        fout = open(self.output_file, 'w')

        if class_file is not None:
            cls_reader = ClassReader()
            classes = cls_reader.read(class_file)
        for _class in classes:
            self.dump_class(_class, fout)

    def dump_class(self, _class, _file):

        " dumps a class into the provided file "

        sstr = self.format_class_declaration(_class)
        self.incTabulation()
        sstr += self.format_constructors(_class)
        sstr += self.format_methods(_class)
        sstr += self.format_members(_class)
        sstr += "\n"
        self.decTabulation()
        _file.write(sstr)

    def format_class_declaration(self, _class):

        " forge a str representing the class "

        sstr = "class " + _class.name

        if _class.inheritance is not None:
            sstr += "(" + ", ".join(_class.inheritance) + ")"

        sstr += "\n"
        return sstr



    def format_constructors(self, _class):

        " forge a str representing the constructor "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:
            meths = _class.getMethods(encaps)
            if _class.name in meths:
                for meth in meths[_class.name]:
                    sstr += self.formatMethod(_class, meth)

        for encaps in ['public', 'private', 'protected']:
            meths = _class.getMethods(encaps)
            if '~' + _class.name in meths:
                for meth in meths['~' + _class.name]:
                    sstr += self.formatMethod(_class, meth)

        return sstr


    def format_methods(self, _class):

        " forge a str representing methods "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            meths = _class.getMethods(encaps)
            meths_names = set(meths.keys()) - set([_class.name, '~' + _class.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:
                for _name in meths_names:
                    for meth in meths[_name]:
                        sstr += self.formatMethod(_class, meth)

        return sstr


    def format_members(self, _class):

        " forge a str representing members "

        sstr = ""

        for encaps in ['public', 'private', 'protected']:

            membs = _class.getMembers(encaps)
            if len(membs) is not 0:
                for dummy_n, memb in membs.iteritems():
                    sstr += self.formatMember(_class, memb)
                    sstr += "\n"
        return sstr



    def formatMethod(self, _class, meth):

        sstr = self.get_tabulation()
        sstr += m.encapsulation + " "
        if m.static: sstr += m.static + " "
        if m.virtual: sstr += m.virtual + " "
        if m.ret: sstr += m.ret + " "

        sstr += m.name + "("
        sstr += ", ".join([a + " " + b for b,a in list(m.args.iteritems())])
        sstr +=  ")"
        if m.const: sstr += " const"
        sstr+= ";\n"

        self.incTabulation()

        self.decTabulation()

        return sstr

    def formatMember(self,c,m):
        sstr = self.getTabulation()
        sstr += m.encapsulation + " "
        if m.static == 'static': sstr += m.static
        sstr += m.type + " " + m.name + ';'
        return sstr

    def getTabulation(self):
        return "  " * self.nb_tabulation

    def incTabulation(self):
        self.nb_tabulation += 1

    def decTabulation(self):
        self.nb_tabulation -= 1


import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Classes descriptor format producer for class representation')
    parser.add_argument('--class_file','-c', help='The class file to process',required=True)
    parser.add_argument('--output_file','-o' , help='The file where to put the classes description',required=True)

    args = parser.parse_args()
    args = vars(args)
    dumper_class = ClassDumperClasses(args['output_file'])
    dumper_class.dump(class_file=args['class_file'])
