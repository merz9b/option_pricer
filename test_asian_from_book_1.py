# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 9:28
# @Author  : Xin Zhang
# @File    : test_asian_from_book_1.py

"""
Asian Call Option (average price not strike)
Valuation date: 01-01-2018
Averaging period: 01-01-2018 until 30-06-2018
Underlying price : 100
Strike: 100
Volatility: 0.1
Risk free rate: 0.08
dividend : 0.05 [q = r - b]

Asian Value (Haug, Haug and Margrabe): 1.9484
"""


import QuantLib as Ql
from QuantLib import (SimpleQuote, Date)

evaluation_date = Date(1, 1, 2018)
maturity_date = Date(2, 7, 2018)

avg_start = evaluation_date
avg_end = maturity_date

calendar = Ql.China()
day_counter = Ql.ActualActual()

duration_days = day_counter.dayCount(evaluation_date, maturity_date)
# store whole period
# fixing_dates = [
#     avg_start +
#     i for i in range(
#         day_counter.dayCount(
#             avg_start,
#             avg_end) +
#         1)]

# fixing_dates = [avg_end - i * 7 for i in range(day_counter.dayCount(avg_start,avg_end)//7 + 1) if avg_end - i * 7 >= avg_start][::-1]
fixing_dates = [avg_start + i * 7 for i in range(27)]
# set evaluation date
calculation_date = evaluation_date
Ql.Settings.instance().evaluationDate = calculation_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 100

spot_price = SimpleQuote(100)

interest_rate = SimpleQuote(0.08)

volatility = SimpleQuote(0.1)

dividend_rate = SimpleQuote(0.05)


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
    Ql.QuoteHandle(spot_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(interest_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve))


past_fixes = 0
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

print("BSM ASIAN FDM price is {0:.4f}".format(fdm_price))  # 2.1594
print("BSM ASIAN FDM delta is {0:.4f}".format(fdm_delta))
print("BSM ASIAN FDM gamma is {0:.4f}".format(fdm_gamma))
