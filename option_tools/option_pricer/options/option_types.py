# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 11:18
# @Author  : Xin Zhang
# @File    : option_types.py

from QuantLib import Option as OpType


# OptionType:
CALL = OpType.Call
PUT = OpType.Put

'000000 0000'

class OptionSet:
    @classmethod
    def VANNILLA(cls):
        return cls


# OptionGeneric:
VANNILLA = 0
EXOTIC = 1

'http://repo.optionplus.cn/gs_zhangxin/test_1.git'

# ExerciseType:
EUROPEAN = 0
AMERICAN = 2


class AverageType:
    GEOMETRIC = 8
    ARITHMETIC = 4


class AveragingContinuity:
    DISCRETE = 0
    CONTINUOUS = 16


if __name__ == '__main__':
    s = [VANNILLA | EUROPEAN,
         VANNILLA | AMERICAN,

         EXOTIC | EUROPEAN | AverageType.ARITHMETIC,

         EXOTIC | EUROPEAN | AverageType.GEOMETRIC,

         EXOTIC | EUROPEAN |
         AverageType.ARITHMETIC | AveragingContinuity.CONTINUOUS,

         EXOTIC | EUROPEAN |
         AverageType.GEOMETRIC | AveragingContinuity.CONTINUOUS
         ]

    print(sorted(s))
