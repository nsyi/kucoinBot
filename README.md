## 🚀 🚀 🚀 KUCOIN Trading Bot

Requires the following credentials in `secret.py`

```python
api_key = "<YOUR_KEY>"
api_secret "<YOUR_SECRET>"
api_passphrase "<YOUR_PASSPHRASE>"
```

`place_order` Places an order given the required arguments.

    Args:
        side (str): BUY or SELL
        price (float): price, e.g. 0.0001
        size (float): size, amount of base currency to buy or sell
        symbol (str): symbol, e.g. ETH-BTC
    Returns:
        None

## 📝 Notes

- [KUCOIN: Docs](https://docs.kucoin.com)
