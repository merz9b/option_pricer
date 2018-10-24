# -*- coding: utf-8 -*-
# @Time    : 2018/10/17 9:12
# @Author  : Xin Zhang
# @File    : test_script.py

import abc


class Greeks:
    def __init__(self):
        self._delta = None
        self._gamma = None
        self._rho = None
        self._theta = None
        self._vega = None

    @property
    def delta(self):
        return self._delta

    @property
    def gamma(self):
        return self._gamma

    @property
    def rho(self):
        return self._rho

    @property
    def theta(self):
        return self._theta

    @property
    def vega(self):
        return self._vega

    @delta.setter
    def delta(self, delta):
        self._delta = delta

    @gamma.setter
    def gamma(self, gamma):
        self._gamma = gamma

    @rho.setter
    def rho(self, rho):
        self._rho = rho

    @theta.setter
    def theta(self, theta):
        self._theta = theta

    @vega.setter
    def vega(self, vega):
        self._vega = vega

    def to_dict(self):

        return {
            'delta': self.delta,
            'gamma': self.gamma,
            'rho': self.rho,
            'theta': self.theta,
            'vega': self.vega
        }

    def __str__(self):
        return str(self.to_dict())

    __repr__ = __str__


class OptionType(object):

    def __init__(self, root_type=''):
        self._path = root_type

    def __getattr__(self, path):
        return OptionType('{0}/{1}'.format(self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(OptionType().Euro.Call)

print(OptionType().America.Call)

print(OptionType().Setting.Fold)

greeks = Greeks()

print(greeks)

greeks.vega = 1
greeks.delta = 100
greeks.theta = 21
greeks.gamma = 30
greeks.rho = 10


greeks.to_dict()


print(greeks.to_dict())


class AbstractOption(metaclass=abc.ABCMeta):

    def __init__(self):

        self.underlying_price = None
        self.strike_price = None
        self.volatility = None
        self.start_date = None
        self.end_date = None
        self.r = None
        self.dividend = None
        self.__price_process = None
        self.__option_type = None
        self.__NPV = None
        self.__greeks = Greeks()

    @property
    def oid(self):
        return 1

    @abc.abstractmethod
    def greeks(self):
        raise NotImplementedError

    @abc.abstractmethod
    def NPV(self):
        raise NotImplementedError

    @abc.abstractmethod
    def set_process(self, process):
        """
        price movements process
        :param process: default, BSM
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_exercise(self, exercise_type):
        """
        set European or American
        :param exercise_type:
        :return: None
        """
    @abc.abstractmethod
    def set_type(self, option_type):
        """
        set call or put
        :param option_type:
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def set_parameters(
            self,
            underlying_price,
            strike_price,
            volatility,
            start_date,
            end_date,
            r,
            dividend=None):
        raise NotImplementedError


class AbstractPricingMachine(metaclass=abc.ABCMeta):

    def __init__(self, option: AbstractOption):
        self.option = option

    @abc.abstractmethod
    def compute_price(self, compute_engine):
        """
        using compute engine to get option price
        :param compute_engine: theoretical or MC
        :return: None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_greeks(self):

        raise NotImplementedError


class Pricing(AbstractPricingMachine):
    def compute_price(self, compute_engine):
        pass

    def compute_greeks(self):
        pass


class OptionBase:
    def __init__(self):
        self.price = None

    def __add__(self, other):
        o_b = self.__class__()
        o_b.price = self.price + other.price
        return o_b
    __radd__ = __add__

    def __mul__(self, other):
        try:
            pct = float(other)
            o_b = self.__class__()
            o_b.price = self.price * pct
            return o_b
        except ValueError:
            raise TypeError('Invalid mul value')
    __rmul__ = __mul__
# option 1 with oid 1


class opt_1(OptionBase):
    @property
    def oid(self):
        return 1
# option 2 with oid 2


class opt_2(OptionBase):
    @property
    def oid(self):
        return 2


method_dict = {}


def add_method(cls_ins):
    method_dict[cls_ins.id] = cls_ins()
    return cls_ins

m = {}
def d1(a):
    def wrapper(b):
        global m
        m[a] = b
        return b
    return wrapper

@d1(a = 1)
def s1():
    print(1)

m[1]()


class AbstractPricing(metaclass=abc.ABCMeta):
    id = None

    @abc.abstractmethod
    def __call__(self, option):
        raise NotImplementedError


@add_method
class PA(AbstractPricing):
    id = 1

    def __call__(self, option):
        assert option.oid == self.id, 'Wrong type of option'
        option.price = 1


@add_method
class PB(AbstractPricing):
    id = 2

    def __call__(self, option):
        assert option.oid == self.id, 'Wrong type of option'
        option.price = 2


def pricing(option):
    method_dict[option.oid](option)


o1 = opt_1()
print(o1.price)
# compute
pricing(o1)
# result : 1
print(o1.price)  # auto call PA to price o1


o2 = opt_2()
print(o2.price)
# compute price
pricing(o2)
# result : 2
print(o2.price)  # auto call PB to price o2

# combination of o1 and o2
o_combine = o1 + 0.5 * o2 + o1

pricing(o_combine)

print(o_combine.price)


def Result():
    price_l = []
    while True:
        price = yield 1
        price_l.append(price)
        if len(price_l) == 3:
            print(sum(price_l))


res = Result()
next(res)

res.send(4)
res.send(5)
res.send(6)


class AbstractType:
    pass

class OptionType(AbstractType):
    call = 0
    put = 1

class ExerciseType(AbstractType):
    American = 0
    European = 2

print(OptionType.call|ExerciseType.American)
print(OptionType.put|ExerciseType.American)
print(OptionType.call|ExerciseType.European)
print(OptionType.put|ExerciseType.European)


