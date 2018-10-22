# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 9:16
# @Author  : Xin Zhang
# @File    : test_schedule_script.py

import QuantLib as Ql
from QuantLib import Date, Period, DateGeneration


effective_date = Date(1, 10, 2018)
termination_date = Date(1, 11, 2018)

# tenor = Period(Ql.Monthly)
tenor = Period(Ql.Daily)

calendar = Ql.China()
business_convention = Ql.Following
termination_business_convention = Ql.Following

date_generation = DateGeneration.Forward
end_of_month = False

schedule = Ql.Schedule(effective_date,
                       termination_date,
                       tenor,
                       calendar,
                       business_convention,
                       termination_business_convention,
                       date_generation,
                       end_of_month)

list(schedule)
