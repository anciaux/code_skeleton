#!/usr/bin/python

from class_dumper import ClassDumper
from class_reader import ClassReader
import os, re 

class ClassDumperPython(ClassDumper):
    def __init__(self,output_dir):
        ClassDumper.__init__(self)
        self.output_dir = output_dir
        self.nb_tabulation = 0

    def makeBaseFilename(self,class_name):
        name = re.sub(r'([0-9]|[A-Z0-9])','_\g<1>',class_name)
        name = name.lower()
        
        if name[0] == '_':
            name = name[1:]
        return name
        
    def dump(self,class_file):
        cls_reader = ClassReader()
        classes = cls_reader.read(class_file)
        for c in classes:
            basename = self.makeBaseFilename(c.name)
            class_filename = os.path.join(self.output_dir,basename+".py")
            with open(class_filename,'w') as f:
                self.dumpClass(c,f)

        return ""

        
    def dumpClass(self,c,f):

        sstr =  self.formatClassDeclaration(c)
        self.incTabulation()
        sstr += self.formatConstructors(c)
        sstr += self.formatMethods(c)
        sstr += self.formatMembers(c)
        sstr += "\n" 


        f.write("## -------------------------------------------------------------------------- ##\n")

        if c.inheritance is not None:
            for herit in c.inheritance:
                f.write("#include \"" + self.makeBaseFilename(herit) + ".hh\"\n")                

        f.write(sstr)
        f.write("## -------------------------------------------------------------------------- ##\n")

    def formatClassDeclaration(self,c):
        sstr = "class " + c.name

        if c.inheritance is not None:
            sstr += ": public " + ", public ".join(c.inheritance)
            
        sstr += "{\n"
        return sstr


        
    def formatConstructors(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            meths = c.getMethods(encaps)
            if c.name in meths:
                for m in meths[c.name]:
                    sstr += self.formatMethod(c,m)
            if '~' + c.name in meths:
                for m in meths['~' + c.name]:
                    sstr += self.formatMethod(c,m)
        

        if not sstr == "": 
            sstr = """
{0}## ------------------------------------------------------------------ ##
{0}## Constructors/Destructors                                           ##
{0}## ------------------------------------------------------------------ ##

""".format(self.getTabulation()) + sstr 

        return sstr


    def formatMethods(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            meths = c.getMethods(encaps)
            meths_names = set(meths.keys()) - set([c.name,'~'+c.name])
            meths_names = list(meths_names)
            if len(meths_names) is not 0:

                for n in meths_names:
                    for m in meths[n]:
                        sstr += self.formatMethod(c,m)
                        sstr += "\n"

        if not sstr == "":
            sstr = """
{0}## ------------------------------------------------------------------ ##
{0}## Methods                                                            ##
{0}## ------------------------------------------------------------------ ##

""".format(self.getTabulation()) + sstr

        return sstr


    def formatMembers(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            membs = c.getMembers(encaps)
            if len(membs) is not 0:
                for n,m in membs.iteritems():
                    sstr += self.formatMember(c,m)
                sstr += "\n"

        if not sstr == "":
            sstr = """
{0}## ------------------------------------------------------------------ ##
{0}## Members                                                            ##
{0}## ------------------------------------------------------------------ ##

""".format(self.getTabulation()) + sstr

        return sstr



    def formatMethod(self,c,m):

        sstr = ""
        if m.static: raise
        sstr += self.getTabulation() + "def " + m.name + "("
        sstr += ", ".join([b for b,a in list(m.args.iteritems())])
        sstr +=  "):\n"

        self.incTabulation()
        
        if m.virtual == 'pure virtual': 
                sstr += self.getTabulation() + "raise Exception('This is a pure virtual method')\n"


        sstr += self.getTabulation() + "pass\n"

        self.decTabulation()
            
        return sstr

    def formatMember(self,c,m):
        sstr = "  "
        if m.static == 'static': sstr += 'static '
        sstr += m.type + " " + m.name + ";\n"
        return sstr

    def getTabulation(self):
        return "\t" * self.nb_tabulation

    def incTabulation(self):
        self.nb_tabulation += 1

    def decTabulation(self):
        self.nb_tabulation -= 1

        
import argparse
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CPP project producer for class representation')
    parser.add_argument('--class_file','-c', help='The class file to process',required=True)
    parser.add_argument('--output_dir','-o' , help='The directory where to put produced files',required=True)

    args = parser.parse_args()
    args = vars(args)
    os.makedirs(args['output_dir'])
    dumper_class = ClassDumperPython(args['output_dir'])

    dumper_class.dump(args['class_file'])
