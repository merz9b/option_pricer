# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 10:30
# @Author  : Xin Zhang
# @File    : test_script_euro.py

import QuantLib as Ql
from QuantLib import Date, EuropeanOption, SimpleQuote, QuoteHandle
from option_tools.utils.tools import GreeksComputer

start_date = Date(7, 3, 2018)
end_date = Date(7, 7, 2018)

Ql.Settings.instance().evaluationDate = start_date

# set calendar and day counter
calendar = Ql.China()
day_counter = Ql.ActualActual()

payoff = Ql.PlainVanillaPayoff(Ql.Option.Call, 100)

euro_option = EuropeanOption(payoff, Ql.EuropeanExercise(end_date))

underlying_price = SimpleQuote(100)
interest_rate = SimpleQuote(0.01)
volatility = SimpleQuote(0.2)
dividend = SimpleQuote(0)

risk_free_curve = Ql.FlatForward(
    0,
    Ql.TARGET(),
    QuoteHandle(interest_rate),
    day_counter)
volatility_curve = Ql.BlackConstantVol(
    0, Ql.TARGET(), QuoteHandle(volatility), day_counter)
dividend_curve = Ql.FlatForward(
    0,
    Ql.TARGET(),
    QuoteHandle(dividend),
    day_counter)

process = Ql.BlackScholesMertonProcess(
    QuoteHandle(underlying_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(risk_free_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve)
)

euro_option.setPricingEngine(Ql.AnalyticEuropeanEngine(process))

print(euro_option.NPV())

# theoretical method
gc = GreeksComputer(euro_option)
gc.get_greeks()

# implement numerical method
gc = GreeksComputer(euro_option, numerical=True)

gc.get_greeks(underlying_price,
              interest_rate,
              volatility,
              start_date)
