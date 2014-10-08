import re
from class_decriptor import ClassDescriptor

class ClassReader:

    def __init__(self):
        self.classes = []
        self.current_class = None

    def read(self,filename):
        f = open(filename,'r')
        for line in f:
            self.readline(line)

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
        
        
    def isNewClassTag(self,line):
        m = re.match(r'class (.*)',line)
        if m: 
            name = m.group(1)
            if self.current_class is not None:
                self.classes.append(self.current_class)
            self.current_class = ClassDescriptor(name)
            return True
        return False

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
        m = re.match(r'((?:public|protected|private)*)\s+((?:virtual|pure virtual)*)\s+(\S*)\s+(\S*)\((.*)\)',line)
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
