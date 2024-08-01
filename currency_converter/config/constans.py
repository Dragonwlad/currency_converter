'''Константы для криптовалют.'''



TYPE_CURRENCY = (
    ('Fiat', 'fiat'),
    ('Crypto', 'crypto')
)

CRYPTO = {
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


FIAT = {
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
}

FIAT_FROM_CRYPTOCOMPARE = {
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
}

FIAT_SIGN={
    "RUB":"₽",
    "AUD":"A$",
    "AZN":"₼",
    "GBP":"£",
    "AMD":"֏",
    "BYN":"Br",
    "BGN":"лв",
    "BRL":"R$",
    "HUF":"Ft",
    "VND":"₫",
    "HKD":"₫",
    "GEL":"₾",
    "DKK":"kr",
    "AED":"د.إ",
    "USD":"$",
    "EUR":"€",
    "EGP":"E£",
    "INR":"₹",
    "IDR":"Rp",
    "KZT":"₸",
    "CAD":"$",
    "QAR":"﷼",
    "KGS":"лв",
    "CNY":"¥",
    "MDL":"L",
    "NZD":"NZ$",
    "NOK":"kr",
    "PLN":"zł",
    "RON":"RON",
    "XDR":"XDR",
    "SGD":"S$",
    "TJS":"TJS",
    "THB":"฿",
    "TRY":"₺",
    "TMT":"T",
    "UZS":"лв",
    "UAH":"₴",
    "CZK":"Kč",
    "SEK":"kr",
    "CHF":"₣",
    "RSD":"РСД",
    "ZAR":"R",
    "KRW":"₩",
    "JPY":"¥",
}
