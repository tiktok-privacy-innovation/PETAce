# Copyright 2023 TikTok Pte. Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Auxiliary functions for indexing.
"""

from typing import Tuple, Union


def format_int_index(index: int, limit: int, axis: int):
    """Convert an integer index to a valid index for a given axis.
    """
    if index >= limit or index < -limit:
        raise IndexError(f"index {index} is out of bounds for axis {axis} with size {limit}")
    if index < 0:
        index %= limit[0]
    return index


def format_slice_index(index: slice, limit: int, axis: int):
    """ Convert a slice index to a valid index for a given axis."""
    start = 0
    end = limit
    if index.start is not None:
        start = index.start
    if index.stop is not None:
        end = index.stop
    if start >= limit or start < -limit or end > limit or end < -limit:
        raise IndexError(f"index {index} is out of bounds for axis {axis} with size {limit}")
    if start < 0:
        start %= limit
    if end < 0:
        end %= limit
    if start >= end:
        raise IndexError("Empty array. slice start must be less than slice end")
    return start, end - start


def index_to_block_index(index: Union[int, slice, tuple], shape: Tuple, ndim: int) -> Tuple[int, int, int, int]:
    """Convert a slice or int index to (row_start, col_start, row_num, col_num)
    """
    # single index
    if isinstance(index, int):
        if ndim == 1:
            row_start = 0
            col_start = format_int_index(index, shape[0], 0)
            row_num = 1
            col_num = 1
        else:
            row_start = format_int_index(index, shape[0], 0)
            col_start = 0
            row_num = 1
            col_num = shape[1]
    # single slice
    elif isinstance(index, slice):
        if ndim == 1:
            col_start, col_num = format_slice_index(index, shape[0], 0)
            row_start = 0
            row_num = 1
        else:
            row_start, row_num = format_slice_index(index, shape[0], 0)
            col_start = 0
            col_num = shape[1]
    # tuple index
    elif isinstance(index, tuple):
        if len(index) != 2:
            raise IndexError("Only support at most 2-d index")
        if not isinstance(index[0], (int, slice)) or not isinstance(index[1], (int, slice)):
            raise IndexError(f"unsupported index type {type(index)}")
        if isinstance(index[0], int):
            row_start = format_int_index(index[0], shape[0], 0)
            row_num = 1
        else:
            row_start, row_num = format_slice_index(index[0], shape[0], 0)
        if isinstance(index[1], int):
            col_start = format_int_index(index[1], shape[1], 1)
            col_num = 1
        else:
            col_start, col_num = format_slice_index(index[1], shape[1], 1)
    else:
        raise IndexError(f"unsupported index type {type(index)}")
    return row_start, col_start, row_num, col_num
