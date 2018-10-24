# Guosen option tools

## Setup

- install the package by executing:
```commandline
python setup.py install
```

# Reference Documents

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
