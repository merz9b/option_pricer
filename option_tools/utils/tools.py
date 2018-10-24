# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 11:48
# @Author  : Xin Zhang
# @File    : tools.py

from datetime import datetime
import QuantLib as Ql


def cast_string_to_date(time_str, fmt='%Y-%m-%d'):
    d = datetime.strptime(time_str, fmt)
    return Ql.Date(d.day, d.month, d.year)

# get signature code by level


def get_signature_code(code, level):
    r = code % int(10 ** level)
    return r // int(10 ** (level - 1))


class GreeksComputer:
    def __init__(self, option, numerical=False):
        """
        initialize greeks computer
        :param option: QuantLib option object
        :param numerical: whether to using numerical method
        """
        self.greeks = dict()
        self.option = option
        self.numerical = numerical
        self.p0 = self.option.NPV()

    def get_greeks(self, underlying_price=None,
                   interest_rate=None,
                   volatility=None,
                   valuation_date=None):
        """
        get option greeks
        :param underlying_price: underlying_price quote
        :param interest_rate: interest_rate quote
        :param volatility: volatility quote
        :param valuation_date: valuation_date quote
        :return: greeks:dict
        """
        self._get_delta(underlying_price)
        self._get_gamma(underlying_price)
        self._get_rho(interest_rate)
        self._get_vega(volatility)
        self._get_theta(valuation_date)
        return self.greeks

    def _get_delta(self, underlying_price=None):
        try:
            if not self.numerical:
                d = self.option.delta()
            else:
                raise RuntimeError('Implement numerical method.')
        except RuntimeError:
            assert underlying_price is not None, 'Parameter<underlying_price> is needed in numerical method.'
            u0 = underlying_price.value()

            h = 0.01

            underlying_price.setValue(u0 + h)
            p_plus = self.option.NPV()

            underlying_price.setValue(u0 - h)
            p_minus = self.option.NPV()

            # reset to original value
            underlying_price.setValue(u0)

            d = (p_plus - p_minus) / (2 * h)

        self.greeks['delta'] = d

    def _get_gamma(self, underlying_price=None):
        try:
            if not self.numerical:
                g = self.option.gamma()
            else:
                raise RuntimeError('Implement numerical method.')
        except RuntimeError:
            assert underlying_price is not None, 'Parameter<underlying_price> is needed in numerical method.'
            u0 = underlying_price.value()

            h = 0.01

            underlying_price.setValue(u0 + h)
            p_plus = self.option.NPV()

            underlying_price.setValue(u0 - h)
            p_minus = self.option.NPV()

            # reset to original value
            underlying_price.setValue(u0)

            g = (p_plus - 2 * self.p0 + p_minus) / (h * h)

        self.greeks['gamma'] = g

    def _get_rho(self, interest_rate=None):
        try:
            if not self.numerical:
                r = self.option.rho()
            else:
                raise RuntimeError('Implement numerical method.')

        except RuntimeError:
            assert interest_rate is not None, 'Parameter<interest_rate> is needed in numerical method.'
            r0 = interest_rate.value()
            h = 0.0001
            interest_rate.setValue(r0 + h)
            p_plus = self.option.NPV()

            interest_rate.setValue(r0)

            r = (p_plus - self.p0) / h

        self.greeks['rho'] = r

    def _get_vega(self, volatility=None):
        try:
            if not self.numerical:
                v = self.option.vega()
            else:
                raise RuntimeError('Implement numerical method.')

        except RuntimeError:
            assert volatility is not None, 'Parameter<volatility> is needed in numerical method.'

            h = 0.0001

            v0 = volatility.value()
            volatility.setValue(v0 + h)
            p_plus = self.option.NPV()

            volatility.setValue(v0)

            v = (p_plus - self.p0) / h

        self.greeks['vega'] = v

    def _get_theta(self, valuation_date=None):
        try:
            if not self.numerical:
                t = self.option.theta()
            else:
                raise RuntimeError('Implement numerical method.')

        except RuntimeError:
            assert valuation_date is not None, 'Parameter<valuation_date> is needed in numerical method.'
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

            p1 = self.option.NPV()

            h = 1 / 365.0

            Ql.Settings.instance().evaluationDate = valuation_date

            # store theta
            t = (p1 - self.p0) / h
        self.greeks['theta'] = t


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
