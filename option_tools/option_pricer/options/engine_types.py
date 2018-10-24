# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:16
# @Author  : Xin Zhang
# @File    : engine_types.py

from .option_base import (
    EuropeanOption,
    AmericanOption,
    ArithmeticDiscreteAsianOption)

# MC OR ANALYTIC OR FD APPROXIMATION
MC_INCLUDE = (
    ArithmeticDiscreteAsianOption.oid,
)

FD_INCLUDE = (
    AmericanOption.oid,
    ArithmeticDiscreteAsianOption.oid
)

ANALYTIC_INCLUDE = (
    EuropeanOption.oid,
)


class Int:
    __slots__ = ['attr', 'value']

    def __init__(self, value, attr):
        self.attr = attr
        self.value = value

    def __add__(self, other):
        global MC_INCLUDE, FD_INCLUDE, ANALYTIC_INCLUDE
        if self.attr == 'analytic':
            assert other in ANALYTIC_INCLUDE, 'No analytic engine for this option.'
            return self.value + other
        elif self.attr == 'mc':
            assert other in MC_INCLUDE, 'No mc engine for this option.'
            return self.value + other
        elif self.attr == 'fd':
            assert other in FD_INCLUDE, 'No fd engine for this option.'
            return self.value + other
        else:
            raise TypeError('Invalid engine type.')

    __radd__ = __add__

    def __str__(self):
        return '<{tp}> : {d}'.format(tp=self.attr.upper(), d=self.value)

    __repr__ = __str__


class EngineType:
    ANALYTIC = Int(1000000000, 'analytic')
    MC = Int(2000000000, 'mc')
    FD = Int(3000000000, 'fd')
