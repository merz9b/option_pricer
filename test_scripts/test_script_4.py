# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:43
# @Author  : Xin Zhang
# @File    : test_script_4.py

# --------------------------------------------------------------------------
import QuantLib as Ql

from option_tools.option_pricer.engines import (AnalyticBsmEuropeanEngine,FdBsmAmericanEngine,
    FdBsmDiscreteArithmeticAsianEngine)

from option_tools.option_pricer.engines.engine_types import EngineType

from option_tools.option_pricer.options import (EuropeanOption, AmericanOption,
    ArithmeticDiscreteAsianOption)
from option_tools.utils.tools import get_signature_code

print(EngineType.ANALYTIC + EuropeanOption.oid)
# print(EngineType.MC + EuropeanOption.oid)
print(EngineType.FD + AmericanOption.oid)


print(ArithmeticDiscreteAsianOption.oid)
print(get_signature_code(ArithmeticDiscreteAsianOption.oid, 1))
print(get_signature_code(ArithmeticDiscreteAsianOption.oid, 5))


"""
European call option
evaluation date : 2018-03-07
maturity date : 2018-07-07
spot price : 100
strike price : 100
volatility : 0.2
risk_free_rate : 0.01
dividend rate : 0

price : 4.77139
"""

spot_price = 100
strike_price = 100
evaluation_date = '2018-03-07'
maturity_date = '2018-07-07'
vol = 0.2
rf = 0.01

option = EuropeanOption(Ql.Option.Put)

option.set_params(spot_price,
                  strike_price,
                  vol,
                  rf,
                  evaluation_date,
                  maturity_date)

if option.is_setup_finished():
    print('Setup finished')

option.set_engine(AnalyticBsmEuropeanEngine)
# option.set_engine(FdBsmAmericanEngine)

if option.is_setup_finished():
    print('Setup finished')

print(option.npv)
print(option.greeks)

ame_option = AmericanOption(Ql.Option.Put)
ame_option.set_params(spot_price,
                      strike_price,
                      vol,
                      rf,
                      evaluation_date,
                      maturity_date)
ame_option.set_engine(FdBsmAmericanEngine)

print(ame_option.npv)
print(ame_option.greeks)

"""
Asian Call Option (average price not strike)
Valuation date: 01-01-2018
Averaging period: 01-01-2018 until 02-07-2018
Underlying price : 100
Strike: 100
Volatility: 0.1
Risk free rate: 0.08
dividend : 0.05 [q = r - b]

Asian Value (Haug, Haug and Margrabe): 1.9484
"""
spot_price = 100
strike_price = 100
evaluation_date = '2018-01-01'
maturity_date = '2018-07-02'
vol = 0.1
rf = 0.08
dividend = 0.05

asian_option = ArithmeticDiscreteAsianOption(Ql.Option.Call)

asian_option.set_averaging_date(evaluation_date, maturity_date, 7)

asian_option.set_params(spot_price, strike_price, vol, rf, evaluation_date,
                        maturity_date, dividend)

asian_option.set_engine(McBsmDiscreteArithmeticAsianEngine)

asian_option.set_engine(FdBsmDiscreteArithmeticAsianEngine)

print(asian_option.is_setup_finished())

print(asian_option.npv)
print(asian_option.greeks)
