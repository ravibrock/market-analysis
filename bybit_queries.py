import json
import requests
import pandas as pd
import time


def candle_length(start_time):
    difference = (time.time() - int(start_time)) / (60 * 200)
    if difference < 1:
        return "1"
    elif 1 <= difference < 3:
        return "3"
    elif 3 <= difference < 5:
        return "5"
    elif 5 <= difference < 15:
        return "15"
    elif 15 <= difference < 30:
        return "30"
    elif 30 <= difference < 60:
        return "60"
    elif 60 <= difference < 120:
        return "120"
    elif 120 <= difference < 240:
        return "240"
    elif 240 <= difference < 360:
        return "360"
    elif 360 <= difference < 720:
        return "720"
    elif 720 <= difference < 1440:
        return "D"
    elif 1440 <= difference < 10080:
        return "W"
    elif 10080 <= difference:
        raise Exception("Start time must be within the last 50 weeks.")


def get_tickers(quote_currency=None):
    url = "https://api.bybit.com/v2/public/symbols"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        data = response.json()
        df = pd.DataFrame(data["result"]).iloc[:, :-4]
        df = df[df["status"] == "Trading"].drop(columns=["status"])
        if quote_currency:
            df = df[df["quote_currency"] == quote_currency]
        return df.reset_index(drop=True)


def market_data(symbol, interval, start_time):
    url = "https://api.bybit.com/public/linear/kline"
    querystring = {"symbol": symbol, "interval": interval, "from": start_time}
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    else:
        data = response.json()
        if json.loads(response.text)["ret_code"] != 0:
            raise Exception(json.loads(response.text)["ret_msg"])
        df = pd.DataFrame(data["result"])
        return df
