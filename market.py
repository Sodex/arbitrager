import asyncio
import websockets
import json



spot_balance = 150 # in $
btcusd_ask = 0
btcrub_bid = 0
usdrub_ask = 70.850
fee = 0.002


def calculate_arbitrage_opportunity():
	try:
		btc = spot_balance / btcusd_ask - (spot_balance / btcusd_ask) * fee
		rub = btc * btcrub_bid - (btc * btcrub_bid) * fee
		usd = rub / usdrub_ask - (rub / usdrub_ask) * fee
	except ZeroDivisionError:
		return 0
	else:
		return usd - spot_balance

async def subscribe(websocket, channel='btcusdt@bookTicker'):
    payload = {'method': 'SUBSCRIBE',
               'params': [channel],
               'id': 4815162342}

    seried_payload = json.dumps(payload)
    await websocket.send(seried_payload)
    await websocket.recv()

async def updates_handler(websocket):
    global btcusd_ask
    global btcrub_bid
    global usdrub_ask

    while True:
        data = await websocket.recv()
        data = json.loads(data)

        if data["s"] == 'BTCUSDT':
        	btcusd_ask = float(data["a"])
        elif data["s"] == 'BTCRUB':
        	btcrub_bid = float(data["b"])
        elif data["s"] == 'USDTRUB':
        	usdrub_ask = float(data["a"])

        result = calculate_arbitrage_opportunity()
        print(f'[ARBITRAGE_PROFIT] ${result:.2f} [TICKER] {data["s"]} [BEST_BID] {float(data["b"]):.2f} [BEST_ASK] {float(data["a"]):.2f}')

async def task(channel):
    websocket = await websockets.connect('wss://stream.binance.com:9443/ws')
    # подписываемся на обновления определенного канала
    await subscribe(websocket, channel)
    await updates_handler(websocket)

async def main():
    await asyncio.gather(task('btcusdt@bookTicker'), task('btcrub@bookTicker'), task('usdtrub@bookTicker'))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

