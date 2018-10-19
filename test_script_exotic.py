# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 15:52
# @Author  : Xin Zhang
# @File    : test_script_exotic.py

import QuantLib as ql
import numpy as np


def time_from_reference_factory(daycounter, ref):
    """
    returns a function, that calculate the time in years
    from a the reference date *ref* to date *dat*
    with respect to the given DayCountConvention *daycounter*

    Parameter:
        dayCounter (ql.DayCounter)
        ref (ql.Date)

    Return:

        f(np.array(ql.Date)) -> np.array(float)
    """

    def impl(dat):
        return daycounter.yearFraction(ref, dat)
    return np.vectorize(impl)


start_date = ql.Date(18, 10, 2018)
end_date = ql.Date(18, 5, 2019)

calendar = ql.China()
day_counter = ql.ActualActual()

time_from_reference = time_from_reference_factory(day_counter, start_date)


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
            end_date) +
        1)]

# store look back month
period_by_months = [start_date +
                    ql.Period(1, ql.Months) * i for i in range(7 + 1)]

month_end_index = [s - start_date for s in period_by_months]

# set evaluation date
ql.Settings.instance().evaluationDate = start_date


underlying_price = ql.SimpleQuote(13000)
sigma = ql.SimpleQuote(0.25)
dividend_rate = ql.SimpleQuote(0)
interest_rate = ql.SimpleQuote(0)

exercise = ql.EuropeanExercise(end_date)
dividend_curve = ql.FlatForward(
    0,
    ql.TARGET(),
    ql.QuoteHandle(dividend_rate),
    day_counter)
interest_curve = ql.FlatForward(
    0,
    ql.TARGET(),
    ql.QuoteHandle(interest_rate),
    day_counter)
volatility_curve = ql.BlackConstantVol(
    0, ql.TARGET(), ql.QuoteHandle(sigma), day_counter)

u = ql.QuoteHandle(underlying_price)
d = ql.YieldTermStructureHandle(dividend_curve)
r = ql.YieldTermStructureHandle(interest_curve)
v = ql.BlackVolTermStructureHandle(volatility_curve)

process = ql.BlackScholesMertonProcess(u, d, r, v)

# set random params
rsg_unif = ql.UniformRandomSequenceGenerator(
    time_steps, ql.UniformRandomGenerator())
rsg_gaussian = ql.GaussianRandomSequenceGenerator(rsg_unif)

duration = time_from_reference(end_date).tolist()

seq = ql.GaussianPathGenerator(
    process,
    duration,
    time_steps,
    rsg_gaussian,
    False)

trials_collections = []
for _ in range(num_trials):
    sim_prices = np.zeros((num_paths, time_steps + 1))
    for idx in range(num_paths):
        tmp_path = seq.next().value()
        sim_prices[idx, :] = np.fromiter(tmp_path, dtype=np.float)
    trials_collections.append(sim_prices)


def payoff_mapping(x):
    if x <= 0:
        return 0
    elif x <= 500:
        return x
    elif x <= 1000:
        return 500 + (x - 500) * 0.9
    elif x <= 1500:
        return 950 + (x - 1000) * 0.8
    elif x <= 2000:
        return 1350 + (x - 1500) * 0.6
    else:
        return 1650 + (x - 2000) * 0.4


def payoff_dev(underlying_price, strike):
    pay = underlying_price - strike
    return payoff_mapping(pay)


def temp_pay_off(single_path):
    global month_end_index
    total_pay_off = 0
    for i in range(len(month_end_index) - 1):
        price_list = single_path[month_end_index[i]:month_end_index[i + 1]]
        m = price_list.mean()
        last_price = price_list[-1]
        strike = max(m, 13000) + 1000
        a_p_off = payoff_dev(last_price, strike)
        total_pay_off += a_p_off
    return total_pay_off


option_price_collections = []
for i in range(num_trials):
    option_price_sim = np.apply_along_axis(
        temp_pay_off, 1, trials_collections[i])
    o_p = option_price_sim.mean()
    option_price_collections.append(o_p)


print('Price : ', np.mean(option_price_collections))
print('Std : ', np.std(option_price_collections))
