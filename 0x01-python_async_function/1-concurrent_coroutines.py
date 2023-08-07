#!/usr/bin/env python3
"""
    Let's execute multiple coroutines at the same time with async.
"""

import asyncio
import random
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int = 0, max_delay: int = 10) -> float:
    """
        Spawn wait_random n times with the specified max_delay.
        Return the list of all the delays (float values).
    """
    tasks = [wait_random(max_delay) for _ in range(n)]
    delays = [await task for task in asyncio.as_completed(tasks)]
    return delays

if __name__ == "__main__":
    start = asyncio.get_event_loop().time()
    print(asyncio.run(wait_n(5, 5)))
    print(asyncio.run(wait_n(10, 7)))
    print(asyncio.run(wait_n(10, 0)))
    end = asyncio.get_event_loop().time()
    print("Total time: {}".format(end - start))
