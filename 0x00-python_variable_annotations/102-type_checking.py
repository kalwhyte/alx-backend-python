#!/usr/bin/env python3
'''Task 102 - Type Checking
'''
from typing import Tuple, List, Any, Union, TypeVar, Mapping


T = TypeVar('T')


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    '''Returns a list.
    '''
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in
