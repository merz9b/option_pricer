# -*- coding: utf-8 -*-
# @Time    : 2018/10/23 11:18
# @Author  : Xin Zhang
# @File    : option_types.py


class OptionType:
    CALL = 0
    PUT = 1


class ExerciseType:
    EUROPEAN = 0
    AMERICAN = 2


class AsianAverageType:
    GEOMETRIC = 8
    ARITHMETIC = 4


class AveragingContinuity:
    DISCRETE = 0
    CONTINUOUS = 16


if __name__ == '__main__':
    s = [OptionType.CALL | ExerciseType.EUROPEAN,
         OptionType.CALL | ExerciseType.AMERICAN,
         OptionType.PUT | ExerciseType.EUROPEAN,
         OptionType.PUT | ExerciseType.AMERICAN,

         OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,
         OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.ARITHMETIC,

         OptionType.CALL | ExerciseType.EUROPEAN | AsianAverageType.GEOMETRIC,
         OptionType.PUT | ExerciseType.EUROPEAN | AsianAverageType.GEOMETRIC,

         OptionType.CALL | ExerciseType.EUROPEAN |
         AsianAverageType.ARITHMETIC | AveragingContinuity.CONTINUOUS,
         OptionType.PUT | ExerciseType.EUROPEAN |
         AsianAverageType.ARITHMETIC | AveragingContinuity.CONTINUOUS,

         OptionType.CALL | ExerciseType.EUROPEAN |
         AsianAverageType.GEOMETRIC | AveragingContinuity.CONTINUOUS,
         OptionType.PUT | ExerciseType.EUROPEAN |
         AsianAverageType.GEOMETRIC | AveragingContinuity.CONTINUOUS]
