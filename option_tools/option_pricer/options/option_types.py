# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 11:18
# @Author  : Xin Zhang
# @File    : option_types.py


"""

option type coding

0000 | 00000 |  0

> 0 ~ 1

Vannilla or Exotic


> 2 ~ 32 dual number

2 : Asian
4 : Barrier
6 : ....




"""

from QuantLib import Option as OpType


class OptionMetaType(type):
    def __new__(cls, name, bases, attrs):
        if len(bases) > 0:
            attrs['oid'] += bases[0].oid
        return super().__new__(cls, name, bases, attrs)


# OptionType:
CALL = OpType.Call
PUT = OpType.Put



class CodeGen:
    # 1
    VANNILLA = 0
    EXOTIC = 1

    # 2
    EUROPEAN = 10
    AMERICAN = 20

    # 3
    ASIAN = 100
    BARRIER = 200

    # 4
    GEOMETRIC = 1000
    ARITHMETIC = 2000

    # 5
    DISCRETE = 10000
    CONTINUOUS = 20000




if __name__ == '__main__':
    pass
