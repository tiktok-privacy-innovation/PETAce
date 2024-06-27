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

import numbers
from typing import Union

import numpy as np


def auto_broadcast(a: "SecureArray", b: Union["SecureArray", np.ndarray]):
    """
    Auto broadcast two array to same shape.

    Parameters
    ----------
    a : SecureArray
        The input array.
    b : Union[&quot;SecureArray&quot;, np.ndarray]
        The input array.

    Returns
    -------
    SecureArray
        The broadcasted array.
    """
    if isinstance(b, (bool, numbers.Number, np.number)):
        b = np.array(b)
    if a.shape == b.shape:
        return a, b
    if a.ndim != 0 and b.ndim != 0 and a.shape != b.shape:
        raise ValueError(f"Shape mismatch: {a.shape} and {b.shape}")
    if a.ndim == 0:
        a_resize = a.resize(b.shape)
        return a_resize, b
    if isinstance(b, np.ndarray):
        b = np.resize(b, a.shape)
    else:
        b = b.resize(a.shape)
    return a, b
