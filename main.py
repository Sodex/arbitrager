from multiprocessing import Process
import market
import strategy
import time


if __name__ == '__main__':
    kwargs = {'depth': 5, 'endpoint_url': 'wss://stream.binance.com:9443/ws'}
    args = ('btcusdt', 'btcrub', 'usdtrub')

    market_process = Process(target=market.init, args=args, kwargs=kwargs)
    strategy_process = Process(target=strategy.init, args=args)

    market_process.start()
    time.sleep(1)
    strategy_process.start()