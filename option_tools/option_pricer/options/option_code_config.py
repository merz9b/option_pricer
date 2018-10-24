# -*- coding: utf-8 -*-
# @Time    : 2018/10/24 13:30
# @Author  : Xin Zhang
# @File    : option_code_config.py

"""
params level

1 : european or american

2 : vannilla or exotic

3 : asian or barrier

4 : discrete or continuous

5 : geometric or arithmetic



10 : engine : theoretic , mc or fd
"""


class CodeGen:
    # 1
    EUROPEAN = 1
    AMERICAN = 2

    # 2
    VANNILLA = 10
    EXOTIC = 20

    # 3
    ASIAN = 100
    BARRIER = 200

    # 4
    DISCRETE = 1000
    CONTINUOUS = 2000

    # 5
    GEOMETRIC = 10000
    ARITHMETIC = 20000


if __name__ == '__main__':
    print(CodeGen.AMERICAN)
