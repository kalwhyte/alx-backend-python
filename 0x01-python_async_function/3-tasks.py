#!/usr/bin/env python3
"""
    3. Tasks
"""

import asyncio
import random
import time
wait_random = __import__('0-basic_async_syntax').wait_random


def task_wait_random(max_delay: int) -> asyncio.Task:
    """
        Take the code from wait_n and alter it into a new function task_wait_random.
        The code is nearly identical to wait_n except task_wait_random is
        taking in an integer argument (max_delay).
        spawn wait_random with max_delay.
        Return the asyncio.Task object.
    """
    task = asyncio.create_task(wait_random(max_delay))
    return task
