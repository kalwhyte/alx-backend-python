#!/usr/bin/env python3
""" 
    Using the (async) measure_time function
"""
import asyncio
import time


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """ 
        Measure the total execution time for wait_n(n, max_delay), and
        return the total_time / n. Your function should return a float.
    """
    start = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    end = time.perf_counter()
    total_time = end - start
    return (total_time) / n
