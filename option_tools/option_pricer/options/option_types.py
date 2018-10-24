# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 11:18
# @Author  : Xin Zhang
# @File    : option_types.py


from abc import ABCMeta, abstractmethod
from option_tools.utils.tools import cast_string_to_date, GreeksComputer
import QuantLib as Ql
from QuantLib import (SimpleQuote,
                      EuropeanExercise, AmericanExercise,
                      Average, PlainVanillaPayoff)
from .option_code_config import CodeGen


class OptionMetaType(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        if len(bases) > 0:
            attrs['oid'] += bases[0].oid
        return super().__new__(mcs, name, bases, attrs)


class Greeks:
    def __init__(self):
        self.__delta = None
        self.__gamma = None
        self.__rho = None
        self.__theta = None
        self.__vega = None

    @property
    def delta(self):
        return self.__delta

    @property
    def gamma(self):
        return self.__gamma

    @property
    def rho(self):
        return self.__rho

    @property
    def theta(self):
        return self.__theta

    @property
    def vega(self):
        return self.__vega

    @delta.setter
    def delta(self, delta):
        self.__delta = delta

    @gamma.setter
    def gamma(self, gamma):
        self.__gamma = gamma

    @rho.setter
    def rho(self, rho):
        self.__rho = rho

    @theta.setter
    def theta(self, theta):
        self.__theta = theta

    @vega.setter
    def vega(self, vega):
        self.__vega = vega

    def to_dict(self):

        return {
            'delta': self.delta,
            'gamma': self.gamma,
            'rho': self.rho,
            'theta': self.theta,
            'vega': self.vega
        }

    def all_filled(self):
        filled = True
        d = self.to_dict()
        for v in d.values():
            filled = filled and (v is not None)
        return filled

    def __str__(self):
        return str(self.to_dict())

    __repr__ = __str__


class OptionBase(metaclass=OptionMetaType):
    oid = 0  # option id

    def __init__(self, option_type):
        """
        initialize option with a option type[call or put]
        :param option_type: call or put
        """
        # option result
        self.__npv = None
        self.__greeks = Greeks()

        # option attribution
        self.evaluation_date = None
        self.maturity_date = None
        self.spot_price = None
        self.strike_price = None
        self.volatility = None
        self.risk_free_rate = None
        self.dividend_rate = None

        self.option_instance = None
        self.engine_instance = None
        self.option_type = option_type
        self.exercise = None
        self.payoff = None

        self.calendar = Ql.China()
        self.day_counter = Ql.ActualActual()

        self.setup_finished = dict(
            params=False,
            exercise=False,
            payoff=False,
            instance=False,
            engine=False
        )

    def set_params(
            self,
            spot_price,
            strike_price,
            volatility,
            risk_free_rate,
            evaluation_date: str,
            maturity_date: str,
            dividend_rate=0):
        """
        set option parameters
        :param spot_price: float
        :param strike_price: float
        :param volatility: float
        :param risk_free_rate: float
        :param evaluation_date: str, format like 2010-01-01
        :param maturity_date: str, format like 2010-01-01
        :param dividend_rate: float
        """
        self.spot_price = SimpleQuote(spot_price)
        self.strike_price = strike_price
        self.volatility = SimpleQuote(volatility)
        self.risk_free_rate = SimpleQuote(risk_free_rate)
        self.evaluation_date = cast_string_to_date(evaluation_date)
        self.maturity_date = cast_string_to_date(maturity_date)
        self.dividend_rate = SimpleQuote(dividend_rate)
        self.setup_finished['params'] = True
        self.set_exercise()
        self.setup_finished['exercise'] = True
        self.set_payoff()
        self.setup_finished['payoff'] = True
        self.set_option_instance()
        self.setup_finished['instance'] = True

    def set_payoff(self):
        """
        set payoff type, vannilla or others
        """
        self.payoff = PlainVanillaPayoff(self.option_type, self.strike_price)

    def set_engine(self, engine_cls):
        self.engine_instance = engine_cls(self)
        self.setup_finished['engine'] = True

    @abstractmethod
    def set_exercise(self):
        """
        set exercise type, european or american
        """
        raise NotImplementedError

    @abstractmethod
    def set_option_instance(self):
        """
        set option instance
        """
        raise NotImplementedError

    def is_setup_finished(self):
        base = True
        for v in self.setup_finished.values():
            base = base and v
        return base

    def compute(self):
        assert self.is_setup_finished(), 'Option does not fully setup.'
        Ql.Settings.instance().evaluationDate = self.evaluation_date
        self.engine_instance.set_engine()
        self.option_instance.setPricingEngine(self.engine_instance.engine)
        return self.option_instance.NPV()

    @property
    def greeks(self):
        if self.__greeks.all_filled():
            return self.__greeks
        else:
            gc = GreeksComputer(self.option_instance)
            gks = gc.get_greeks(
                self.spot_price,
                self.risk_free_rate,
                self.volatility,
                self.evaluation_date)
            self.__greeks.delta = gks['delta']
            self.__greeks.gamma = gks['gamma']
            self.__greeks.rho = gks['rho']
            self.__greeks.theta = gks['theta']
            self.__greeks.vega = gks['vega']
            return self.__greeks

    @property
    def npv(self):
        self.__npv = self.compute()
        return self.__npv


class AbstractEuropeanOption(OptionBase):
    oid = CodeGen.EUROPEAN

    def set_exercise(self):
        """
        set exercise type, european or american
        """
        self.exercise = EuropeanExercise(self.maturity_date)


class AbstractAmericanOption(OptionBase):
    oid = CodeGen.AMERICAN

    def set_exercise(self):
        """
        set exercise type, european or american
        """
        self.exercise = AmericanExercise(
            self.evaluation_date, self.maturity_date)

# <<<< Vannilla European & American


class EuropeanOption(AbstractEuropeanOption):
    oid = CodeGen.VANNILLA

    def set_option_instance(self):
        self.option_instance = Ql.VanillaOption(self.payoff, self.exercise)


class AmericanOption(AbstractAmericanOption):
    oid = CodeGen.VANNILLA

    def set_option_instance(self):
        self.option_instance = Ql.VanillaOption(self.payoff, self.exercise)

# <<<< Exotic European


class AbstractEuropeanExoticOption(AbstractEuropeanOption):
    oid = CodeGen.EXOTIC

# <<<< Asian European


class AbstractAsianOption(AbstractEuropeanExoticOption):
    oid = CodeGen.ASIAN

    def __init__(self, option_type):
        super().__init__(option_type)
        self.setup_finished['avg_date'] = False
        self.setup_finished['avg_type'] = False
        self.avg_start = None
        self.avg_end = None
        self.avg_freq = None
        self.avg_type = None

    def set_averaging_date(self, avg_start, avg_end, freq=1):
        """
        set asian option average params
        :param avg_start: average start date, string, fmt like 2010-01-01
        :param avg_end:  average end date, string, fmt like 2010-01-01
        :param freq: average frequency, unit: days
        """
        self.avg_start = cast_string_to_date(avg_start)
        self.avg_end = cast_string_to_date(avg_end)
        self.avg_freq = freq
        self.setup_finished['avg_date'] = True

    @abstractmethod
    def set_averaging_type(self):
        """
        set average type for asian option
        """
        raise NotImplementedError


# <<<< BARRIER European
class BarrierOption(AbstractEuropeanExoticOption):
    oid = CodeGen.BARRIER


# <<<< Asian options
class AbstractDiscreteAsianOption(AbstractAsianOption):
    oid = CodeGen.DISCRETE

# <<< pricing


class ArithmeticDiscreteAsianOption(AbstractDiscreteAsianOption):
    oid = CodeGen.ARITHMETIC

    def __init__(self, option_type, past_fixes=0, cum_sum=0):
        super().__init__(option_type)
        self.past_fixes = past_fixes
        self.cum_sum = cum_sum

    def set_averaging_type(self):
        self.avg_type = Average.Arithmetic
        self.setup_finished['avg_type'] = True

    def set_averaging_date(self, avg_start, avg_end, freq=1):
        """
        set asian option average params
        :param avg_start: average start date, string, fmt like 2010-01-01
        :param avg_end:  average end date, string, fmt like 2010-01-01
        :param freq: average frequency, unit: days
        """
        super().set_averaging_date(avg_start, avg_end, freq)
        self.set_averaging_type()

    def set_option_instance(self):
        fixing_dates = [self.avg_end -
                        i *
                        7 for i in range(self.day_counter.dayCount(self.avg_start, self.avg_end) //
                                         self.avg_freq +
                                         1) if self.avg_end -
                        i *
                        7 >= self.avg_start][::-
                                             1]

        self.option_instance = Ql.DiscreteAveragingAsianOption(
            self.avg_type,
            self.cum_sum,
            self.past_fixes,
            Ql.DateVector(fixing_dates),
            self.payoff,
            self.exercise)


# << Not Implemented
class AbstractContinuousAsianOption(AbstractAsianOption):
    oid = CodeGen.CONTINUOUS
