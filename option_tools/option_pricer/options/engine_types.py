# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:16
# @Author  : Xin Zhang
# @File    : engine_types.py

from .option_types import (OptionType, ExerciseType,
                           AveragingContinuity, AsianAverageType)

# MC OR ANALYTIC OR FD APPROXIMATION
MC_INCLUDE = (
    OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,
    OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,
)

FD_INCLUDE = (
    OptionType.CALL | ExerciseType.AMERICAN,
    OptionType.PUT | ExerciseType.AMERICAN,
    OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC | AveragingContinuity.DISCRETE,
    OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC | AveragingContinuity.DISCRETE,
)

ANALYTIC_INCLUDE = (
    OptionType.CALL | ExerciseType.EUROPEAN,
    OptionType.PUT | ExerciseType.EUROPEAN,
)


class Int:
    __slots__ = ['attr', 'value']

    def __init__(self, value, attr):
        self.attr = attr
        self.value = value

    def __or__(self, other):
        global MC_INCLUDE, FD_INCLUDE, ANALYTIC_INCLUDE
        if self.attr == 'analytic':
            assert other in ANALYTIC_INCLUDE, 'No analytic engine for this option.'
            return self.value | other
        elif self.attr == 'mc':
            assert other in MC_INCLUDE, 'No mc engine for this option.'
            return self.value | other
        elif self.attr == 'fd':
            assert other in FD_INCLUDE, 'No fd engine for this option.'
            return self.value | other
        else:
            raise TypeError('Invalid engine type.')

    __ror__ = __or__

    def __str__(self):
        return '<{tp}> : {d}'.format(tp=self.attr.upper(), d=self.value)

    __repr__ = __str__


class EngineType:
    ANALYTIC = Int(0, 'analytic')
    MC = Int(32, 'mc')
    FD = Int(64, 'fd')
