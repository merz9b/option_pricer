# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 15:51
# @Author  : Xin Zhang
# @File    : test_script_3.py

from QuantLib import *

start_date = Date(7, 7, 2018)
maturity_date = Date(4, 10, 2018)
volatility = 0.3
option_type = Option.Call
spot_price = 15000
strike_price = 15000

risk_free_rate = 0.1
dividend_rate = 0.
day_count = ActualActual()
calendar = China()

payoff = PlainVanillaPayoff(option_type, strike_price)
exercise = EuropeanExercise(maturity_date)

# fixing_scheduler = Schedule(
#     start_date,
#     maturity_date,
#     Period(Daily),
#     calendar,
#     Following,
#     Following,
#     DateGeneration.Backward,
#     False)
#
# fixing_dates = [d for d in fixing_scheduler][1:]

fixing_dates = [
    start_date +
    i for i in range(
        day_count.dayCount(
            start_date,
            maturity_date)+1)][1:]


print(fixing_dates[:3])
print(fixing_dates[-3:])

calculation_date = start_date
Settings.instance().evaluationDate = calculation_date

spot_handle = RelinkableQuoteHandle(SimpleQuote(spot_price))
flat_ts = YieldTermStructureHandle(
    FlatForward(
        calculation_date,
        risk_free_rate,
        day_count))
dividend_yield = YieldTermStructureHandle(
    FlatForward(calculation_date, dividend_rate, day_count))
flat_vol_ts = BlackVolTermStructureHandle(
    BlackConstantVol(
        calculation_date,
        calendar,
        volatility,
        day_count))

bsm_process = BlackScholesMertonProcess(
    spot_handle, dividend_yield, flat_ts, flat_vol_ts)

option = DiscreteAveragingAsianOption(
    Average.Arithmetic,
    0.,
    0,
    DateVector(fixing_dates),
    payoff,
    exercise)

engine = FdBlackScholesAsianEngine(bsm_process, 200, 100, 100)

option.setPricingEngine(engine)
fdm_price = option.NPV()
fdm_delta = option.delta()
print("BSM ASIAN FDM price is {0:.4f}".format(fdm_price))
print("BSM ASIAN FDM delta is {0:.4f}".format(fdm_delta))
# BSM ASIAN FDM price is 615.4783
# BSM ASIAN FDM delta is 0.5647