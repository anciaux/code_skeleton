from class_dumper import ClassDumper

class ClassDumperCPP(ClassDumper):
    def __init__(self):
        ClassDumper.__init__(self)


    def dumpFile(self,c):
        sstr = "class " + c.name + "{\n"

        sstr += self.formatConstructor(c)
        sstr += self.formatMethods(c)
        sstr += self.formatMembers(c)
        
        sstr += "};\n" 
        print sstr

    def formatConstructor(self,c):
        sstr = ""

        for encaps in ['public','private', 'protected']:
            
            meths = c.getMethods(encaps)
            if c.name in meths:
                sstr += encaps + ':'
                sstr += str(meths[name])
        

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
                sstr += encaps + ':\n\n'

            for n in meths_names:
                for m in meths[n]:
                    sstr += str(m) + "\n"
            sstr += "\n"

        if not sstr == "":
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
                sstr += encaps + ':\n\n'

            for n,m in membs.iteritems():
                sstr += str(m) + "\n"
            sstr += "\n"

        if not sstr == "":
            sstr = """
  /* ------------------------------------------------------------------------ */
  /* Members                                                                  */
  /* ------------------------------------------------------------------------ */

""" + sstr

        return sstr



if __name__ == '__main__':
    dumper_class = ClassDumperCPP()
    print dumper_class.dump('test.classes')
