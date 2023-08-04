#!/usr/bin/env python3
'''Task 7 - Complex types
'''
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    '''Returns a tuple of a string and a float.
    '''
    return (k, v * v)
