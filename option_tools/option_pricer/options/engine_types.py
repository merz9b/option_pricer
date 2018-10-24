# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:16
# @Author  : Xin Zhang
# @File    : engine_types.py

import random
from abc import ABCMeta, abstractmethod
from .engine_include_config import FD_INCLUDE, MC_INCLUDE, ANALYTIC_INCLUDE
from QuantLib import (BlackScholesMertonProcess, QuoteHandle,
                      BlackConstantVol, FlatForward, YieldTermStructureHandle,
                      BlackVolTermStructureHandle, AnalyticEuropeanEngine,
                      MCDiscreteArithmeticAPEngine, FdBlackScholesAsianEngine,
                      FDAmericanEngine)


def ensure_pairable(option_instance, engine_instance):
    """
    ensure option and engine pairable
    :param option_instance: option instance
    :param engine_instance: engine instance
    """
    _ = engine_instance.eid + option_instance.oid


# engine attribution class


class Int:
    __slots__ = ['attr', 'value']

    def __init__(self, value, attr):
        self.attr = attr
        self.value = value

    def __add__(self, other):

        if isinstance(other, self.__class__):
            if other.attr == 'abstract':
                return self.__class__(other.value + self.value, self.attr)
            else:
                return self.__class__(other.value + self.value, other.attr)

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


# engine type class
class EngineType:
    ANALYTIC = Int(1000000000, 'analytic')
    MC = Int(2000000000, 'mc')
    FD = Int(3000000000, 'fd')
    ABSTRACT = Int(0, 'abstract')


class EngineMetaType(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        if len(bases) > 0:
            attrs['eid'] += bases[0].eid
        return super().__new__(mcs, name, bases, attrs)


class PricingEngineBase(metaclass=EngineMetaType):
    eid = EngineType.ABSTRACT

    def __init__(self, option):
        self.engine = None
        self.process = None
        ensure_pairable(option, self)
        self.option = option

    @abstractmethod
    def set_process(self):
        raise NotImplementedError

    @abstractmethod
    def set_engine(self):
        raise NotImplementedError


class AbstractBsmEngine(PricingEngineBase):
    eid = EngineType.ABSTRACT

    def set_process(self):
        risk_free_curve = FlatForward(
            self.option.evaluation_date,
            QuoteHandle(self.option.risk_free_rate),
            self.option.day_counter)

        volatility_curve = BlackConstantVol(
            self.option.evaluation_date,
            self.option.calendar,
            QuoteHandle(self.option.volatility),
            self.option.day_counter)

        dividend_curve = FlatForward(
            self.option.evaluation_date,
            QuoteHandle(self.option.dividend_rate),
            self.option.day_counter)

        self.process = BlackScholesMertonProcess(
            QuoteHandle(self.option.spot_price),
            YieldTermStructureHandle(dividend_curve),
            YieldTermStructureHandle(risk_free_curve),
            BlackVolTermStructureHandle(volatility_curve)
        )


class AbstractAnalyticBsmEngine(AbstractBsmEngine):
    eid = EngineType.ABSTRACT

# >>>> AnalyticBsmEuropeanEngine


class AnalyticBsmEuropeanEngine(AbstractAnalyticBsmEngine):
    eid = EngineType.ANALYTIC

    def set_engine(self):
        self.set_process()
        self.engine = AnalyticEuropeanEngine(self.process)


class AbstractMcBsmEngine(AbstractBsmEngine):
    eid = EngineType.ABSTRACT

# >>>> McBsmDiscreteArithmeticAsianEngine


class McBsmDiscreteArithmeticAsianEngine(AbstractMcBsmEngine):
    eid = EngineType.MC

    def __init__(self, option, n_required=100000):
        super().__init__(option)
        self.n_required = n_required

    def set_engine(self):
        self.set_process()
        mc_str = 'PseudoRandom'
        is_bb = True
        is_av = True
        is_cv = True
        n_require = self.n_required
        tolerance = float(self.option.strike_price / 10000.0)
        n_max = int(n_require * 2)
        seed = random.randint(1, 1000)

        self.engine = MCDiscreteArithmeticAPEngine(
            self.process,
            mc_str,
            is_bb,
            is_av,
            is_cv,
            n_require,
            tolerance,
            n_max,
            seed)


class AbstractFdBsmEngine(AbstractBsmEngine):
    eid = EngineType.ABSTRACT

# >>>> FdBsmDiscreteArithmeticAsianEngine


class FdBsmDiscreteArithmeticAsianEngine(AbstractFdBsmEngine):
    eid = EngineType.FD

    def set_engine(self):
        self.set_process()

        duration_days = self.option.day_counter.dayCount(
            self.option.evaluation_date, self.option.maturity_date)
        self.engine = FdBlackScholesAsianEngine(
            self.process, duration_days, 400, 200)

# >>>> FdBsmAmericanEngine


class FdBsmAmericanEngine(AbstractFdBsmEngine):
    eid = EngineType.FD

    def set_engine(self):
        self.set_process()

        self.engine = FDAmericanEngine(self.process)


if __name__ == '__main__':

    s1 = Int(0, 'abstract')
    s2 = Int(0, 'abstract')
    s3 = Int(2000000000, 'mc')

    s4 = s1 + s3

    s4 + s1
