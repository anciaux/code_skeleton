import re
from class_decriptor import ClassDescriptor

class ClassReader:

    def __init__(self):
        self.classes = []
        self.current_class = None

    def read(self,filename):
        f = open(filename,'r')
        self.line_cpt = 0
        for line in f:
            self.readline(line)
            self.line_cpt += 1

        if self.current_class is not None:
            self.classes.append(self.current_class)
        
        return self.classes


    def readline(self,line):
        line = line.split('#')[0]
        line = line.strip()
        if line == "": return
        if self.isNewClassTag(line): return
        if self.isNewMethodTag(line): return
        if self.isNewMemberTag(line): return
        else: raise Exception("could not parse line:{0}\n'".format(self.line_cpt) + line + "'")
        
        
    def isNewClassTag(self,line):
        ret = False
        m = re.match(r'class\s+(\S*)',line)
        if m:
            name        = m.group(1)
            inheritance = None           
            ret = True

        m = re.match(r'class\s+(\S*)\((.*)\)',line)
        if m: 
            name        = m.group(1)
            inheritance = m.group(2)
            inheritance = inheritance.strip().split(',')
            inheritance = [e.strip() for e in inheritance] 
            ret = True
            
        if ret == False: return False
        
        if self.current_class is not None:
                self.classes.append(self.current_class)
                
        self.current_class = ClassDescriptor(name,inheritance)
        
        return True

    def isNewMemberTag(self,line):
        m = re.match(r'((?:public|protected|private)*)\s+((?:\S|(?:\s+\*))+)\s+(.*)',line)
        if m: 
            encapsulation = m.group(1)
            _type         = m.group(2)
            name          = m.group(3)
            self.current_class.addMember(name,_type,encapsulation)
            return True
        return False

    def isNewMethodTag(self,line):
        m = re.match(r'((?:public|protected|private)*)\s*((?:virtual|pure virtual)?)\s*(\S*)\s+(\S*)\((.*)\)',line)
        if m: 
            encapsulation = m.group(1).strip()
            virtual       = m.group(2).strip()
            ret           = m.group(3).strip()
            name          = m.group(4).strip()
            args          = m.group(5).strip().split(',')
            args = [tuple(e.strip().split(' ')) for e in args]
            self.current_class.addMethod(name,args,ret,encapsulation,virtual)            
            return True
        return False

            

if __name__ == '__main__':
    cls_reader = ClassReader()
    classes = cls_reader.read('test.classes')
    for c in classes:
        print c
