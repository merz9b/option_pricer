# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 15:30
# @Author  : Xin Zhang
# @File    : test_script_new_asian_tmp.py

"""
Asian Call Option (average price not strike)
Valuation date: 06-04-2017
Averaging period: 01-05-2017 until 31-05-2017 (May)
Underlying price (per 05-04-2017): 515.25
Strike: 515
Volatility: 20,669%
Risk free rate: 0,980%

Asian Value (Haug, Haug and Margrabe): 12.7763
"""


import QuantLib as Ql
from QuantLib import (SimpleQuote, Date)

evaluation_date = Date(6, 4, 2017)
maturity_date = Date(31, 5, 2017)

avg_start = Date(1, 5, 2017)
avg_end = maturity_date

calendar = Ql.China()
day_counter = Ql.ActualActual()

duration_days = day_counter.dayCount(evaluation_date, maturity_date)
# store whole period
fixing_dates = [
    avg_start +
    i for i in range(
        day_counter.dayCount(
            avg_start,
            avg_end) +
        1)]

# set evaluation date
calculation_date = evaluation_date
Ql.Settings.instance().evaluationDate = calculation_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 515

spot_price = SimpleQuote(515.25)

interest_rate = SimpleQuote(0.0098)

volatility = SimpleQuote(0.2669)

dividend_rate = SimpleQuote(0)


# option exercise type
exercise = Ql.EuropeanExercise(maturity_date)
payoff = Ql.PlainVanillaPayoff(Ql.Option.Call, strike_price)

# curve setup
# dividend_curve = Ql.FlatForward(
#     0,
#     Ql.TARGET(),
#     Ql.QuoteHandle(dividend_rate),
#     day_counter)
# interest_curve = Ql.FlatForward(
#     0,
#     Ql.TARGET(),
#     Ql.QuoteHandle(interest_rate),
#     day_counter)
# volatility_curve = Ql.BlackConstantVol(
#     0, Ql.TARGET(), Ql.QuoteHandle(volatility), day_counter)

# 2
#
dividend_curve = Ql.FlatForward(
    evaluation_date,
    Ql.QuoteHandle(dividend_rate),
    day_counter)
interest_curve = Ql.FlatForward(
    evaluation_date,
    Ql.QuoteHandle(interest_rate),
    day_counter)
volatility_curve = Ql.BlackConstantVol(
    evaluation_date,
    calendar,
    Ql.QuoteHandle(volatility),
    day_counter)

bsm_process = Ql.BlackScholesMertonProcess(
    Ql.RelinkableQuoteHandle(spot_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(interest_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve))


past_fixes = 1
running_sum = 0.0

option = Ql.DiscreteAveragingAsianOption(
    average_type,
    running_sum,
    past_fixes,
    Ql.DateVector(fixing_dates),
    payoff,
    exercise)

engine = Ql.FdBlackScholesAsianEngine(bsm_process, duration_days, 400, 200)

option.setPricingEngine(engine)

fdm_price = option.NPV()
fdm_delta = option.delta()
fdm_gamma = option.gamma()

print("BSM ASIAN FDM price is {0:.4f}".format(fdm_price))
print("BSM ASIAN FDM delta is {0:.4f}".format(fdm_delta))
print("BSM ASIAN FDM gamma is {0:.4f}".format(fdm_gamma))

# option.vega()
# option.theta()
