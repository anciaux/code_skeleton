from class_reader import ClassReader

class ClassDumper:
    
    def __init__(self):
        pass

    def dump(self,class_file):
        cls_reader = ClassReader()
        classes = cls_reader.read(class_file)
        sstr = ""
        for c in classes:
            sstr += self.dumpFile(c)

        return sstr

        raise Exception('pure virtual function')
        
    def dumpFile(self,c):
        raise Exception('pure virtual function')
