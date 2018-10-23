# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:43
# @Author  : Xin Zhang
# @File    : test_script_4.py

# --------------------------------------------------------------------------
from option_tools.option_pricer.options.engine_types import (
    EngineType, OptionType, ExerciseType, AveragingContinuity, AsianAverageType)


mc = (
    OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,
    OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,
)

fd = (
    OptionType.CALL | ExerciseType.AMERICAN,
    OptionType.PUT | ExerciseType.AMERICAN,
    OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC | AveragingContinuity.DISCRETE,
    OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC | AveragingContinuity.DISCRETE,
)

ana = (
    OptionType.CALL | ExerciseType.EUROPEAN,
    OptionType.PUT | ExerciseType.EUROPEAN,
)


for m in mc:
    print(m | EngineType.MC)

for f in fd:
    print(f | EngineType.FD)

for a in ana:
    print(a | EngineType.ANALYTIC)

for a in ana:
    print(a | EngineType.MC)

# --------------------------------------------------------------------------
from option_tools.option_pricer.options.option_base import EuropeanOption
from option_tools.option_pricer.options.option_types import OptionType

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
