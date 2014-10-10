from class_dumper import ClassDumper

class ClassDumperDOT(ClassDumper):
    def __init__(self):
        ClassDumper.__init__(self)
        self.encaps_symbol = {'public':'+','private':'-','protected':'#'} 
        
    def dump(self,class_file,output_filename):
        sstr = 'digraph "test"\n{'
        sstr += """
edge [fontname="Helvetica",fontsize="10",labelfontname="Helvetica",labelfontsize="10"];
node [fontname="Helvetica",fontsize="10",shape=record];
"""

        sstr += ClassDumper.dump(self,class_file)
        sstr += "}"

        with open(output_filename,'w') as f:
            f.write(sstr)
            f.close()
        
        
    def dumpFile(self,c):
        sstr =  self.formatClassDeclaration(c)
        sstr += self.formatConstructors(c)
        sstr += self.formatMethods(c)
        sstr += self.formatMembers(c)
        sstr += '}"];\n'
        sstr += self.formatInheritance(c)
        return sstr

    def formatClassDeclaration(self,c):
        sstr = '"{0}" '.format(c.name)
        sstr += '[label="{' + format(c.name) + "\\n"
        return sstr

    def formatInheritance(self,c):
        if c.inheritance is not None:
            sstr = ""
            for mother in c.inheritance:
                sstr += '"{0}" '.format(mother) + " -> " + '"{0}" '.format(c.name)
                sstr += '[style="solid",color="midnightblue",fontname="Helvetica",arrowtail="onormal",fontsize="10",dir="back"];\n'
            return sstr
        return ""


        
    def formatConstructors(self,c):
        sstr = ""
        for encaps in ['public','private', 'protected']:
            
            meths = c.getMethods(encaps)
            if c.name in meths:
                if sstr == "":  sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths[c.name]:
                    sstr += self.formatMethod(c,cons)
                    sstr += "\\l"
            if '~' + c.name in meths:
                if sstr == "":  sstr = "|"
                sstr += self.encaps_symbol[encaps] + " "
                for cons in meths['~' + c.name]:
                    sstr += self.formatMethod(c,cons)
                    sstr += "\\l"

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
                        if sstr == "":  sstr = "|"
                        sstr += self.encaps_symbol[encaps] + " "
                        sstr += self.formatMethod(c,m)
                        sstr += "\\l"

        return sstr


    def formatMembers(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            membs = c.getMembers(encaps)
            if len(membs) is not 0:
                
                for n,m in membs.iteritems():
                    if sstr == "":  sstr = "|"
                    sstr += self.encaps_symbol[encaps] + " "
                    sstr += self.formatMember(c,m)
                    sstr += "\\l"

        return sstr



    def formatMethod(self,c,m):
        arg_types = list(m.args.iteritems())
        arg_types = [a for b,a in arg_types]
        sstr = ""
        if m.static: sstr += m.static + " "
        if m.ret:    sstr += m.ret + " "
        sstr += m.name + "(" + ",".join(arg_types) + ")"
        if m.virtual == 'pure virtual': sstr += "=0"

        return sstr

    def formatMember(self,c,m):
        return m.type + " " + m.name

import argparse
import subprocess
import os
    
if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(description='DOT graph producer for class representation')
    parser.add_argument('--class_file','-c', help='The class file to process',required=True)
    parser.add_argument('--format','-f' , default="pdf", help='The format of the produced graph file')
    parser.add_argument('--output','-o' , help='The file to be produced',required=True)

    args = parser.parse_args()
    args = vars(args)
    dumper_class = ClassDumperDOT()
    dot_file = os.path.splitext(args['output'])[0] + ".dot"

    dumper_class.dump(args['class_file'],dot_file)
    exe           = ['dot']
    option_format = ['-T'+args['format'] ]
    option_output = ['-o', args['output'] ]
    option_input  = ['test.dot']
    subprocess.call(exe+option_format+option_output+option_input)

