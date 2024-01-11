import os
import requests
from itertools import product

CURRENCY_BASE_URLS = (
    "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/",
    "https://raw.githubusercontent.com/fawazahmed0/currency-api/1/",
)
CURRENCY_SUFFIXES = (".min.json", ".json")


def get_rate(src: str, dest: str, date: str = "latest") -> float:
    rate = None
    for base_url, suffix in product(CURRENCY_BASE_URLS, CURRENCY_SUFFIXES):
        url = os.path.join(base_url, date, "currencies", src, dest + suffix)
        rate = requests.get(url)
        if rate.status_code == 200:
            break

    if not rate:
        raise RuntimeError(f"Cannot get currency rate {src} -> {dest} on date {date}.")

    return rate.json()[dest]
