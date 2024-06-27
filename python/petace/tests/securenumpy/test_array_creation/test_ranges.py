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

import numpy as np
import numpy.testing as npt

import petace.securenumpy as snp
from petace.tests.utils import SnpTestBase


class TestArange(SnpTestBase):

    def test_01(self, party_id):
        cipher = snp.arange(10)
        plain = cipher.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain, np.arange(10))

    def test_02(self, party_id):
        cipher = snp.arange(1, 10)
        plain = cipher.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain, np.arange(1, 10))

    def test_03(self, party_id):
        cipher = snp.arange(10, step=0.5)
        plain = cipher.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain, np.arange(10, step=0.5))


class TestLinspace(SnpTestBase):

    def test_01(self, party_id):
        arr0 = snp.linspace(0, 10)
        plain0 = arr0.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain0, np.linspace(0, 10), decimal=5)

    def test_02(self, party_id):
        arr1 = snp.linspace(2, 10, num=100)
        plain1 = arr1.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain1, np.linspace(2, 10, num=100), decimal=4)

    def test_03(self, party_id):
        arr2 = snp.linspace(2, 10, endpoint=False)
        plain2 = arr2.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain2, np.linspace(2, 10, endpoint=False), decimal=5)


class TestLogspace(SnpTestBase):

    def test_01(self, party_id):
        arr0 = snp.logspace(0, 6)
        plain0 = arr0.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain0, np.logspace(0, 6), decimal=4)

    def test_02(self, party_id):
        arr1 = snp.logspace(0, 6, num=100)
        plain1 = arr1.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain1, np.logspace(0, 6, num=100), decimal=4)

    def test_03(self, party_id):
        arr2 = snp.logspace(0, 6, endpoint=False)
        plain2 = arr2.reveal_to(0)
        if party_id == 0:
            npt.assert_almost_equal(plain2, np.logspace(0, 6, endpoint=False), decimal=5)
