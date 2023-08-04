#!/usr/bin/env python3
'''Task 6 - Complex types - mixed list
'''
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    '''Returns the sum of a list of floats.
    '''
    return float(sum(mxd_lst))
