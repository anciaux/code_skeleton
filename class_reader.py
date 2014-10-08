import re
from class_decriptor import ClassDescriptor

class ClassReader:
    
    def read(self,filename):
        f = open(filename,'r')
        for line in f:
            self.readline(line)

    def readline(self,line):
        line = line.split('#')[0]
        line = line.strip()
        if line == "": return
        m = re.match(r'class (.*)',line)
        print line
        if m: 
            print line
            print m.group(1)
            
        


if __name__ == '__main__':
    cls_reader = ClassReader()
    classes = cls_reader.read('test.classes')
    print classes
