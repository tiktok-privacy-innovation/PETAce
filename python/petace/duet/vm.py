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

import struct
import numbers
import collections
from typing import Union, List, Tuple

import numpy as np

from petace.duet.pyduet import DuetVM, Instruction
from ._type import Private, Share, Public, PETAceType
from .exception import DuetVMError


class PETAceBuffer:
    """Array objects stored in C ++.

    Attributes
    ----------
    shape : tuple of ints
        Shape of created array.
    dtype : np.dtype
        Data type of created array.
    data_type : PETAceType
        Data type of created array.
    reg_addr : int
        Register address of created array.
    """

    def __init__(self, shape: Tuple[int], dtype: np.dtype, data_type: PETAceType, reg_addr: int):
        self.shape = shape
        self.dtype = dtype
        self.data_type = data_type
        self.reg_addr = reg_addr


class VM(DuetVM):
    """Virtual machine for PETAce.
    """
    _supported_operations = {
        "add",
        "sub",
        "mul",
        "div",
        "reveal",
        "share",
        "lt",
        "gt",
        "ge",
        "eq",
        "multiplexer",
        "argmax_and_max",
        "quick_sort",
        "sigmoid",
        "split_by_condition",
        "group_then_sum_by_grouped_count",
        "groupby_sum",
        "groupby_count",
        "reshape",
        "transpose",
        "resize",
        "not",
        "le",
        "and",
        "or",
        "xor",
        "set_item",
        "mat_mul",
        "groupby_max",
        "groupby_min",
    }

    def __check_type(self, data, _type):
        if not isinstance(data, _type):
            raise DuetVMError(f"Except {_type} but got {type(data)}")

    def __check_dtype(self, dtype):
        if dtype not in (np.float64, np.bool_):
            raise DuetVMError(f"unsupported dtype, {dtype}")

    def new_private(self, shape: Tuple[int], dtype: np.dtype, data: np.ndarray, party: int) -> PETAceBuffer:
        self.__check_dtype(dtype)

        if dtype == np.float64:
            reg_addr = self.new_private_double_matrix(party)
            data_type = Private.DOUBLE
        elif dtype == np.bool_:
            reg_addr = self.new_private_bool_matrix(party)
            data_type = Private.BOOL

        if data is not None:
            if dtype == np.float64:
                self.set_private_double_matrix(data, reg_addr)
            elif dtype == np.bool_:
                self.set_private_bool_matrix(data, reg_addr)
        return PETAceBuffer(shape, dtype, data_type, reg_addr)

    def new_share(self, shape: Tuple[int], dtype: np.dtype, share: np.ndarray = None) -> PETAceBuffer:
        self.__check_dtype(dtype)
        if share is not None:
            if share.ndim == 0:
                share = np.reshape(share, (1, 1))
            elif share.ndim == 1:
                share = np.reshape(share, (1, -1))
            elif share.ndim > 2:
                raise ValueError(f"Only support 0d, 1d or 2d array, got {share.ndim} dimension")

        if dtype == np.float64:
            reg_addr = self.new_airth_matrix()
            data_type = Share.DOUBLE
            if share is not None:
                self.set_airth_share_matrix(share, reg_addr)
        elif dtype == np.bool_:
            reg_addr = self.new_bool_matrix()
            data_type = Share.BOOL
            if share is not None:
                self.set_boolean_share_matrix(share, reg_addr)

        return PETAceBuffer(shape, dtype, data_type, reg_addr)

    def new_public(self, data: Union[numbers.Number, np.ndarray]) -> PETAceBuffer:
        self.__check_type(data, (numbers.Number, np.ndarray))
        if isinstance(data, numbers.Integral):
            data = int(data)
            shape = ()
            reg_addr = self.new_public_index()
            data_type = Public.IINT
            dtype = int
            self.set_public_index(data, reg_addr)
        elif isinstance(data, numbers.Number):
            data = float(data)
            shape = ()
            reg_addr = self.new_public_double()
            data_type = Public.IDOUBLE
            dtype = float
            self.set_public_double(data, reg_addr)
        elif isinstance(data, np.ndarray):
            self.__check_dtype(data.dtype)
            dtype = data.dtype
            shape = data.shape
            if data.ndim < 2:
                data = np.reshape(data, (1, -1))
            if dtype == np.float64:
                reg_addr = self.new_public_double_matrix()
                data_type = Public.DOUBLE
                self.set_public_double_matrix(data, reg_addr)
            elif dtype == np.bool_:
                reg_addr = self.new_public_bool_matrix()
                data_type = Public.BOOL
                self.set_public_bool_matrix(data, reg_addr)

        return PETAceBuffer(shape, dtype, data_type, reg_addr)

    def delete_buffer(self, obj: PETAceBuffer):
        self.__check_type(obj, PETAceBuffer)
        self.delete_data(obj.reg_addr)

    def to_numpy(self, obj: PETAceBuffer) -> np.ndarray:
        self.__check_type(obj, PETAceBuffer)
        if obj.data_type not in Private.support_types():
            raise DuetVMError(f"Only support private, unsupported data type, {obj.data_type}")
        if obj.dtype == np.float64:
            res = self.get_private_double_matrix(obj.reg_addr)
        elif obj.dtype == np.bool_:
            res = self.get_private_bool_matrix(obj.reg_addr)
        else:
            raise DuetVMError(f"unsupported dtype, {obj.dtype}")
        return res

    def to_share(self, obj: PETAceBuffer) -> np.ndarray:
        self.__check_type(obj, PETAceBuffer)
        if obj.data_type not in Share.support_types():
            raise DuetVMError(f"Only support share, unsupported data type, {obj.data_type}")
        if obj.dtype == np.float64:
            res = self.get_airth_share_matrix(obj.reg_addr)
        elif obj.dtype == np.bool_:
            res = self.get_boolean_share_matrix(obj.reg_addr)
        return res

    def execute_code(self, operation: str, objs: List[PETAceBuffer]) -> None:
        if operation not in self._supported_operations:
            raise DuetVMError(f"unsupported operation, {operation}")
        for obj in objs:
            self.__check_type(obj, PETAceBuffer)
        inst = Instruction([operation, *[obj.data_type for obj in objs]])
        self.exec_code(inst, [obj.reg_addr for obj in objs])

    def vstack(self, buffers: Union[List[PETAceBuffer], Tuple[PETAceBuffer]]) -> PETAceBuffer:
        if not isinstance(buffers, collections.Iterable):
            raise TypeError("Input must be an iterable")
        if len(buffers) < 2:
            raise ValueError("Input must be at least 2 arrays")
        shape = np.vstack([np.empty(buffer.shape) for buffer in buffers]).shape
        first = buffers[0]
        for i in buffers[1:]:
            ret = self.new_share(shape, np.float64)
            self.airth_share_vstack(first.reg_addr, i.reg_addr, ret.reg_addr)
            if first.reg_addr != buffers[0].reg_addr:
                self.delete_buffer(first)
            first = ret
        return ret

    def hstack(self, buffers: Union[List[PETAceBuffer], Tuple[PETAceBuffer]]) -> PETAceBuffer:
        if not isinstance(buffers, collections.Iterable):
            raise TypeError("Input must be an iterable")
        if len(buffers) < 2:
            raise ValueError("Input must be at least 2 arrays")
        shape = np.hstack([np.empty(buffer.shape) for buffer in buffers]).shape
        first = buffers[0]
        for i in buffers[1:]:
            ret = self.new_share(shape, np.float64)
            if len(first.shape) == 1:
                self.airth_share_vstack(first.reg_addr, i.reg_addr, ret.reg_addr)
            else:
                self.airth_share_hstack(first.reg_addr, i.reg_addr, ret.reg_addr)
            if first.reg_addr != buffers[0].reg_addr:
                self.delete_buffer(first)
            first = ret
        return ret

    def make_share(self,
                   data: Union[np.ndarray, None],
                   shape,
                   party: int = 0,
                   dtype: np.dtype = np.float64) -> PETAceBuffer:
        if dtype not in (np.float64, np.bool_):
            raise DuetVMError(f"unsupported dtype, {dtype}")
        if isinstance(data, np.ndarray):
            data = data.astype(dtype)
            if data.ndim < 2:
                data = data.reshape((1, -1))
        private_matrix = self.new_private(shape, dtype, data, party)
        share_matrix = self.new_share(shape, dtype)
        self.execute_code("share", [private_matrix, share_matrix])
        self.delete_buffer(private_matrix)
        return share_matrix

    def send_shape(self, shape: tuple):
        ndim = len(shape)
        self.send_buffer(bytearray(struct.pack('i', ndim)))
        if ndim > 0:
            self.send_buffer(bytearray(struct.pack('i' * ndim, *shape)))

    def recv_shape(self) -> tuple:
        ndim = struct.unpack('i', bytes(self.recv_buffer(4)))[0]
        if ndim == 0:
            return ()
        buffer = bytes(self.recv_buffer(4 * ndim))
        shape = struct.unpack('i' * ndim, buffer)
        return shape

    def inner_flatten(self, buffer: PETAceBuffer) -> PETAceBuffer:
        """transform 2d matrix to 1d matrix(row major).
        In-place
        """
        self.__check_type(buffer, PETAceBuffer)
        if len(buffer.shape) == 0:
            return buffer
        row_public = self.new_public(1)
        col_public = self.new_public(np.prod(buffer.shape))
        ret = self.new_share(buffer.shape, buffer.dtype)
        self.execute_code("reshape", [buffer, row_public, col_public, ret])
        self.delete_buffer(buffer)
        return ret
