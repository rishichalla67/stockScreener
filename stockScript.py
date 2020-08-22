import requests
from bs4 import BeautifulSoup

exchanges = ['NYSE', 'AMEX']


def PriceTracker(symbol):
    url = 'https://finance.yahoo.com/quote/{}?p={}&.tsrc=fin-srch'.format(symbol, symbol)
    price = 0
    valuation = 'N/A'
    prediction = 'N/A'
    chartPattern = 'N/A'
    compName = 'N/A'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')


    try:
        price = soup.find_all('div', {'class': 'D(ib) Mend(20px)'})[0].find('span').text
        compName = soup.find_all('h1', {'class': 'D(ib) Fz(18px)'})[0].text
        valuation = soup.find_all('div', {'class': 'Fw(b) Fl(end)--m Fz(s) C($primaryColor'})[0].text
        prediction = soup.find_all('div', {'class': 'Fz(xs) Mb(4px)'})[0].find('span').text
        chartPattern = soup.find_all('div', {'class': 'Mb(4px) Whs(nw)'})[0].text
    except IndexError:
        valuation = "N/A"

    return price, valuation, prediction, chartPattern, compName

i = 0
# O(n^2)

for x in exchanges:
    print('\n\n')
    print('*************** {} UNDERVALUED BULLISH SCREENER ***************'.format(x))
    print('Searching...')
    print("_________________________________________________")
    my_file = open("{}.txt".format(x), "r")
    symbols = my_file.readlines()
    for symbol in symbols:
        symbol = symbol.rstrip("\n")
        #print(symbol)
        if '-' not in symbol and '.' not in symbol:
            p, valuation, prediction, chartPattern, compName = PriceTracker(symbol)
            #print(compName)
            if valuation == 'Undervalued':
                if prediction == 'Bullish':
                    if valuation != 'N/A' and prediction != 'N/A':
                        print('{}: Current Price is {}. Bullish because {}'.format(compName, p, chartPattern))
                        i = i + 1
                        print("_________________________________________________")

print('{} amount of possible Stocks to look at'.format(i))