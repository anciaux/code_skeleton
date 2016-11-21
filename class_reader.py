#!/usr/bin/python
# -*- coding: utf-8 -*-

" Module used to read .classes files "
################################################################
import re
from class_decriptor import ClassDescriptor
################################################################


class ClassReader(object):

    " Reader for classes objects "

    def __init__(self):
        self.classes = []
        self.current_class = None
        self.filename = None
        self.line_cpt = 0

    def read(self, filename):

        " read the provided .classes file "

        self.filename = filename
        _file = open(self.filename, 'r')
        self.line_cpt = 0
        for line in _file:
            self.readline(line)
            self.line_cpt += 1

        if self.current_class is not None:
            self.classes.append(self.current_class)

        return self.classes

    def readline(self, line):

        " read a single line "

        line = line.split('#')[0]
        line = line.strip()
        if line == "":
            return
        try:
            if self._is_new_class_tag(line):
                return
            if self._is_new_method_tag(line):
                return
            if self._is_new_typedef(line):
                return
            if self._is_new_member_tag(line):
                return
            else:
                raise Exception('Unknown tag')
        except Exception as ex:
            raise Exception(self.filename + ":{0}".format(self.line_cpt+1)
                            + ":'" + line + "' : " + str(ex))

    def _is_new_class_tag(self, line):

        ret = False
        match = re.match(r'class\s+(\S*)', line)
        if match:
            name = match.group(1)
            inheritance = None
            ret = True

        match = re.match(r'class\s+(\S*)\((.*)\)', line)
        if match:
            name = match.group(1).strip()
            inheritance = match.group(2).strip()
            inheritance = inheritance.strip().split(',')
            inheritance = [e.strip() for e in inheritance]
            ret = True

        if ret is False:
            return False

        if self.current_class is not None:
            self.classes.append(self.current_class)

        self.current_class = ClassDescriptor(name, inheritance)

        return True

    def _is_new_member_tag(self, line):
        if not line.find("(") == -1:
            return False
        if not line.find(")") == -1:
            return False
        match = re.match((r'((?:public|protected|private)*)\s*((?:static)?)\s*'
                          r'((?:\S|(?:\s+\*)|(?:\s+\&))+)\s+(\S*)[\s|;]*(?://)*(.*)'), line)
        if match:
            encapsulation = match.group(1).strip()
            static = match.group(2).strip()
            _type = match.group(3).strip()
            name = match.group(4).strip()
            comments = match.group(5).strip()
            name = name.replace(';', '')
            self.current_class.add_member(name, _type, encapsulation,
                                          static, comments)
            return True
        return False

    def _is_new_typedef(self, line):

        if not line.find("(") == -1:
            return False
        if not line.find(")") == -1:
            return False
        match = re.match(
            r'((?:public|protected|private)*)\s*typedef\s*(\S+)', line)
        if match:
            encapsulation = match.group(1).strip()
            name = match.group(2).strip()
            name = name.replace(';', '')
            self.current_class.add_type(name, encapsulation)
            return True
        return False

    def _is_new_method_tag(self, line):

        match = re.match((r'((?:public|protected|private)*)\s*((?:static)?)\s*'
                          r'((?:virtual|pure virtual)?)\s*(.*)\s+([\S|~]*)\((.*)\)\s*'
                          r'((?:const)?)[\s|;]*(?://)*(.*)'), line)
        if match:
            encapsulation = match.group(1).strip()
            static = match.group(2).strip()
            virtual = match.group(3).strip()
            ret = match.group(4).strip()
            name = match.group(5).strip()
            args = match.group(6).strip().split(',')
            const = match.group(7).strip()
            comments = match.group(8).strip()
            args = [list(e.strip().split(' ')) for e in args]
            temp_args = []
            for arg in args:
                if len(arg) >= 2:
                    temp_args.append(tuple([" ".join(arg[:-1]), arg[-1]]))
            args = temp_args
            args = [e for e in args if not e[0] == '']
            self.current_class.add_method(name, args, ret,
                                          encapsulation, virtual,
                                          static, const, comments)
            return True
        return False

################################################################

def main():
    cls_reader = ClassReader()
    classes = cls_reader.read('test.classes')
    for _class in classes:
        print _class

if __name__ == '__main__':
    main()
