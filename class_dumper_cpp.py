from class_dumper import ClassDumper

class ClassDumperCPP(ClassDumper):
    def __init__(self):
        ClassDumper.__init__(self)


    def dumpHeader(self,c):
        self.stage = 'header'
        sstr =  self.formatClassDeclaration(c)
        sstr += self.formatConstructors(c)
        sstr += self.formatMethods(c)
        sstr += self.formatMembers(c)
        sstr += "};\n" 
        print sstr

    def dumpCCFile(self,c):
        self.stage = 'CC'
        sstr = self.formatConstructors(c)
        sstr += self.formatMethods(c)
        print sstr
        
    def dumpFile(self,c):
        self.dumpHeader(c)
        self.dumpCCFile(c)
        
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
                if self.stage == 'header': sstr += encaps + ':\n\n'
                sstr += self.formatMethod(meths[name])
        

        if not sstr == "":
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Constructors/Destructors                                                 */
  /* ------------------------------------------------------------------------ */

""" + sstr 

        return sstr


    def formatMethods(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            meths = c.getMethods(encaps)
            meths_names = set(meths.keys()) - set(c.name)
            meths_names = list(meths_names)
            if len(meths_names) is not 0:
                if self.stage == 'header': sstr += encaps + ':\n\n'

                for n in meths_names:
                    for m in meths[n]:
                        sstr += self.formatMethod(c,m)
                sstr += "\n"

        if not sstr == "" and self.stage == 'header':
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Methods                                                                  */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr


    def formatMembers(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            membs = c.getMembers(encaps)
            if len(membs) is not 0:
                if self.stage == 'header': sstr += encaps + ':\n\n'

                for n,m in membs.iteritems():
                    sstr += self.formatMember(c,m)
                sstr += "\n"

        if not sstr == "" and self.stage == 'header':
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Members                                                                  */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr



    def formatMethod(self,c,m):

        sstr = ""
        if self.stage == 'header':
            sstr = "  "
            if m.virtual in ['virtual','pure virtual']:
                sstr += "virtual "
            sstr += m.ret + " " + m.name + "("
            sstr += ", ".join([a + " " + b for b,a in list(m.args.iteritems())])
            sstr +=  ");\n"

        if self.stage == 'CC':
            sstr = ""
            sstr += m.ret + " " + c.name + "::" + m.name + "("
            sstr += ", ".join([a + " " + b for b,a in list(m.args.iteritems())])
            sstr +=  "){\n\n}\n\n"
            sstr += "\n"
            sstr += """
/* --------------------------------------------------------------------------- */

"""

            
        return sstr

    def formatMember(self,c,m):
        sstr = "  " + m.type + " " + m.name + ";"
        return sstr

if __name__ == '__main__':
    dumper_class = ClassDumperCPP()
    dumper_class.dump('test.classes')
