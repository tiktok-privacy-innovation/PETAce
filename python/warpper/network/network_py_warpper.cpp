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

#include <pybind11/stl.h>

#include "pybind11/pybind11.h"

#include "network/net_factory.h"
#include "network/net_socket.h"
#include "network/network.h"

namespace py = pybind11;

PYBIND11_MODULE(pynetwork, m) {
    py::enum_<petace::network::NetScheme>(m, "NetScheme")
            .value("SOCKET", petace::network::NetScheme::SOCKET)
            .value("AGENT", petace::network::NetScheme::AGENT)
            .export_values();

    py::class_<petace::network::NetParams>(m, "NetParams")
            .def(py::init<>())
            .def_readwrite("local_addr", &petace::network::NetParams::local_addr)
            .def_readwrite("local_port", &petace::network::NetParams::local_port)
            .def_readwrite("remote_addr", &petace::network::NetParams::remote_addr)
            .def_readwrite("remote_port", &petace::network::NetParams::remote_port)
            .def_readwrite("shared_topic", &petace::network::NetParams::shared_topic)
            .def_readwrite("local_agent", &petace::network::NetParams::local_agent)
            .def_readwrite("remote_party", &petace::network::NetParams::remote_party);

    py::class_<petace::network::Network, std::shared_ptr<petace::network::Network>>(m, "Network")
            .def("send_data",
                    [](petace::network::Network& self, py::buffer b, int size) {
                        py::buffer_info info = b.request();
                        self.send_data(static_cast<void*>(info.ptr), size);
                    })
            .def("recv_data", [](petace::network::Network& self, py::buffer b, int size) {
                py::buffer_info info = b.request();
                self.recv_data(static_cast<void*>(info.ptr), size);
            });

    py::class_<petace::network::NetSocket, std::shared_ptr<petace::network::NetSocket>, petace::network::Network>(
            m, "petace::network::NetSocket");

    py::class_<petace::network::NetFactory, std::unique_ptr<petace::network::NetFactory, py::nodelete>>(m, "NetFactory")
            .def_static("get_instance", &petace::network::NetFactory::get_instance, py::return_value_policy::reference)
            .def("build", &petace::network::NetFactory::build);
}
