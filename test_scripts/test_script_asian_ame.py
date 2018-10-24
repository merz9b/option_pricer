# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:18
# @Author  : Xin Zhang
# @File    : test_script_asian_ame.py

"""
Asian put option

strike : Arithmetic Average

payoff : Plain vannilla payoff

underlying_price_0 : 15000
start_date : 2018-07-05
end_date : 2018-10-03
volatility : 0.3
interest_rate : 0.01
dividend_rate : 0
"""

import QuantLib as Ql
from QuantLib import SimpleQuote
from option_tools.utils.tools import GreeksComputer
import random

start_date = Ql.Date(7, 7, 2018)
end_date = Ql.Date(3, 10, 2018) + 1

calendar = Ql.China()
day_counter = Ql.ActualActual()

# MC params
num_trials = 20
num_paths = 100000
time_steps = day_counter.dayCount(start_date, end_date)

# store whole period
period_by_days = [
    start_date +
    i for i in range(
        day_counter.dayCount(
            start_date,
            end_date))]

# set evaluation date
Ql.Settings.instance().evaluationDate = start_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 15000

underlying_price = SimpleQuote(15000)

interest_rate = SimpleQuote(0.01)

volatility = SimpleQuote(0.3)

dividend_rate = SimpleQuote(0)

# option exercise type
exercise = Ql.AmericanExercise(start_date, end_date)
payoff = Ql.PlainVanillaPayoff(Ql.Option.Call, strike_price)
#

# curve setup
dividend_curve = Ql.FlatForward(
    0,
    Ql.TARGET(),
    Ql.QuoteHandle(dividend_rate),
    day_counter)
interest_curve = Ql.FlatForward(
    0,
    Ql.TARGET(),
    Ql.QuoteHandle(interest_rate),
    day_counter)
volatility_curve = Ql.BlackConstantVol(
    0, Ql.TARGET(), Ql.QuoteHandle(volatility), day_counter)


# BS equation behind
bsm_process = Ql.BlackScholesMertonProcess(
    Ql.QuoteHandle(underlying_price),
    Ql.YieldTermStructureHandle(dividend_curve),
    Ql.YieldTermStructureHandle(interest_curve),
    Ql.BlackVolTermStructureHandle(volatility_curve))


past_fixs = 0
running_sum = 0

discrete_asian_option = Ql.DiscreteAveragingAsianOption(
    average_type,
    running_sum,
    past_fixs,
    Ql.DateVector(period_by_days),
    payoff,
    exercise)


mc_str = 'PseudoRandom'
is_bb = True
is_av = True
is_cv = True
n_require = 100000
tolerance = 0.05
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


discrete_asian_option.setPricingEngine(price_engine)

print(discrete_asian_option.NPV())

# 509.4412

steps = 200
discrete_asian_option.setPricingEngine(Ql.BinomialVanillaEngine(bsm_process, 'crr', steps))
print(discrete_asian_option.NPV())


gc = GreeksComputer(discrete_asian_option)

gks = gc.get_greeks(underlying_price,
                    interest_rate,
                    volatility,
                    end_date)

print(gks)
