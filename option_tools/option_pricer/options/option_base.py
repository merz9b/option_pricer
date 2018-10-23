# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:54
# @Author  : Xin Zhang
# @File    : option_base.py

from option_tools.utils.tools import cast_string_to_date
from QuantLib import SimpleQuote, China, ActualActual
from .option_types import ExerciseType, OptionType


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


class OptionBase:
    def __init__(self):
        self.oid = 0  # option id
        self.evaluation_date = None
        self.maturity_date = None
        self.spot_price = None
        self.strike_price = None
        self.volatility = None
        self.risk_free_rate = None
        self.dividend_rate = None
        self.npv = None
        self.greeks = Greeks()

        self.calendar = China()
        self.day_counter = ActualActual()

        self.__setup_finished = dict(
            params=False,
            exercise=False,
            otype=False
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

    def set_exercise(self, exercise_type):
        """
        set exercise type, european or american
        :param exercise_type: ExerciseType
        """
        self.oid |= exercise_type
        self.__setup_finished['exercise'] = True

    def set_type(self, option_type):
        """
        set option type, call or put
        :param option_type: OptionType
        """
        self.oid |= option_type
        self.__setup_finished['otype'] = True

    def is_setup_finished(self):
        base = True
        for v in self.__setup_finished.values():
            base = base and v
        return base


class VannillaOption(OptionBase):
    pass


class EuropeanOption(VannillaOption):
    def __init__(self):
        super().__init__()
        self.set_exercise(ExerciseType.EUROPEAN)


class AmericanOption(VannillaOption):
    def __init__(self):
        super().__init__()
        self.set_exercise(ExerciseType.AMERICAN)


class AsianOption(OptionBase):
    def __init__(self):
        super().__init__()
        self.avg_start = None
        self.avg_end = None
        self.set_exercise(ExerciseType.EUROPEAN)

    def set_average_params(self, avg_start, avg_end, avg_type, avg_continuity):
        """
        set asian option average params
        :param avg_start: average start date
        :param avg_end:  average end date
        :param avg_type: AsianAverageType:[Geometric, Arithmetic]
        :param avg_continuity: AveragingContinuity:[Continuous, Discrete]
        """
        self.avg_start = avg_start
        self.avg_end = avg_end
        self.oid = self.oid | avg_type | avg_continuity
