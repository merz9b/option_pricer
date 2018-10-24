# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:43
# @Author  : Xin Zhang
# @File    : test_script_4.py

# --------------------------------------------------------------------------
import QuantLib as Ql
from option_tools.utils.tools import get_signature_code
from option_tools.option_pricer.options.option_base import EuropeanOption, AmericanOption, ArithmeticDiscreteAsianOption
from option_tools.option_pricer.options.engine_types import EngineType

print(EngineType.ANALYTIC + EuropeanOption.oid)
# print(EngineType.MC + EuropeanOption.oid)
print(EngineType.FD + AmericanOption.oid)


print(ArithmeticDiscreteAsianOption.oid)
print(get_signature_code(ArithmeticDiscreteAsianOption.oid, 1))
print(get_signature_code(ArithmeticDiscreteAsianOption.oid, 5))


"""
European call option
evaluation date : 2018-03-07
maturity date : 2018-07-07
spot price : 100
strike price : 100
volatility : 0.2
risk_free_rate : 0.01
dividend rate : 0

price : 4.77139
"""
spot_price = 100
strike_price = 100
evaluation_date = '2018-03-07'
maturity_date = '2018-07-07'
vol = 0.2
rf = 0.01

option = EuropeanOption(Ql.Option.Call)

option.set_params(spot_price,
                  strike_price,
                  vol,
                  rf,
                  evaluation_date,
                  maturity_date)


if option.is_setup_finished():
    pass

Ql.Settings.instance().evaluationDate = option.evaluation_date
# set calendar and day counter
calendar = Ql.China()
day_counter = Ql.ActualActual()

risk_free_curve = Ql.FlatForward(
    option.evaluation_date,
    Ql.QuoteHandle(option.risk_free_rate),
    day_counter)

volatility_curve = Ql.BlackConstantVol(
    option.evaluation_date,
    calendar,
    Ql.QuoteHandle(option.volatility),
    day_counter)

dividend_curve = Ql.FlatForward(
    option.evaluation_date,
    Ql.QuoteHandle(option.dividend_rate),
    day_counter)

process = Ql.BlackScholesMertonProcess(
    Ql.QuoteHandle(option.spot_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(risk_free_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve)
)

option.option_instance.setPricingEngine(Ql.AnalyticEuropeanEngine(process))

print(option.option_instance.NPV())  # 4.77139


class PricingEngine:
    def __init__(self):
        self.engine = 0

    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, option):
        xid = option.oid | self.engine
        return option
