## 🚀🚀🚀 KUCOIN Trading Bot 🚀🚀🚀

This is an implementation of the KUCOIN API for a max volatility algorithm. It will try to find the traiding pairs with max volatility to create a grid trading bot. Currently the grid trading part is not implemented. It works as follows:

1. Get initial volatility using klines
2. Calculate instantanious volatility with tick in separate thread
3. Determine the grid prices
4. Place grid orders
5. Fullfill orders and place new orders
6. Repeat until volatility is low
7. Contiue to check for new pairs with high volatility
8. Repeat

Requires the following credentials in `secret.py`

```python
api_key = "<YOUR_KEY>"
api_secret "<YOUR_SECRET>"
api_passphrase "<YOUR_PASSPHRASE>"
```

## Methods

`place_order` Places an order. You can place two types of orders: limit and market. Orders can only be placed if your account has sufficient funds. Once an order is placed, your account funds will be put on hold for the duration of the order. How much and which funds are put on hold depends on the order type and parameters specified.

    Args:
        side (str): BUY or SELL
        price (float): price, e.g. 0.0001
        size (float): size, amount of base currency to buy or sell
        symbol (str): symbol, e.g. ETH-BTC
    Returns:
        None

`get_klines` Request via this endpoint to get the kline of the specified symbol. Data are returned in grouped buckets based on requested type.

    Args:
        symbol (str): symbol, e.g. ETH-BTC
        type (str): 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
        start (str): start time
        end (str): end time
    Returns:
        time, open, close, high, low, volume, turnover

`get_initial_volatility` Returns the inital volatility
Args:
symbol (str): symbol, e.g. ETH-BTC
type (str): 1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
Returns:
volatility

## 📝 Notes

- [KUCOIN: Docs](https://docs.kucoin.com)
