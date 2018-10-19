# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 11:48
# @Author  : Xin Zhang
# @File    : tools.py

import QuantLib as Ql


def numerical_greeks(
        option,
        underlying_price,
        interest_rate,
        volatility,
        valuation_date):
    greeks_dict = {}

    u0 = underlying_price.value()
    p0 = option.NPV()
    h = 0.01

    underlying_price.setValue(u0 + h)
    p_plus = option.NPV()

    underlying_price.setValue(u0 - h)
    p_minus = option.NPV()

    # reset to original value
    underlying_price.setValue(u0)

    option_delta = (p_plus - p_minus) / (2 * h)

    # store delta
    greeks_dict['delta'] = option_delta

    option_gamma = (p_plus - 2 * p0 + p_minus) / (h * h)

    # store gamma
    greeks_dict['gamma'] = option_gamma

    r0 = interest_rate.value()
    h = 0.0001
    interest_rate.setValue(r0 + h)
    p_plus = option.NPV()

    interest_rate.setValue(r0)

    option_rho = (p_plus - p0) / h

    # store rho
    greeks_dict['rho'] = option_rho

    # vega
    v0 = volatility.value()
    volatility.setValue(v0 + h)
    p_plus = option.NPV()

    volatility.setValue(v0)

    # store vega
    greeks_dict['vega'] = (p_plus - p0) / h

    # calc theta
    d_o_w = valuation_date.weekday() - 1  # day of week
    if d_o_w == 6:
        # saturday
        Ql.Settings.instance().evaluationDate = valuation_date + 3
    elif d_o_w == 0:
        # sunday
        Ql.Settings.instance().evaluationDate = valuation_date + 2
    else:
        Ql.Settings.instance().evaluationDate = valuation_date + 1
    p1 = option.NPV()
    h = 1 / 365.0
    Ql.Settings.instance().evaluationDate = valuation_date

    # store theta
    greeks_dict['theta'] = (p1 - p0) / h
    return greeks_dict


def get_greeks(
        option,
        underlying_price=None,
        interest_rate=None,
        volatility=None,
        valuation_date=None,
        auto=True):
    try:
        if auto:
            greeks_dict = dict(
                delta=option.delta(),
                gamma=option.gamma(),
                theta=option.theta(),
                vega=option.vega(),
                rho=option.rho(),
            )
            return greeks_dict
        else:
            raise RuntimeError('Implement numerical method.')
    except RuntimeError:

        assert all([underlying_price is not None,
                    interest_rate is not None,
                    volatility is not None,
                    valuation_date is not None]), 'Parameters are needed in numerical method.'
        greeks_dict = numerical_greeks(
            option,
            underlying_price=underlying_price,
            interest_rate=interest_rate,
            volatility=volatility,
            valuation_date=valuation_date)
        return greeks_dict
