import asyncio
import aioredis
import json

# todo: rewrite using multithreading since async approach is useless for cpu-bound operations


async def run_strategy(symbol, redis_connection):
    channel = (await redis_connection.subscribe(symbol))[0]
    assert isinstance(channel, aioredis.Channel)

    async for message in channel.iter():
        data = json.loads(message)
        print('Got message:', data)


async def run_strategeis(*args, **kwargs):
    redis_connection = await aioredis.create_redis(('localhost', 6379))

    strategies = []
    for symbol in args:
        strategy = asyncio.create_task(run_strategy(symbol=symbol, redis_connection=redis_connection))
        strategies.append(strategy)

    await asyncio.gather(*strategies)


def init(*args, **kwargs):
    asyncio.run(run_strategeis(*args, **kwargs))
