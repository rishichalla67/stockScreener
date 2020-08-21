import requests
from bs4 import BeautifulSoup

exchanges = ['NYSE', 'AMEX']


def PriceTracker(symbol):
    url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(symbol, symbol)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'lxml')
    price = 0
    valuation = 'N/A'
    prediction = 'N/A'
    chartPattern = 'N/A'
    try:
        price = soup.find_all('div', {'class': 'D(ib) Mend(20px)'})[0].find('span').text
        valuation = soup.find_all('div', {'class': 'Fw(b) Fl(end)--m Fz(s) C($primaryColor'})[0].text
        prediction = soup.find_all('div', {'class': 'Fz(xs) Mb(4px)'})[0].find('span').text
        chartPattern = soup.find_all('div', {'class': 'Mb(4px) Whs(nw)'})[0].text
    except IndexError:
        valuation = 'N/A'

    return price, valuation, prediction, chartPattern

# O(n^2)
for x in exchanges:
    print('*************** {} UNDERVALUED BULLISH SCREENER ***************'.format(x))
    print('Searching...')
    my_file = open("{}.txt".format(x), "r")
    symbols = my_file.readlines()
    for symbol in symbols:
        symbol = symbol.rstrip("\n")
        if '-' not in symbol and '.' not in symbol:
            p, valuation, prediction, chartPattern = PriceTracker(symbol)
            price = float(p)
            if valuation == 'Undervalued':
                if prediction == 'Bullish':
                    if valuation != 'N/A' and prediction != 'N/A':
                        if price <= 10.00:
                            print('{}: {})'.format(symbol, chartPattern))
