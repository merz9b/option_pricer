# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 10:31
# @Author  : Xin Zhang
# @File    : test_script_asian.py

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
fixing_dates = [
    start_date +
    i for i in range(
        day_counter.dayCount(
            start_date,
            end_date))]

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
calculation_date = start_date
Ql.Settings.instance().evaluationDate = calculation_date

#
option_type = Ql.Option.Call

average_type = Ql.Average.Arithmetic

strike_price = 15000

underlying_price = SimpleQuote(15000)

interest_rate = SimpleQuote(0.01)

volatility = SimpleQuote(0.3)

dividend_rate = SimpleQuote(0)

# option exercise type
exercise = Ql.EuropeanExercise(end_date)
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
dividend_curve = Ql.FlatForward(start_date, Ql.QuoteHandle(dividend_rate), day_counter)
interest_curve = Ql.FlatForward(start_date, Ql.QuoteHandle(interest_rate), day_counter)
volatility_curve = Ql.BlackConstantVol(start_date, calendar, Ql.QuoteHandle(volatility), day_counter)


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

# price_engine_2 = Ql.MCDiscreteArithmeticAPEngine(
#     bsm_process,
#     'ld',
#     controlVariate = True,
#     requiredSamples = 100000
# )

discrete_asian_option.setPricingEngine(price_engine)

print(discrete_asian_option.NPV())  # 515.4315

# continuous
continuous_asian_option = Ql.ContinuousAveragingAsianOption(
    average_type, payoff, exercise)
continuous_engine = Ql.ContinuousArithmeticAsianLevyEngine(
    bsm_process, Ql.QuoteHandle(SimpleQuote(0)), start_date)
continuous_asian_option.setPricingEngine(continuous_engine)
print(continuous_asian_option.NPV())  # 356.554

# Geometric average
running_sum_geo = 1

discrete_geo_option = Ql.DiscreteAveragingAsianOption(
    Ql.Average.Geometric,
    running_sum_geo,
    0,
    Ql.DateVector(fixing_dates),
    payoff,
    exercise
)

discrete_geo_engine = Ql.AnalyticDiscreteGeometricAveragePriceAsianEngine(
    bsm_process
)

discrete_geo_option.setPricingEngine(discrete_geo_engine)
print(discrete_geo_option.NPV())

gc_1 = GreeksComputer(discrete_geo_option)
gc_1.get_greeks()

gc_2 = GreeksComputer(discrete_geo_option, True)
gc_2.get_greeks(underlying_price,
                interest_rate,
                volatility,
                start_date)

# end of geo avg


gc = GreeksComputer(discrete_asian_option)

gks = gc.get_greeks(underlying_price,
                    interest_rate,
                    volatility,
                    end_date)

print(gks)
# NPV : 515
# {'delta': 0.5182452731389731,
#  'gamma': -0.0008162112408172106,
#  'rho': 820.4516033231357,
#  'vega': 1698.7409835303424,
#  'theta': -188132.51040833752}
