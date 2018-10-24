# Guosen option tools

## Setup

- install the package by executing:
```commandline
python setup.py install
```

# Documents

## Engines and Options

Engines and options dependency relations are store in file `engine_include_config.py`.  

**European Option** : [ AnalyticBsmEuropeanEngine ]  
  
**American Option** : [ FdBsmAmericanEngine ]  
  
**Arithmetic Discrete Asian Option** : [ FdBsmDiscreteArithmeticAsianEngine, McBsmDiscreteArithmeticAsianEngine ]  


# Example usage

## Case one : European call option

>  European call option

>  evaluation date : 2018-03-07

>  maturity date : 2018-07-07

>  spot price : 100

>  strike price : 100

>  volatility : 0.2

>  risk_free_rate : 0.01

>  dividend rate : 0


```python
import QuantLib as Ql

from option_tools.option_pricer.options import EuropeanOption

from option_tools.option_pricer.engines import AnalyticBsmEuropeanEngine

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

option.set_engine(AnalyticBsmEuropeanEngine)

print(option.npv)

print(option.greeks)
```


## Case two : American put option

>  American put option

>  evaluation date : 2018-03-07

>  maturity date : 2018-07-07

>  spot price : 100

>  strike price : 100

>  volatility : 0.2

>  risk_free_rate : 0.01

>  dividend rate : 0


```python
import QuantLib as Ql

from option_tools.option_pricer.options import AmericanOption

from option_tools.option_pricer.engines import FdBsmAmericanEngine

spot_price = 100
strike_price = 100
evaluation_date = '2018-03-07'
maturity_date = '2018-07-07'
vol = 0.2
rf = 0.01

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
```


## Case three : Discrete Arithmetic Asian Call Option

>  Asian Call Option

>  evaluation date : 2018-01-01

>  maturity date : 2018-07-02

>  spot price : 100

>  strike price : 100

>  volatility : 0.1

>  risk_free_rate : 0.08

>  dividend rate : 0.05

> averaging period: 2018-01-01 to 2018-07-02

> averaging frequency : 7 days

> Asian Value (Haug, Haug and Margrabe): 1.9484



```python
import QuantLib as Ql

from option_tools.option_pricer.options import ArithmeticDiscreteAsianOption

from option_tools.option_pricer.engines import McBsmDiscreteArithmeticAsianEngine, FdBsmDiscreteArithmeticAsianEngine

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

# or using other engine
# asian_option.set_engine(FdBsmDiscreteArithmeticAsianEngine)

print(asian_option.is_setup_finished())

print(asian_option.npv)

print(asian_option.greeks)
```