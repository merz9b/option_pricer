#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 22:44
# @Author  : John
# @File    : example_of_metaclass.py


class MyType2(type):
    def __new__(cls, name, bases, attrs):
        if len(bases) > 0:
            attrs['f'] += bases[0].f
        return super().__new__(cls, name, bases, attrs)


class Foo(metaclass=MyType2):
    f = 3


class Bar(Foo):
    f = 4





class OptionType:
    def __init__(self, base_type = 0):
        self.type_code = base_type

    @property
    def VANNILLA(self):
        return self.__class__(self.type_code | 0)

    @property
    def EXOTIC(self):
        return self.__class__(self.type_code | 1)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)

    @property
    def ASIAN(self):
        return self.__class__(self.type_code | 2)


    def build(self):
        return self.type_code





OptionType().EXOTIC.build()