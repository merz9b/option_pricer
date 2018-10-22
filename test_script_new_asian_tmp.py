# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 15:30
# @Author  : Xin Zhang
# @File    : test_script_new_asian_tmp.py


import QuantLib as Ql
from QuantLib import (SimpleQuote, Date)

start_date = Date(7, 7, 2018)
maturity_date = Date(3, 10, 2018) + 1

calendar = Ql.China()
day_counter = Ql.ActualActual()

# store whole period
fixing_dates = [
    start_date +
    i for i in range(
        day_counter.dayCount(
            start_date,
            maturity_date) + 1)][1:]

# set evaluation date
calculation_date = start_date
Ql.Settings.instance().evaluationDate = calculation_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 15000

spot_price = SimpleQuote(15000)

interest_rate = SimpleQuote(0.01)

volatility = SimpleQuote(0.3)

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
    start_date,
    Ql.QuoteHandle(dividend_rate),
    day_counter)
interest_curve = Ql.FlatForward(
    start_date,
    Ql.QuoteHandle(interest_rate),
    day_counter)
volatility_curve = Ql.BlackConstantVol(
    start_date,
    calendar,
    Ql.QuoteHandle(volatility),
    day_counter)

bsm_process = Ql.BlackScholesMertonProcess(
    Ql.RelinkableQuoteHandle(spot_price),
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

engine = Ql.FdBlackScholesAsianEngine(bsm_process, 300, 300, 50)

option.setPricingEngine(engine)

fdm_price = option.NPV()
fdm_delta = option.delta()
fdm_gamma = option.gamma()
print("BSM ASIAN FDM price is {0:.4f}".format(fdm_price))  # 524.4498
print("BSM ASIAN FDM delta is {0:.4f}".format(fdm_delta))
print("BSM ASIAN FDM gamma is {0:.4f}".format(fdm_gamma))


# option.vega()
# option.theta()
