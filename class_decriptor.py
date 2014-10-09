
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


    def __init__(self,name,inheritance=None):
        self.name = name 
        self.inheritance = inheritance 
        self.members = {'private':{},'public':{},'protected':{}}
        self.methods = {'private':{},'public':{},'protected':{}}

    def addMethod(self,name,args,ret,encapsulation,virtual):
        new_method = Method(name,args,ret,encapsulation,virtual)
        if name not in self.methods[encapsulation]: self.methods[encapsulation][name] = []
        self.methods[encapsulation][name].append(new_method)

    def addMember(self,name,_type,encapsulation):
        new_member = Member(name,_type,encapsulation)
        self.members[encapsulation][name] = new_member

    def getMembers(self,encapsulation=None):
        return self.members[encapsulation]

    def getMethods(self,encapsulation=None):
        return self.methods[encapsulation]

    def __str__(self):
        sstr = "Class " + self.name + "\n"
        if (self.inheritance):
            sstr += "Inherit: "
            tmp = ""
            for mother in self.inheritance:
                tmp += mother + ","
            sstr += tmp[:-1] + "\n"
            
        sstr += "Methods:\n"
        for encaps,meths in self.methods.iteritems():
            sstr += encaps + ":\n"
            for name,m_list in meths.iteritems():
                for m in m_list:
                    sstr += str(m) + "\n"
        sstr += "\n"
        sstr += "Members:\n"
        for encaps,membs in self.members.iteritems():
            sstr += encaps + ":\n"
            for name,m in membs.iteritems():
                sstr += str(m) + "\n"       
        return sstr
        
if __name__ == '__main__':
    my_class = ClassDescriptor('dummy')
    my_class.addMethod('compute',[('int','arg1'),('double','arg2')],'bool','public','')
    my_class.addMember('res','double','private')
    print my_class
