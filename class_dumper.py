from class_reader import ClassReader

class ClassDumper:
    
    def __init__(self):
        self.base_types = ['int','double', 'float', 'unsigned int']
        self.base_types = self.base_types + [e + ' *' for e in self.base_types] + [e + ' &' for e in self.base_types]

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

    def baseType(self,_type):
        temp_type = _type.replace('&','')
        temp_type = temp_type.strip()
        return temp_type
