# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 12:54
# @Author  : Xin Zhang
# @File    : engine_include_config.py

from .option_types import (
    EuropeanOption,
    AmericanOption,
    ArithmeticDiscreteAsianOption)

# MC OR ANALYTIC OR FD APPROXIMATION
# options using Monte Carlo engine
MC_INCLUDE = (
    ArithmeticDiscreteAsianOption.oid,
)

# options using finite difference engine
FD_INCLUDE = (
    AmericanOption.oid,
    ArithmeticDiscreteAsianOption.oid
)

# options using analytic engine
ANALYTIC_INCLUDE = (
    EuropeanOption.oid,
)
