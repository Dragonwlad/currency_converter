
currency = {
    "RUB": "Russian Ruble",
    "AUD": "Australian Dollar",
    "AZN": "Azerbaijani Manat",
    "GBP": "British Pound Sterling",
    "AMD": "Armenian Dram",
    "BYN": "Belarusian Ruble",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "HUF": "Hungarian Forint",
    "VND": "Vietnamese Dong",
    "HKD": "Hong Kong Dollar",
    "GEL": "Georgian Lari",
    "DKK": "Danish Krone",
    "AED": "UAE Dirham",
    "USD": "United States Dollar",
    "EUR": "Euro",
    "EGP": "Egyptian Pound",
    "INR": "Indian Rupee",
    "IDR": "Indonesian Rupiah",
    "KZT": "Kazakhstani Tenge",
    "CAD": "Canadian Dollar",
    "QAR": "Qatari Rial",
    "KGS": "Kyrgystani Som",
    "CNY": "Chinese Yuan",
    "MDL": "Moldovan leu",
    "NZD": "New Zealand Dollar",
    "NOK": "Norwegian Krone",
    "PLN": "Polish Zloty",
    "RON": "Romanian Leu",
    "XDR": "Special Drawing Rights",
    "SGD": "Singapore dollar",
    "TJS": "Tajikistani somoni",
    "THB": "Thai baht",
    "TRY": "Turkish Lira",
    "TMT": "Turkmenistani Manat",
    "UZS": "Uzbekistan Som",
    "UAH": "Ukranian Hryvnia",
    "CZK": "Czech Koruna",
    "SEK": "Swedish Krona",
    "CHF": "Swiss Franc",
    "RSD": "Serbian Dinar",
    "ZAR": "South African Rand",
    "KRW": "Korean Won",
    "JPY": "Japanese Yen",
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "XRP": "XRP",
    "ARB": "Arbitrum",
    "USDC": "USD Coin",
    "FDUSD": "First Digital USD",
    "DOGE": "Dogecoin",
    "USDT": "Tether",
    "AVAX": "Avalanche",
    "OP": "Optimism",
    "ADA": "Cardano",
    "BNB": "Binance Coin",
    "MATIC": "Polygon",
    "LINK": "Chainlink",
    "WSB": "WallStreetBets DApp",
    "BONK": "Bonk",
    "LTC": "Litecoin",
    "ETC": "Ethereum Classic",
    "LDO": "Lido DAO",
    "TIA": "Celestia",
    "FIL": "FileCoin",
    "MANTLE": "Mantle",
    "SEI": "Sei",
    "INJ": "Injective",
    "SHIB": "Shiba Inu",
    "BCH": "Bitcoin Cash",
    "ICP": "Internet Computer",
    "STX": "Stacks",
    "DOT": "Polkadot",
    "TRX": "TRON",
    "NEAR": "Near",
    "PEOPLE": "ConstitutionDAO",
    "ENS": "Ethereum Name Service",
    "APT": "Aptos",
    "SUI": "Sui",
    "TUSD": "True USD",
    "GMT": "STEPN",
    "BSV": "Bitcoin SV",
    "WBTC": "Wrapped Bitcoin",
}

currency_from_CB = {'HUF', 'HKD', 'QAR', 'UZS', 'EGP', 'MDL', 'RSD', 'NOK',
                    'AMD', 'TJS', 'XDR', 'AED', 'AZN', 'KGS', 'INR', 'VND',
                    'SEK', 'TMT'}

currency_from_crypto = {'THB', 'SOL', 'TRY', 'NZD', 'SGD', 'CZK', 'ARB', 'HUF',
                        'HKD', 'AVAX', 'QAR', 'UZS', 'BNB', 'SUI', 'EGP',
                        'LTC', 'RON', 'MDL', 'CAD', 'XRP', 'PEOPLE', 'JPY',
                        'SEI', 'ENS', 'RSD', 'DOGE', 'BCH', 'PLN',
                        'TUSD', 'BSV', 'NOK', 'ETC', 'AMD', 'AUD',
                        'ICP', 'TJS', 'ETH', 'XDR', 'GBP', 'USD',
                        'EUR', 'FDUSD', 'AED', 'BGN', 'CHF', 'UAH',
                        'TIA', 'LINK', 'WBTC', 'KZT', 'BYN', 'DOT',
                        'SHIB', 'BONK', 'INJ', 'MATIC', 'DKK', 'FIL',
                        'AZN', 'KGS', 'KRW', 'USDC', 'INR', 'LDO', 'ZAR',
                        'VND', 'BTC', 'OP', 'USDT', 'MANTLE', 'SEK', 'TRX',
                        'STX', 'CNY', 'IDR', 'TMT', 'GMT', 'RUB', 'BRL',
                        'GEL', 'APT', 'ADA', 'WSB', 'NEAR'
                        }

valuete = ''

for key in currency.keys():
    valuete += key + ','
valuete = valuete[0:len(valuete)-1]
# print(valuete)

url = f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={valuete}&tsyms=USD'
print(url)

# x = map(lambda *args: args, [1, 2], [3, 4])
# print(x)
# x = dict(x)
# print(x)


from typing import Callable


def invert(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            return [i + 1 for i in result]
        else:
            raise RuntimeError

    return wrapper

 
@invert
def square(numbers: list) -> list:
    return [i**2 for i in numbers]


asd = [1, 2, 3, 4, 5]
print(square(asd))


def test() -> None:
    assert square([1, 2, 3, 4, 5]) == [2, 5, 10, 17, 26]


test()

def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure = outer_function(10)
print(closure)  # => 15