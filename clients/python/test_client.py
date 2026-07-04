from fsda_client import FSDA

fs = FSDA()
result = fs.zscoreFS([[1,2,3],[4,5,6],[7,8,9]])
print(result)

# getYahoo bhi try karo
data = fs.getYahoo('AAPL', 'plots', False, 'LastPeriod', '1mo')
print(data['Ticker'], data['Success'])