import asyncio
import aioredis
import websockets
import json

# to do: ping-pong and ipc
 
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
    redis_connection = await aioredis.create_redis(('localhost', 6379))

    while True:
        data = await websocket.recv()
        await redis_connection.publish_json(symbol, data)


async def run_orderbooks_streams(*args, **kwargs):
    tasks = []
    for symbol in args:
        endpoint_url = kwargs["endpoint_url"]
        depth = kwargs["depth"]
        task = asyncio.create_task(run_orderbook_stream(endpoint_url=endpoint_url, symbol=symbol, depth=depth))
        tasks.append(task)

    await asyncio.gather(*tasks)


def init(*args, **kwargs):
    # creates event loop
    asyncio.run(run_orderbooks_streams(*args, **kwargs))