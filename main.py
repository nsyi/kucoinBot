from threading import Thread
import base64
import time
from datetime import datetime
import re
from webbrowser import get
import secret
import threading
import json
import hmac
import hashlib
import requests
from urllib.parse import urljoin, urlencode
import numpy as np
import websocket
import os
import collections


def clear():
    return os.system("clear")


BASE_URL = "https://api.kucoin.com"  # 'https://api.binance.com'
# url = 'https://openapi-sandbox.kucoin.com'
# All private REST requests must contain the following headers:

# KC-API-KEY The API key as a string.
# KC-API-SIGN The base64-encoded signature (see Signing a Message).
# Use API-Secret to encrypt the prehash string {timestamp+method+endpoint+body} with sha256 HMAC.
# The request body is a JSON string and need to be the same with the parameters passed by the API.
# KC-API-TIMESTAMP A timestamp for your request.
# KC-API-PASSPHRASE The passphrase you specified when creating the API key.
# For API key-V2.0, please Specify KC-API-KEY-VERSION as 2 --> Encrypt passphrase with HMAC-sha256 via API-Secret --> Encode contents by base64 before you pass the request."
# KC-API-KEY-VERSION You can check the version of API key on the page of API Management

headers = {
    "KC-API-KEY": secret.api_key,
    "KC-API-TIMESTAMP": str(int(time.time() * 1000)),
    "KC-API-PASSPHRASE": hmac.new(
        secret.api_secret.encode("utf-8"),
        secret.api_passphrase.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest(),
    "KC-API-KEY-VERSION": "2",
}

# <h2>3. How to Calculate Bitcoin’s Volatility?</h2>
# <p>Volatility is measured by sampling how far away Bitcoin’s price goes from the price at a fixed point in time. In our case – Bitcoin’s opening price on a specific day.</p>
# <p>Bitcoin’s daily volatility formula is actually the standard deviation of Bitcoin’s price.</p>
# <p>The standard deviation is calculated as follows = √(Bitcoin’s price variance).</p>
# <p>Bitcoin’s price variance is calculated as follows:</p>
# <ul>
# <li>Sample Bitcoin’s price at different time points throughout the day – the number of samples is N</li>
# <li>Calculate: (Bitcoin’s opening price – Price at N)^2</li>
# <li>Sum up all the results = ∑(Bitcoin’s opening price – Price at N)^2</li>
# <li>Divide the results by N = ∑(Bitcoin’s opening price – Price at N)^2 /N</li>
# <li>This is the Bitcoin’s variance</li></ul>

# From Bitcoin Volatility Index (0.69%) | Bitcoin Volatility Explained (2022 Updated)
# https://99bitcoins.com/bitcoin/historical-price/volatility/


def place_order(side, price, size, symbol):
    """Place an order
    Args:
        side (str): BUY or SELL
        price (float): price, e.g. 0.0001
        size (float): size, amount of base currency to buy or sell
        symbol (str): symbol, e.g. ETH-BTC
    Returns:
        None
    """

    path = "/api/v1/orders"
    url = urljoin(BASE_URL, path)
    method = "POST"
    now = int(time.time() * 1000)
    data = {
        "clientOid": str(now),
        "side": side,
        "symbol": symbol,
        "price": price,
        "size": size,
    }
    data_json = json.dumps(data)
    str_to_sign = str(now) + method + path + data_json
    signature = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            str_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            secret.api_passphrase.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": secret.api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
        "Content-type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, data_json, headers=headers)
    print(response.status_code)
    print(response.json())


def printit():  # Timer Setup
    path = "/api/v1/market/orderbook/level1"
    params_btc = {"symbol": "BTC-USDT"}
    auth = (secret.api_key, secret.api_secret)
    # GET /api/v1/market/orderbook/level1?symbol=BTC-USDT

    threading.Timer(0.3, printit).start()
    print(get_price("BTC-USDT"))


def get_price(symbol):
    path = "/api/v1/market/orderbook/level1"
    params = {"symbol": symbol}
    r = requests.get(BASE_URL + path, params=params)
    data = r.json()["data"]
    return data["price"]


def get_symbols(market):
    path = "/api/v1/symbols"
    r = requests.get(BASE_URL + path, params={"market": market})
    if r.status_code == 200:
        data = r.json()["data"]
        return data
    else:
        print(r.status_code)
        print(r.json())


def get_markets():
    path = "/api/v1/markets"
    r = requests.get(BASE_URL + path)
    data = r.json()["data"]
    print(data)


def get_balances():
    # Example for get balance of accounts in python
    path = "/api/v1/accounts"
    method = "GET"
    now = int(time.time() * 1000)
    str_to_sign = str(now) + method + path
    signature = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            str_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            secret.api_passphrase.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": secret.api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2",
    }
    response = requests.request(method, urljoin(BASE_URL, path), headers=headers)
    print(response.status_code)
    print(response.json())


def create_deposit_adress():
    # Example for create deposit addresses in python
    url = "https://openapi-sandbox.kucoin.com/api/v1/deposit-addresses"
    now = int(time.time() * 1000)
    data = {"currency": "BTC"}
    data_json = json.dumps(data)
    str_to_sign = str(now) + "POST" + "/api/v1/deposit-addresses" + data_json
    signature = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            str_to_sign.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    passphrase = base64.b64encode(
        hmac.new(
            secret.api_secret.encode("utf-8"),
            secret.api_passphrase.encode("utf-8"),
            hashlib.sha256,
        ).digest()
    )
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": secret.api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": 2,
        # specifying content type or using json=data in request
        "Content-Type": "application/json",
    }
    response = requests.request("post", url, headers=headers, data=data_json)
    print(response.status_code)
    print(response.json())


# GET /api/v1/market/candles?type=1min&symbol=BTC-USDT&startAt=1566703297&endAt=1566789757


def get_klines(symbol, type="1min", start="0", end="0"):
    """
    Args:
        symbol (str): symbol, e.g. ETH-BTC
        type (str): 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
        start (str): start time
        end (str): end time
    Returns:
        time, open, close, high, low, volume, turnover
    """
    path = "/api/v1/market/candles"
    params = {"symbol": symbol, "startAt": start, "endAt": end, "type": type}
    r = requests.get(BASE_URL + path, params=params)
    # print(response.status_code)
    # print(response.json())
    if r.status_code == 200:
        return r.json()["data"]
    else:
        # print(r.status_code)
        # print(r)
        return None


def get_std_deviation_percentage(data):
    """
    function to get the standard deviation percentage
    """
    # get the mean of the data
    mean = np.mean(data)
    # get the standard deviation of the data
    std_dev = np.std(data)
    # get the standard deviation percentage
    std_dev_percentage = (std_dev / mean) * 100
    # return the standard deviation percentage
    return std_dev_percentage


def get_initial_volatility(symbol, type="1min"):
    """
    Args:
        symbol (str): symbol, e.g. ETH-BTC
        type (str): 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
    Returns:
            volatility
    """
    kline = get_klines(symbol, type)
    if kline:
        highs = [float(i[3]) for i in kline]
        lows = [float(i[4]) for i in kline]
        all = highs + lows
        std = get_std_deviation_percentage(all)
        return std


def max_volatility():
    symbols = get_symbols("")
    volatility_list = {}
    max_val = 0
    for symbol in symbols:
        s = symbol["symbol"]
        vol = get_initial_volatility(s, "3min")
        if vol:
            # print(f'Volatility: %{vol:.2f} for {s}')
            volatility_list[s] = vol
            if vol > max_val:
                max_val = vol
                max_symbol = s
                print(f"Max volatility: %{max_val:.2f} for {max_symbol}")
    max_vol = max(volatility_list, key=volatility_list.get)
    print("-----------------")
    print(f"Max volatility: %{volatility_list[max_vol]:.2f} for {max_vol}")


url_t = "http://localhost:8000/records/%i"


def process_id(id):
    """process a single ID"""
    # fetch the data
    r = requests.get(url_t % id)
    # parse the JSON reply
    data = r.json()
    # and update some data with PUT
    requests.put(url_t % id, data=data)
    return data


def process_range(id_range, store=None):
    """process a number of ids, storing the results in a dict"""
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(id)
    return store


def get_initial_volatility_threaded(symbols, store=None, type="1min"):
    """process a number of ids, storing the results in a dict"""
    if store is None:
        store = {}
    for s in symbols:
        vol = get_initial_volatility(s, type)
        if vol:
            store[s] = vol
    return store


def threaded_process_range(nthreads, id_range, type="1min"):
    """process the id range in a specified number of threads"""
    store = {}
    threads = []
    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=get_initial_volatility_threaded, args=(ids, store, type))
        threads.append(t)

    # start the threads
    [t.start() for t in threads]
    # wait for the threads to finish
    [t.join() for t in threads]
    return store


def max_volatility_threaded(type):
    all_symbols = get_symbols("")
    symbol_names = [i["symbol"] for i in all_symbols]
    volatility_list = {}
    max_vol_prev = None
    start_time = datetime.now()
    try:
        volatility_list_new = threaded_process_range(300, symbol_names, type=type)
    except:
        print("Error")
    if volatility_list_new:
        for v in volatility_list_new:
            volatility_list[v] = volatility_list_new[v]
        max_vol = max(volatility_list, key=volatility_list.get)
        print("-----------------")
        print(f"Max volatility: %{volatility_list[max_vol]:.2f} for {max_vol}")
        if max_vol_prev:
            print(
                f"Max volatility previous: %{volatility_list[max_vol_prev]:.2f} for {max_vol_prev}"
            )
        max_vol_prev = max_vol
    total_time = str(datetime.now() - start_time)
    print(f"Total time: {total_time}")


def get_initial_data(symbol, type="1min"):
    kline = get_klines(symbol, type)
    if kline:
        symb_data = []
        for k in kline:
            symb_data.append(k[0:2])
        return symb_data


def get_data_threaded(symbols, store=None, type="1min"):
    if store is None:
        store = {}
    for s in symbols:
        data = get_initial_data(s, type)
        if data:
            store[s] = data
    return store


def threaded_data(nthreads, id_range, type="1min"):
    store = {}
    threads = []
    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=get_data_threaded, args=(ids, store, type))
        threads.append(t)

    # start the threads
    [t.start() for t in threads]
    # wait for the threads to finish
    [t.join() for t in threads]
    return store


def initial_data(type="1min", data_len=1000):
    all_symbols = get_symbols("")
    symbol_names = [i["symbol"] for i in all_symbols]
    data = threaded_data(300, symbol_names, type)
    data_deque = {}
    time_data = collections.deque(maxlen=data_len)
    for sym in data:
        data_deque[sym] = collections.deque(maxlen=data_len)
        for d in data[sym]:
            data_deque[sym].append(float(d[1]))

    for d in data[sym]:
        time_data.append(int(d[0]))

    return data_deque, time_data


def get_all_tickers():
    """Get all tickers"""
    path = "/api/v1/market/allTickers"
    r = requests.get(BASE_URL + path)
    if r.status_code == 200:
        return r.json()["data"]
    else:
        print(r.status_code)
        print(r.json())
        return None


def print_data(
    timestamp, tick_time, calc_time, start_time, vol_sorted, max_vol, max_sym, details
):
    clear()
    millis = int(timestamp[-1] - timestamp[0])
    seconds = (millis / 1000) % 60
    minutes = (millis / (1000 * 60)) % 60
    total_tick_time = calc_time - tick_time
    total_calc_time = datetime.now() - calc_time
    elapsed_time = datetime.now() - start_time
    elapsed_time_str = f"{(elapsed_time.seconds//60)%60}:{elapsed_time.seconds%60}"
    tick_time_str = f"{total_tick_time.seconds}.{total_tick_time.microseconds/1000:.0f}"
    calc_time_str = f"{total_calc_time.seconds}.{total_calc_time.microseconds/1000:.0f}"

    print(
        f"{minutes:00.0f}:{seconds:00.0f} - {tick_time_str} ms  - {calc_time_str} ms - {len(timestamp)}"
    )
    print("-" * 20)
    for i in range(5):
        sym = vol_sorted[i]
        if sym[0] in details:
            print(
                f"#{i}, {sym[0]:12}: %{sym[1]:4.2f}, {details[sym[0]]['last']:12}, High: {details[sym[0]]['high']:12}, Low: {details[sym[0]]['low']:12}"
            )
    print("-" * 20)
    print(f"Max of last {elapsed_time_str} - %{max_vol:.2f} for {max_sym}")


if __name__ == "__main__":
    start_time = datetime.now()
    # algo
    # Get initial volatility using klines
    # calculate instantanious volatility with tick in separate thread
    # determine the grid prices
    # place grid orders
    # fullfill orders and place new orders
    # repeat until volatility is low
    # contine to check for new pairs with high volatility
    # repeat

    # Initialize
    data = {}
    details = {}
    data_len = 1000
    timestamp = collections.deque(maxlen=data_len)
    volatility_data = {}
    max_vol = 0
    max_sym = ""

    # Get inital data
    # data, timestamp = initial_data('1min', data_len)

    while 1:
        try:
            tick_time = datetime.now()
            tick = get_all_tickers()
            calc_time = datetime.now()
            timestamp.append(tick["time"])
            # Get tickers
            for t in tick["ticker"]:
                if t["symbol"] not in data:
                    data[t["symbol"]] = collections.deque(maxlen=data_len)
                if t["last"] is not None:
                    data[t["symbol"]].append(float(t["last"]))
                    details[t["symbol"]] = {
                        "high": t["high"],
                        "low": t["low"],
                        "last": t["last"],
                    }
            for d in data:
                volatility_data[d] = get_std_deviation_percentage(data[d])
            # Get max
            if volatility_data:
                vol_sorted = sorted(
                    volatility_data.items(), key=lambda x: x[1], reverse=True
                )

                if vol_sorted[0][1] > max_vol:
                    max_sym = vol_sorted[0][0]
                    max_vol = vol_sorted[0][1]

            print_data(
                timestamp,
                tick_time,
                calc_time,
                start_time,
                vol_sorted,
                max_vol,
                max_sym,
                details,
            )

        except Exception as e:
            print(e)
            pass
