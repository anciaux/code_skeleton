from class_reader import ClassReader

class ClassDumper:
    
    def __init__(self):
        pass

    def dump(self,filename):
        cls_reader = ClassReader()
        classes = cls_reader.read(filename)
        for c in classes:
            self.dumpFile(c)

    def dumpFile(self,c):
        raise Exception('pure virtual function')
