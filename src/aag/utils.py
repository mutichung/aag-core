import datetime
import logging
import os
import requests
from itertools import product

CURRENCY_BASE_URLS = (
    "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/",
    "https://raw.githubusercontent.com/fawazahmed0/currency-api/1/",
)
CURRENCY_SUFFIXES = (".min.json", ".json")

logger = logging.Logger(__name__)


def get_rate(src: str, dest: str, date: datetime.date | str = "latest") -> float:
    return _get_rate_impl(src, dest, date)


def _get_rate_impl(
    src: str,
    dest: str,
    date: datetime.date | str = "latest",
    should_fallback: bool = True,
) -> float:
    rate = None

    if isinstance(date, datetime.date):
        date = date.isoformat()

    for base_url, suffix in product(CURRENCY_BASE_URLS, CURRENCY_SUFFIXES):
        url = os.path.join(base_url, date, "currencies", src, dest + suffix)
        rate = requests.get(url)
        if rate.status_code == 200:
            break

    if not rate:
        if should_fallback:
            logger.warning(
                f"Falling back to latest ({datetime.date.today().isoformat()}) rate since the following combination "
                f"fails all attempts: {[src, dest, date]}."
            )
            return _get_rate_impl(src, dest, date="latest", should_fallback=False)
        raise RuntimeError(f"Cannot get currency rate {src} -> {dest} on date {date}.")

    return rate.json()[dest]
