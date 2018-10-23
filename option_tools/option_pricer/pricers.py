# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 14:09
# @Author  : Xin Zhang
# @File    : pricers.py

from .options.option_types import OptionType, ExerciseType

PRICER_COLLECTIONS = {}


def register_pricer(pricer_id):
    def wrapper(pricer_func):
        global PRICER_COLLECTIONS
        PRICER_COLLECTIONS[pricer_id] = pricer_func
        return pricer_func
    return wrapper


@register_pricer(12)
def european_(op):
    return op
