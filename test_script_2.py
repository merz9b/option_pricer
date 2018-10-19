# -*- coding: utf-8 -*-
# @Time    : 2018/10/18 8:46
# @Author  : Xin Zhang
# @File    : test_script_2.py

import QuantLib as ql
import numpy as np
import pandas as pd


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
end_date = ql.Date(19, 5, 2019)

start_date + ql.Period('1M') * 7 + ql.Period('1D')

start_date + ql


d_r = pd.Series(pd.date_range(start_date.to_date(), end_date.to_date()))
d_r_1 = d_r[d_r.apply(lambda x:x.day == 18)]

lbk = (
    d_r_1.apply(
        lambda x: (
            x -
            pd.datetime(
                *
                start_date.to_date().timetuple()[
                    :3])).days) /
    365).tolist()

duration = (end_date.to_date() - start_date.to_date()).days / 365  # in years
lbk[-1] = duration
# lbk = lbk[1:]

ql.Settings.instance().evaluationDate = start_date
calendar = ql.China()
day_counter = ql.ActualActual()

time_steps = 1000
num_paths = 100000

mu = 0
price = ql.SimpleQuote(12000)
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

u = ql.QuoteHandle(price)
d = ql.YieldTermStructureHandle(dividend_curve)
r = ql.YieldTermStructureHandle(interest_curve)
v = ql.BlackVolTermStructureHandle(volatility_curve)

process = ql.BlackScholesMertonProcess(u, d, r, v)

day_counter.yearFraction(ql.Date(18, 10, 2018), ql.Date(19, 10, 2018))


time_from_reference = time_from_reference_factory(day_counter, start_date)
time_from_reference(ql.Date(19, 10, 2018))


rsg_unif = ql.UniformRandomSequenceGenerator(
    time_steps, ql.UniformRandomGenerator())
rsg_gaussian = ql.GaussianRandomSequenceGenerator(rsg_unif)


seq = ql.GaussianPathGenerator(
    process,
    duration,
    time_steps,
    rsg_gaussian,
    False)


one_path = seq.next()
path = one_path.value()

t = np.fromiter((path.time(j) for j in range(len(path))), dtype=np.float)
look_back_index = [np.searchsorted(t, tp) for tp in lbk]

sim_prices = np.zeros((num_paths, time_steps + 1))

for idx in range(num_paths):
    tmp_path = seq.next().value()
    sim_prices[idx, :] = np.fromiter(tmp_path, dtype=np.float)


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


def temp_pay_off(single_path):
    global look_back_index
    total_pay_off = 0
    for i in range(len(look_back_index) - 1):
        price_list = single_path[look_back_index[i]:look_back_index[i + 1]]
        m = price_list.mean()
        last_price = price_list[-1]
        strike = max(m, 13000) + 1000
        p_off = strike - last_price
        a_p_off = payoff_mapping(p_off)
        total_pay_off += a_p_off
    return total_pay_off


t_p_o = np.apply_along_axis(temp_pay_off, 1, sim_prices)
o_p = t_p_o.mean()
print('Price : ', o_p)

k = pd.date_range(start_date.to_date(), end_date.to_date(), periods=1001)
k1 = pd.DataFrame(sim_prices.T)
k1.index = k

k1.groupby(lambda x: (x.year, x.month, x.day)).first()
