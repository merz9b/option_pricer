# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:43
# @Author  : Xin Zhang
# @File    : test_script_4.py

# --------------------------------------------------------------------------

from option_tools.option_pricer.options.option_base import EuropeanOption, AmericanOption, AsianOption, AmericanAsianOption, BarrierOptionBase


print(EuropeanOption.oid)
print(AmericanOption.oid)

print(AsianOption.oid)
print(BarrierOptionBase.oid)
print(AmericanAsianOption.oid)




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

option = EuropeanOption()

option.set_params(spot_price,
                  strike_price,
                  vol,
                  rf,
                  evaluation_date,
                  maturity_date)

option.set_type(OptionType.CALL)

if option.is_setup_finished():
    pass


class PricingEngine:
    def __init__(self):
        self.engine =  0

    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, option):
        xid = option.oid | self.engine
        return option
