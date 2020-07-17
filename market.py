import asyncio
import websockets
import json


async def subscribe(websocket, symbol, depth):
    # example: symbol='btcusdt', depth=10 ===> channel='btcusdt@depth10'
    channel = symbol + '@depth' + str(depth)
    payload = {'method': 'SUBSCRIBE',
               'params': [channel],
               'id': 4815162342}

    seried_payload = json.dumps(payload)
    await websocket.send(seried_payload)
    await websocket.recv()
    return websocket

async def run_orderbook_stream(endpoint_url, symbol, depth):
    websocket = await websockets.connect(endpoint_url)
    websocket = await subscribe(websocket=websocket, symbol=symbol, depth=depth)

    while True:
        data = await websocket.recv()
        # data = json.loads(data)
        print(f'[TICKER] {symbol.upper()}')

async def run_orderbooks_streams(*args, **kwargs):
    tasks = []
    for symbol in args:
        endpoint_url = kwargs["endpoint_url"]
        depth = kwargs["depth"]
        task = asyncio.create_task(run_orderbook_stream(endpoint_url=endpoint_url, symbol=symbol, depth=depth))
        tasks.append(task)

    await asyncio.gather(*tasks)

def listen(*args, **kwargs):
    # creates event loop
    asyncio.run(run_orderbooks_streams(*args, **kwargs))