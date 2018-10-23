# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 12:43
# @Author  : Xin Zhang
# @File    : test_script_4.py

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
