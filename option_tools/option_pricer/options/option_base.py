# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:54
# @Author  : Xin Zhang
# @File    : option_base.py

from option_tools.utils.tools import cast_string_to_date
from QuantLib import (SimpleQuote, China, ActualActual,
                      EuropeanExercise, AmericanExercise,
                      Average, PlainVanillaPayoff)
from .option_types import CodeGen, OptionMetaType


class Greeks:
    def __init__(self):
        self._delta = None
        self._gamma = None
        self._rho = None
        self._theta = None
        self._vega = None

    @property
    def delta(self):
        return self._delta

    @property
    def gamma(self):
        return self._gamma

    @property
    def rho(self):
        return self._rho

    @property
    def theta(self):
        return self._theta

    @property
    def vega(self):
        return self._vega

    @delta.setter
    def delta(self, delta):
        self._delta = delta

    @gamma.setter
    def gamma(self, gamma):
        self._gamma = gamma

    @rho.setter
    def rho(self, rho):
        self._rho = rho

    @theta.setter
    def theta(self, theta):
        self._theta = theta

    @vega.setter
    def vega(self, vega):
        self._vega = vega

    def to_dict(self):

        return {
            'delta': self.delta,
            'gamma': self.gamma,
            'rho': self.rho,
            'theta': self.theta,
            'vega': self.vega
        }

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
        self.evaluation_date = None
        self.maturity_date = None
        self.spot_price = None
        self.strike_price = None
        self.volatility = None
        self.risk_free_rate = None
        self.dividend_rate = None
        self.npv = None

        self.option_type = option_type
        self.exercise = None
        self.payoff = None

        self.greeks = Greeks()

        self.calendar = China()
        self.day_counter = ActualActual()

        self.__setup_finished = dict(
            params=False,
            exercise=False,
            payoff=False
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
        self.__setup_finished['params'] = True
        self.set_exercise()
        self.__setup_finished['exercise'] = True
        self.set_payoff()
        self.__setup_finished['payoff'] = True

    def set_exercise(self):
        """
        set exercise type, european or american
        """
        raise NotImplementedError

    def set_payoff(self):
        """
        set payoff type, vannilla or others
        """
        self.payoff = PlainVanillaPayoff(self.option_type, self.strike_price)

    def is_setup_finished(self):
        base = True
        for v in self.__setup_finished.values():
            base = base and v
        return base


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


class AmericanOption(AbstractAmericanOption):
    oid = CodeGen.VANNILLA

# <<<< Exotic European


class AbstractEuropeanExoticOption(AbstractEuropeanOption):
    oid = CodeGen.EXOTIC

# <<<< Asian European


class AbstractAsianOption(AbstractEuropeanExoticOption):
    oid = CodeGen.ASIAN

    def __init__(self, option_type):
        super().__init__(option_type)
        self.__setup_finished['avg_date'] = False
        self.__setup_finished['avg_type'] = False
        self.avg_start = None
        self.avg_end = None
        self.avg_type = None

    def set_averaging_date(self, avg_start, avg_end):
        """
        set asian option average params
        :param avg_start: average start date, string, fmt like 2010-01-01
        :param avg_end:  average end date, string, fmt like 2010-01-01
        """
        self.avg_start = cast_string_to_date(avg_start)
        self.avg_end = cast_string_to_date(avg_end)
        self.__setup_finished['avg_date'] = True

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

    def set_averaging_type(self):
        self.avg_type = Average.Arithmetic
        self.__setup_finished['avg_type'] = False

    def set_averaging_date(self, avg_start, avg_end):
        """
        set asian option average params
        :param avg_start: average start date, string, fmt like 2010-01-01
        :param avg_end:  average end date, string, fmt like 2010-01-01
        """
        super().set_averaging_date(avg_start, avg_end)
        self.set_averaging_type()


# << Not Implemented
class AbstractContinuousAsianOption(AbstractAsianOption):
    oid = CodeGen.CONTINUOUS
