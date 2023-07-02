import requests
import json
from configs import val


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одну и ту же валюту {quote}')

        try:
            quote_ticker = val[quote]
        except KeyError:
            raise APIException(f'Не удалось получить валюту {quote}. Проверьте правильность написания.')

        try:
            base_ticker = val[base]
        except KeyError:
            raise APIException(f'Не удалось получить валюту {base}. Проверьте правильность написания.')


        r = (requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}'))
        total_base = json.loads(r.content)[val[base]]
        return total_base
