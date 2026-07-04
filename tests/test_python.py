import sys
sys.path.append('../src/gateways')
from fsda_gateway import FSDA

fsda = FSDA()

result = fsda.run('getYahoo', 'AAPL', 'plots', False, 'LastPeriod', '1mo')
print(result)

fsda.close()