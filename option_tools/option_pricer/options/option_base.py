# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:54
# @Author  : Xin Zhang
# @File    : option_base.py

from option_tools.utils.tools import cast_string_to_date
from QuantLib import SimpleQuote
from .option_types import ExerciseType, OptionType


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

    def set_exercise(self, exercise_type):
        """
        set exercise type, european or american
        :param exercise_type: ExerciseType
        """
        self.oid |= exercise_type

    def set_type(self, option_type):
        """
        set option type, call or put
        :param option_type: OptionType
        """
        self.oid |= option_type


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
