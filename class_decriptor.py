
class Method:
    def __init__(self,name,args,ret,encapsulation,virtual):
        self.name = name
        self.virtual = virtual
        self.args = dict()
        for k,v in args:
            self.args[v] = k
        self.ret = ret
        self.encapsulation = encapsulation
        if self.encapsulation == '':
            self.encapsulation = 'public'

    def __str__(self):
        sstr = self.encapsulation + " "
        if not self.virtual == '': sstr += self.virtual + " "

        sstr += self.ret + " " + self.name + "("
        pairs = list(self.args.iteritems())
        for k,_type in pairs[:-1]:
            sstr += _type + " " + k + ", "
        sstr += _type + " " + k + ")"
        return sstr
class Member:
    def __init__(self,name,_type,encapsulation):
        self.name = name
        self.type = _type
        self.encapsulation = encapsulation

    def __str__(self):
        return self.encapsulation + " " + self.type + " " + self.name

class ClassDescriptor:


    def __init__(self,name):
        self.name = name 
        self.members = []
        self.methods = []

    
    def addMethod(self,name,args,ret,encapsulation,virtual):
        self.methods.append(Method(name,args,ret,encapsulation,virtual))

    def addMember(self,name,_type,encapsulation):
        self.members.append(Member(name,_type,encapsulation))

    def __str__(self):
        sstr = "Class " + self.name + "\n"
        sstr += "Methods:\n"
        for m in self.methods:
            sstr += str(m) + "\n"
        sstr += "\n"
        sstr += "Members:\n"
        for m in self.members:
            sstr += str(m) + "\n"       
        return sstr
        
if __name__ == '__main__':
    my_class = ClassDescriptor('dummy')
    my_class.addMethod('compute',[('int','arg1'),('double','arg2')],'bool','public')
    my_class.addMember('res','double','private')
    print my_class
