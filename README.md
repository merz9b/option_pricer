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


