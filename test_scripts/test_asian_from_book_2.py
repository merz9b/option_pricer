# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 9:39
# @Author  : Xin Zhang
# @File    : test_asian_from_book_2.py

"""
Asian Call Option (average price not strike)
Valuation date: 01-01-2018
Averaging period: 01-01-2018 until 30-06-2018
Underlying price : 100
Strike: 100
Volatility: 0.1
Risk free rate: 0.08
Dividend : 0.03

Asian Value (Haug, Haug and Margrabe): 1.9484
Asian Value (Curran): 12.7753
BS european value: 16.2952
"""

import QuantLib as Ql
from option_tools.utils.tools import GreeksComputer
import random
from QuantLib import (SimpleQuote, Date)

evaluation_date = Date(1, 1, 2018)
maturity_date = Date(2, 7, 2018)

avg_start = Date(1, 1, 2018)
avg_end = maturity_date

calendar = Ql.China()
day_counter = Ql.ActualActual()

duration_days = day_counter.dayCount(evaluation_date, maturity_date)

# MC params
num_trials = 20
num_paths = 100000
time_steps = day_counter.dayCount(evaluation_date, maturity_date)

# store whole period
# fixing_dates = [avg_end - i * 7 for i in range(day_counter.dayCount(avg_start,avg_end)//7 + 1) if avg_end - i * 7 >= avg_start][::-1]
fixing_dates = [avg_start + i * 7 for i in range(27)]

# fixing_scheduler = Ql.Schedule(
#     start_date,
#     end_date,
#     Ql.Period(Ql.Daily),
#     calendar,
#     Ql.Following,
#     Ql.Following,
#     Ql.DateGeneration.Backward,
#     False)
#
# fixing_dates = [d for d in fixing_scheduler][1:]

# set evaluation date
calculation_date = evaluation_date
Ql.Settings.instance().evaluationDate = calculation_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 100

underlying_price = SimpleQuote(100)

interest_rate = SimpleQuote(0.08)

volatility = SimpleQuote(0.1)

dividend_rate = SimpleQuote(0.05)

# option exercise type
exercise = Ql.EuropeanExercise(maturity_date)
payoff = Ql.PlainVanillaPayoff(option_type, strike_price)
# exercise = Ql.AmericanExercise(ql_valuation_date,ql_expiry_date)

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


# BS equation behind
bsm_process = Ql.BlackScholesMertonProcess(
    Ql.QuoteHandle(underlying_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(interest_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve))


past_fixes = 0
running_sum = 0

discrete_asian_option = Ql.DiscreteAveragingAsianOption(
    average_type,
    running_sum,
    past_fixes,
    Ql.DateVector(fixing_dates),
    payoff,
    exercise)


mc_str = 'PseudoRandom'
is_bb = True
is_av = True
is_cv = True
n_require = 100000
tolerance = strike_price / 100000.0
n_max = 200000
seed = random.randint(1, 1000)

price_engine = Ql.MCDiscreteArithmeticAPEngine(
    bsm_process,
    mc_str,
    is_bb,
    is_av,
    is_cv,
    n_require,
    tolerance,
    n_max,
    seed)

# price_engine_2 = Ql.MCDiscreteArithmeticAPEngine(
#     bsm_process,
#     'ld',
#     controlVariate = True,
#     requiredSamples = 100000
# )

discrete_asian_option.setPricingEngine(price_engine)

print(discrete_asian_option.NPV())  # 1.9457

gc = GreeksComputer(discrete_asian_option)

g = gc.get_greeks(underlying_price,
                  interest_rate,
                  volatility,
                  evaluation_date)

print(g)
