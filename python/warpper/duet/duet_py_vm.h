// Copyright 2023 TikTok Pte. Ltd.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once

#include <memory>
#include <vector>

#include "pybind11/numpy.h"
#include "pybind11/pybind11.h"

#include "duet/vm/duet_vm.h"

namespace py = pybind11;

namespace petace {
namespace duet {
class PythonDuetVM : public DuetVM {
public:
    using DuetVM::DuetVM;

    template <typename T>
    RegisterAddress new_private_matrix(std::size_t party_id) {
        return set_data(std::make_shared<PrivateMatrix<T>>(party_id));
    }

    void set_private_double_matrix(
            const py::array_t<double, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr);

    void set_private_bool_matrix(
            const py::array_t<bool, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr);

    void set_public_double_matrix(
            const py::array_t<double, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr);

    void set_airth_share_matrix(const py::array_t<std::int64_t, py::array::c_style | py::array::forcecast>& input_array,
            RegisterAddress addr);

    void set_boolean_share_matrix(
            const py::array_t<std::int64_t, py::array::c_style | py::array::forcecast>& input_array,
            RegisterAddress addr);

    void set_public_bool_matrix(
            const py::array_t<bool, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr);

    void set_public_double(PublicDouble value, RegisterAddress addr);

    void set_public_index(PublicIndex value, RegisterAddress addr);

    py::array_t<double, py::array::c_style | py::array::forcecast> get_private_double_matrix(RegisterAddress address);

    py::array_t<double, py::array::c_style | py::array::forcecast> get_public_double_matrix(RegisterAddress address);

    py::array_t<bool, py::array::c_style | py::array::forcecast> get_private_bool_matrix(RegisterAddress address);

    py::array_t<bool, py::array::c_style | py::array::forcecast> get_public_bool_matrix(RegisterAddress address);

    py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> get_airth_share_matrix(RegisterAddress addr);

    py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> get_boolean_share_matrix(RegisterAddress addr);

private:
    template <typename T>
    void numpy_to_eigen_(
            const py::array_t<T, py::array::c_style | py::array::forcecast>& input_numpy, Matrix<T>& output_eigen) {
        py::buffer_info buf_info = input_numpy.request();
        if (buf_info.ndim != 2)
            throw std::runtime_error("Number of dimensions must be two");

        auto array_ptr = static_cast<T*>(buf_info.ptr);
        Eigen::Map<Matrix<T>> mat(array_ptr, buf_info.shape[0], buf_info.shape[1]);
        output_eigen = Matrix<T>(mat);
    }

    template <typename T>
    void eigen_to_numpy_(
            const Matrix<T>& input_eigen, py::array_t<T, py::array::c_style | py::array::forcecast>& out_numpy) {
        out_numpy = py::array_t<T, py::array::c_style | py::array::forcecast>(
                {input_eigen.rows(), input_eigen.cols()}, input_eigen.data());
    }
};

}  // namespace duet
}  // namespace petace
