#!/usr/bin/env python3
"""
    Module for async comprehension
"""
import asyncio
import random
from typing import Generator, List


async_comprehension = __import__('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
        Returns the 10 random numbers.
    """
    start = asyncio.get_running_loop().time()
    await asyncio.gather(*(async_comprehension() for i in range(4)))
    end = asyncio.get_running_loop().time()
    return end - start
