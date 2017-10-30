#!/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import unittest

try:
    from code_skeleton.class_reader import ClassReader
except:
    pass


class classesParserTest(unittest.TestCase):
    "Unit tests for Classes parser"

    def setUp(self, ):
        pass

    def test_single_class(self):

        dumper_class = ClassReader()
        animal_class = """
class Animal
  public pure virtual void scream();
  public std::string getName();
  public std::string setName(const std::string & name);
  protected std::string name;
"""
        classes = dumper_class.read_from_buffer(animal_class)
        for c in classes:
            for encaps, memb in c.members.items():
                print(encaps, memb)
        print(classes)
        raise RuntimeError('test to be written')
