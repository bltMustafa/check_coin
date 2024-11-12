import requests
import time
import hashlib

import hmac
from colorama import Fore, Style
from tabulate import tabulate

binance_coin_list_storage = []
bybit_coin_list_storage = []
gateio_coin_list_storage = []
coingecko_coin_list_storage = []

BYBIT_API_KEY = 'gGqEL06o9k3drwMmEg'
BYBIT_API_SECRET = 'Mv1PmbFThxTB05JJLZCZ0zvLxUpeGqcZVpBP'


def binance_coin_list():
    url = "https://api.binance.com/api/v3/ticker/24hr"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        for coin in data:
            symbol = coin.get("symbol")
            if symbol.endswith("USDT"):
                binance_coin_list_storage.append(symbol)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Binance API isteğinde bir hata oluştu:" + Style.RESET_ALL, e)


def bybit_coin_list():
    url = "https://api.bybit.com/v5/asset/coin/query-info"

    api_timestamp = str(int(time.time() * 1000))
    query_string = f"api_key={BYBIT_API_KEY}&timestamp={api_timestamp}"
    api_signature = hmac.new(BYBIT_API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    headers = {
        "X-BYBIT-APIKEY": BYBIT_API_KEY,
    }
    params = {
        "api_key": BYBIT_API_KEY,
        "timestamp": api_timestamp,
        "sign": api_signature
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        for coin in data.get("result", {}).get("rows", []):
            name = coin.get("name")
            bybit_coin_list_storage.append(name)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Bybit API isteğinde bir hata oluştu:" + Style.RESET_ALL, e)


def gate_io_coin_list():
    url = "https://api.gateio.ws/api/v4/spot/currency_pairs"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for coin in data:
            base = coin.get("id")
            if base.endswith("USDT"):
                gateio_coin_list_storage.append(base)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + 'Gate.io isteğinde bir hata oluştu:' + Style.RESET_ALL, e)


def coingecko_coin_list():
    url = 'https://api.coingecko.com/api/v3/coins/list'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for coin in data:
            name = coin.get("id")
            print(f'name>>>>', name)
            coingecko_coin_list_storage.append(name)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + 'Coingecko isteğinde bir hata oluştu:' + Style.RESET_ALL, e)


binance_coin_list()
bybit_coin_list()
gate_io_coin_list()
coingecko_coin_list()

binance_set = set(binance_coin_list_storage)
bybit_set = set(bybit_coin_list_storage)
gateio_set = set(gateio_coin_list_storage)
coingecko_set = set(coingecko_coin_list_storage)

only_in_binance = binance_set - bybit_set
only_in_binance_with_gateio = binance_set - gateio_set
only_in_binance_with_coingecko = binance_set - coingecko_set

only_in_bybit = bybit_set - binance_set
only_in_bybit_with_gateio = bybit_set - gateio_set
only_in_bybit_with_coingecko = bybit_set - coingecko_set

only_in_gateio = gateio_set - binance_set
only_in_gateio_with_bybit = gateio_set - bybit_set
only_in_gateio_with_coingecko = gateio_set - coingecko_set

only_in_coingecko = coingecko_set - binance_set
only_in_coingecko_with_gateio = coingecko_set - gateio_set
only_in_coingecko_with_bybit = coingecko_set - bybit_set

# print(Fore.BLUE + "\n=== Binance Coin Listesi ===" + Style.RESET_ALL)
# print(tabulate([[coin] for coin in binance_coin_list_storage], headers=["Binance Coins"], tablefmt="pretty"))

# print(Fore.BLUE + "\n=== Bybit Coin Listesi ===" + Style.RESET_ALL)
# print(tabulate([[coin] for coin in bybit_coin_list_storage], headers=["Bybit Coins"], tablefmt="pretty"))

# print(Fore.BLUE + "\n=== Gate.io Coin Listesi ===" + Style.RESET_ALL)
# print(tabulate([[coin] for coin in gateio_coin_list_storage], headers=["Gate.io Coins"], tablefmt="pretty"))

# print(Fore.RED + "\n=== Coingecko Coin Listesi ===" + Style.RESET_ALL)
# print(tabulate([[coin] for coin in coingecko_coin_list_storage], headers=["Coingecko Coins"], tablefmt="pretty"))

print(Fore.GREEN + "\n=== Binance'de olup Bybit'te olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_binance], headers=["Binance-Only Coins (Not in Bybit)"], tablefmt="pretty"))

print(Fore.GREEN + "\n=== Binance'de olup Gate.io'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_binance_with_gateio], headers=["Binance-Only Coins (Not in Gate.io)"],
               tablefmt="pretty"))

print(Fore.GREEN + "\n=== Binance'de olup Coin Gecko'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_binance_with_coingecko], headers=["Binance-Only Coins(Not in Coingecko)"],
               tablefmt="pretty"))

print(Fore.YELLOW + "\n=== Bybit'te olup Binance'de olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_bybit], headers=["Bybit-Only Coins (Not in Binance)"], tablefmt="pretty"))

print(Fore.YELLOW + "\n=== Bybit'te olup Gate.io'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_bybit_with_gateio], headers=["Bybit-Only Coins (Not in Gate.io)"],
               tablefmt="pretty"))

print(Fore.YELLOW + "\n=== Bybit'te olup Coin Gecko'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_bybit_with_coingecko], headers=["Bybit-Only Coins (Not in Coingecko)"],
               tablefmt="pretty"))

print(Fore.MAGENTA + "\n=== Gate.io'da olup Binance'de olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_gateio], headers=["Gate.io-Only Coins (Not in Binance)"], tablefmt="pretty"))

print(Fore.MAGENTA + "\n=== Gate.io'da olup Bybit'te olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_gateio_with_bybit], headers=["Gate.io-Only Coins (Not in Bybit)"],
               tablefmt="pretty"))

print(Fore.MAGENTA + "\n=== Gate.io da olup Coin Gecko'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_gateio_with_coingecko], headers=["Gate.io-Only Coins (Not in Coingecko)"],
               tablefmt="pretty"))

print(Fore.RED + "\n=== Coingecko da olup Binance'de olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_coingecko], headers=["Coingecko-Only Coins (Not in Binance)"],
               tablefmt="pretty"))

print(Fore.RED + "\n=== Coingecko da olup Bybit'de olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_coingecko_with_bybit], headers=["Coingecko-Only Coins (Not in Bybit)"],
               tablefmt="pretty"))

print(Fore.RED + "\n=== Coingecko da olup Gateio'da olmayan coinler ===" + Style.RESET_ALL)
print(tabulate([[coin] for coin in only_in_coingecko_with_gateio], headers=["Coingecko-Only Coins (Not in Gate.io)"],
               tablefmt="pretty"))
