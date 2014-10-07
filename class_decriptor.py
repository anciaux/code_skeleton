
class Method:
    def __init__(self,name,args,ret,encapsulation):
        self.name = name
        self.args = dict()
        for k,v in args:
            self.args[k] = v
        self.ret = ret
        self.encapsulation = encapsulation
        
class Member:
    def __init__(self,name,type,encpsulation):
        self.name = name
        self.type = type
        self.encapsulation = encapsulation

class ClassDescriptor:


    def __init__(self,name):
        self.name = name 
        self.members = []
        self.methods = []

    
    def addMethod(self,name,args,ret,encapsulation):
        self.methods.append(Method(name,args,ret,encapsulation))

    def addMember(self,name,type,encapsulation):
        self.members.append(Member(name,type,encapsulation))

    def __str__(self):
        return "Class " + self.name + "\nMethods: " + str(self.methods) + "\nMembers:" + str(self.members)        

        
if __name__ == '__main__':
    my_class = ClassDescriptor('dummy')
    print my_class
    my_class.addMethod('compute',[('int','arg1'),('double','arg2')],'bool','public')
    print my_class
