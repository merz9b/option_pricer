# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 10:31
# @Author  : Xin Zhang
# @File    : test_script_barrier.py

import QuantLib as Ql
from QuantLib import Date, BarrierOption, Barrier, SimpleQuote, QuoteHandle
from option_pricer.utils.tools import get_greeks

start_date = Date(8, 10, 2017)
end_date = Date(8, 1, 2018)

calendar = Ql.China()
day_counter = Ql.ActualActual()

Ql.Settings.instance().evaluationDate = start_date

payoff = Ql.PlainVanillaPayoff(Ql.Option.Call, 100)

barrier_option = BarrierOption(Barrier.UpIn,
                               120,  # barrier
                               0,  # rebase
                               payoff,
                               Ql.EuropeanExercise(end_date)
                               )

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

barrier_option.setPricingEngine(Ql.AnalyticBarrierEngine(process))

# price
print(barrier_option.NPV())

get_greeks(
    barrier_option,
    underlying_price,
    interest_rate,
    volatility,
    start_date)
