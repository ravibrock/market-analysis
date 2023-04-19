# Market analysis

## Purpose
A set of scripts I've written to process data from Kucoin and Bybit about crypto markets. Calculates things such as seasonality and % change. Not updated super frequently so bear in mind that if Bybit or Kucoin make API changes it has the potential of breaking one or more of the scripts.

## List of scripts
- `bybit_charting.Rmd` - Plots all Bybit tokens % change from a given start time
- `bybit_screener.Rmd` - Calculates a number of statistics, like beta to Bitcoin, for Bybit perpetual futures
- `bybit_seasonality.Rmd` - Finds seasonality over a predefined time period for Bybit perpetual futures.
- `kucoin_screener.Rmd` - Calculates a number of statistics, like beta to Bitcoin, for Kucoin perpetual futures
