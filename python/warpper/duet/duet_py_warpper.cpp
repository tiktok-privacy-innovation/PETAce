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
#include "pybind11/functional.h"
#include "pybind11/pybind11.h"
#include "pybind11/stl.h"

#include "duet/util/matrix.h"
#include "network/network.h"

namespace py = pybind11;

PYBIND11_MODULE(pyduet, m) {
    py::class_<petace::duet::Instruction>(m, "Instruction").def(py::init<const std::vector<std::string>&>());

    py::class_<petace::duet::PythonDuetVM>(m, "DuetVM")
            .def(py::init<const std::shared_ptr<petace::network::Network>&, std::size_t>())
            .def("new_airth_matrix", &petace::duet::PythonDuetVM::new_data<petace::duet::ArithMatrix>)
            .def("new_bool_matrix", &petace::duet::PythonDuetVM::new_data<petace::duet::BoolMatrix>)
            .def("new_public_double_matrix", &petace::duet::PythonDuetVM::new_data<petace::duet::PublicMatrix<double>>)
            .def("new_public_double", &petace::duet::PythonDuetVM::new_data<petace::duet::PublicDouble>)
            .def("new_public_index", &petace::duet::PythonDuetVM::new_data<petace::duet::PublicIndex>)
            .def("new_public_bool_matrix", &petace::duet::PythonDuetVM::new_data<petace::duet::PublicMatrixBool>)
            .def("new_private_double_matrix", &petace::duet::PythonDuetVM::new_private_matrix<double>)
            .def("new_private_bool_matrix", &petace::duet::PythonDuetVM::new_private_matrix<std::int64_t>)
            .def("exec_code", &petace::duet::PythonDuetVM::exec_code)
            .def("set_private_double_matrix", &petace::duet::PythonDuetVM::set_private_double_matrix)
            .def("set_private_bool_matrix", &petace::duet::PythonDuetVM::set_private_bool_matrix)
            .def("set_public_double_matrix", &petace::duet::PythonDuetVM::set_public_double_matrix)
            .def("set_public_double", &petace::duet::PythonDuetVM::set_public_double)
            .def("set_public_index", &petace::duet::PythonDuetVM::set_public_index)
            .def("set_public_bool_matrix", &petace::duet::PythonDuetVM::set_public_bool_matrix)
            .def("set_airth_share_matrix", &petace::duet::PythonDuetVM::set_airth_share_matrix)
            .def("set_boolean_share_matrix", &petace::duet::PythonDuetVM::set_boolean_share_matrix)
            .def("get_private_double_matrix", &petace::duet::PythonDuetVM::get_private_double_matrix)
            .def("get_private_bool_matrix", &petace::duet::PythonDuetVM::get_private_bool_matrix)
            .def("get_airth_share_matrix", &petace::duet::PythonDuetVM::get_airth_share_matrix)
            .def("get_boolean_share_matrix", &petace::duet::PythonDuetVM::get_boolean_share_matrix)
            .def("delete_data", &petace::duet::PythonDuetVM::delete_data)
            .def("is_registr_empty", &petace::duet::PythonDuetVM::is_registr_empty)
            .def("party_id", &petace::duet::PythonDuetVM::party_id)
            .def("get_private_double_matrix_shape",
                    &petace::duet::PythonDuetVM::shape<petace::duet::PrivateMatrix<double>>)
            .def("get_public_double_matrix_shape",
                    &petace::duet::PythonDuetVM::shape<petace::duet::PublicMatrix<double>>)
            .def("get_airth_share_matrix_shape", &petace::duet::PythonDuetVM::shape<petace::duet::ArithMatrix>)
            .def("get_bool_share_matrix_shape", &petace::duet::PythonDuetVM::shape<petace::duet::BoolMatrix>)
            .def("public_double_matrix_block",
                    &petace::duet::PythonDuetVM::matrix_block<petace::duet::PublicMatrix<double>>)
            .def("private_double_matrix_block", &petace::duet::PythonDuetVM::private_matrix_block<double>)
            .def("airth_share_matrix_block", &petace::duet::PythonDuetVM::matrix_block<petace::duet::ArithMatrix>)
            .def("bool_share_matrix_block", &petace::duet::PythonDuetVM::matrix_block<petace::duet::BoolMatrix>)
            .def("private_double_vstack", &petace::duet::PythonDuetVM::private_vstack<double>)
            .def("public_double_vstack", &petace::duet::PythonDuetVM::vstack<petace::duet::PublicMatrix<double>>)
            .def("airth_share_vstack", &petace::duet::PythonDuetVM::vstack<petace::duet::ArithMatrix>)
            .def("bool_share_vstack", &petace::duet::PythonDuetVM::vstack<petace::duet::BoolMatrix>)
            .def("private_double_hstack", &petace::duet::PythonDuetVM::private_hstack<double>)
            .def("public_double_hstack", &petace::duet::PythonDuetVM::hstack<petace::duet::PublicMatrix<double>>)
            .def("airth_share_hstack", &petace::duet::PythonDuetVM::hstack<petace::duet::ArithMatrix>)
            .def("bool_share_hstack", &petace::duet::PythonDuetVM::hstack<petace::duet::BoolMatrix>)
            .def("send_buffer", &petace::duet::PythonDuetVM::send_buffer)
            .def("recv_buffer", &petace::duet::PythonDuetVM::recv_buffer);
}
