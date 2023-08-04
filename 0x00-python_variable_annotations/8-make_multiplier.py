#!/usr/bin/env python3
'''Task 8 - Complex types - functions
'''
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    '''Returns a function that multiplies a float by multiplier.
    '''
    def multiply_by_multiplier(number: float) -> float:
        '''Returns the product of number and multiplier.
        '''
        return float(number * multiplier)
    return multiply_by_multiplier
