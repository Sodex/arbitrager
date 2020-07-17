import multiprocessing
import market

def main():
    pass


if __name__ == '__main__':
    market.listen('btcusdt', 'btcrub', 'usdtrub', depth=5, endpoint_url='wss://stream.binance.com:9443/ws')