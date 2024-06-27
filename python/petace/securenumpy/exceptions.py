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


class AxisError(Exception):
    """
    Axis supplied was invalid.

    Parameters
    ----------
    axis : int or str
        The out of bounds axis or a custom exception message.
        If an axis is provided, then `ndim` should be specified as well.
    ndim : int, optional
        The number of array dimensions.
    msg_prefix : str, optional
        A prefix for the exception message.

    Attributes
    ----------
    axis : int, optional
        The out of bounds axis or ``None`` if a custom exception
        message was provided. This should be the axis as passed by
        the user, before any normalization to resolve negative indices.

    ndim : int, optional
        The number of array dimensions or ``None`` if a custom exception
        message was provided.
    """

    def __init__(self, axis, ndim=None):
        self.axis = axis
        self.ndim = ndim

    def __str__(self):
        return f"axis {self.axis} is out of bounds for array of dimension {self.ndim}"
