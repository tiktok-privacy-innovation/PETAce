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

#include "duet_py_vm.h"

#include "duet/util/matrix.h"

namespace petace {
namespace duet {

void PythonDuetVM::set_private_double_matrix(
        const py::array_t<double, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<PrivateMatrix<double>>& matirx_ptr = get_data<PrivateMatrix<double>>(addr);
    if (party_id() == matirx_ptr->party_id()) {
        numpy_to_eigen_(input_array, matirx_ptr->matrix());
    }
}

void PythonDuetVM::set_private_bool_matrix(
        const py::array_t<bool, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<PrivateMatrixBool>& matirx_ptr = get_data<PrivateMatrixBool>(addr);
    if (party_id() == matirx_ptr->party_id()) {
        py::buffer_info buf_info = input_array.request();
        if (buf_info.ndim != 2)
            throw std::runtime_error("Number of dimensions must be two");

        auto array_ptr = static_cast<bool*>(buf_info.ptr);
        matirx_ptr->resize(buf_info.shape[0], buf_info.shape[1]);

        for (size_t i = 0; i < matirx_ptr->size(); ++i) {
            if (array_ptr[i] == true) {
                (*matirx_ptr)(i) = 1;
            } else {
                (*matirx_ptr)(i) = 0;
            }
        }
    }
}

void PythonDuetVM::set_public_double_matrix(
        const py::array_t<double, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<PublicMatrix<double>>& matirx_ptr = get_data<PublicMatrix<double>>(addr);
    numpy_to_eigen_(input_array, matirx_ptr->matrix());
}

void PythonDuetVM::set_airth_share_matrix(
        const py::array_t<std::int64_t, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<ArithMatrix>& share_ptr = get_data<ArithMatrix>(addr);
    numpy_to_eigen_(input_array, share_ptr->shares());
}

void PythonDuetVM::set_boolean_share_matrix(
        const py::array_t<std::int64_t, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<BoolMatrix>& share_ptr = get_data<BoolMatrix>(addr);
    numpy_to_eigen_(input_array, share_ptr->shares());
}

void PythonDuetVM::set_public_double(PublicDouble value, RegisterAddress addr) {
    const std::shared_ptr<PublicDouble>& ptr = get_data<PublicDouble>(addr);
    *ptr = value;
}

void PythonDuetVM::set_public_index(PublicIndex value, RegisterAddress addr) {
    const std::shared_ptr<PublicIndex>& ptr = get_data<PublicIndex>(addr);
    *ptr = value;
}

void PythonDuetVM::set_public_bool_matrix(
        const py::array_t<bool, py::array::c_style | py::array::forcecast>& input_array, RegisterAddress addr) {
    const std::shared_ptr<PublicMatrixBool>& matirx_ptr = get_data<PublicMatrixBool>(addr);
    py::buffer_info buf_info = input_array.request();
    if (buf_info.ndim != 2)
        throw std::runtime_error("Number of dimensions must be two");

    auto array_ptr = static_cast<bool*>(buf_info.ptr);
    matirx_ptr->resize(buf_info.shape[0], buf_info.shape[1]);
    for (size_t i = 0; i < matirx_ptr->size(); ++i) {
        if (array_ptr[i] == true) {
            (*matirx_ptr)(i) = 1;
        } else {
            (*matirx_ptr)(i) = 0;
        }
    }
}

py::array_t<double, py::array::c_style | py::array::forcecast> PythonDuetVM::get_private_double_matrix(
        RegisterAddress addr) {
    const std::shared_ptr<PrivateMatrix<double>>& matirx_ptr = get_data<PrivateMatrix<double>>(addr);
    py::array_t<double, py::array::c_style | py::array::forcecast> ret;
    if (party_id() == matirx_ptr->party_id()) {
        eigen_to_numpy_(matirx_ptr->matrix(), ret);
    }
    return ret;
}

py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> PythonDuetVM::get_airth_share_matrix(
        RegisterAddress addr) {
    const std::shared_ptr<ArithMatrix>& share_ptr = get_data<ArithMatrix>(addr);
    py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> ret;
    eigen_to_numpy_(share_ptr->shares(), ret);
    return ret;
}

py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> PythonDuetVM::get_boolean_share_matrix(
        RegisterAddress addr) {
    const std::shared_ptr<BoolMatrix>& share_ptr = get_data<BoolMatrix>(addr);
    py::array_t<std::int64_t, py::array::c_style | py::array::forcecast> ret;
    eigen_to_numpy_(share_ptr->shares(), ret);
    return ret;
}

py::array_t<bool, py::array::c_style | py::array::forcecast> PythonDuetVM::get_private_bool_matrix(
        RegisterAddress address) {
    const std::shared_ptr<PrivateMatrixBool>& matirx_ptr = get_data<PrivateMatrixBool>(address);
    Matrix<bool> tmp;
    if (party_id() == matirx_ptr->party_id()) {
        tmp.resize(matirx_ptr->rows(), matirx_ptr->cols());
        for (std::size_t i = 0; i < matirx_ptr->size(); ++i) {
            tmp(i) = ((*matirx_ptr)(i) == 1 ? true : false);
        }
    }
    return py::array_t<bool, py::array::c_style | py::array::forcecast>({tmp.rows(), tmp.cols()}, tmp.data());
}

}  // namespace duet
}  // namespace petace
