#!/usr/bin/env python3
'''Task 101 - More involved type annotations
'''
from typing import Any, Mapping, TypeVar, Union


T = TypeVar('T')
Res = Union[Any, T]
Def = Union[T, None]


def safely_get_value(dct: Mapping, key: Any, default: Def = None) -> Res:
    '''Returns the value of a key in a dictionary.
    '''
    if key in dct:
        return dct[key]
    else:
        return default
