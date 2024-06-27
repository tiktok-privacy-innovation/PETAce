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

#include "setops_py_psi.h"

#include "nlohmann/json.hpp"

#include "setops/pjc/circuit_psi.h"
#include "setops/psi/ecdh_psi.h"
#include "setops/psi/kkrt_psi.h"

namespace petace {
namespace setops {

std::vector<std::string> psi(const std::vector<std::string>& input, std::size_t party_id, bool obtain_result,
        bool verbose, const std::shared_ptr<petace::network::Network>& net, petace::setops::PSIScheme psi_scheme) {
    std::vector<std::string> output;
    switch (psi_scheme) {
        case petace::setops::PSIScheme::ECDH_PSI: {
            petace::setops::EcdhPSI psi;
            nlohmann::json params;
            params["common"]["is_sender"] = party_id == 0 ? true : false;
            params["common"]["verbose"] = verbose;

            params["ecdh_params"]["obtain_result"] = obtain_result;

            psi.init(net, params);
            psi.process(net, input, output);
            break;
        }
        case petace::setops::PSIScheme::KKRT_PSI: {
            petace::setops::KkrtPSI psi;

            bool other_obtain_result;
            net->send_data(&obtain_result, 1);
            net->recv_data(&other_obtain_result, 1);

            nlohmann::json params;
            params["common"]["verbose"] = verbose;
            params["kkrt_psi_params"]["epsilon"] = 1.27;
            params["kkrt_psi_params"]["fun_num"] = 3;
            if ((obtain_result == true) && (other_obtain_result == false)) {
                params["common"]["is_sender"] = false;
                params["kkrt_psi_params"]["sender_obtain_result"] = false;
            } else if ((obtain_result == false) && (other_obtain_result == true)) {
                params["common"]["is_sender"] = true;
                params["kkrt_psi_params"]["sender_obtain_result"] = false;
            } else if ((obtain_result == true) && (other_obtain_result == true)) {
                params["common"]["is_sender"] = party_id == 0 ? true : false;
                params["kkrt_psi_params"]["sender_obtain_result"] = true;
            } else {
                throw std::invalid_argument("obtain_result: parameter config error");
            }

            psi.init(net, params);
            psi.process(net, input, output);
            break;
        }
        default: {
            throw std::invalid_argument("not support psi scheme type");
        }
    }
    return output;
}

std::vector<std::vector<std::uint64_t>> pjc(const std::vector<std::string>& keys,
        const std::vector<std::vector<std::uint64_t>>& features, std::size_t party_id, bool verbose,
        const std::shared_ptr<petace::network::Network>& net, petace::setops::PJCScheme pjc_scheme) {
    std::vector<std::vector<std::uint64_t>> output;
    switch (pjc_scheme) {
        case petace::setops::PJCScheme::CIRCUIT_PSI: {
            petace::setops::CircuitPSI pjc;
            nlohmann::json params;
            params["common"]["is_sender"] = party_id == 0 ? true : false;
            params["common"]["verbose"] = verbose;
            params["circuit_psi_params"]["epsilon"] = 1.27;
            params["circuit_psi_params"]["fun_num"] = 3;
            params["circuit_psi_params"]["fun_epsilon"] = 1.27;
            params["circuit_psi_params"]["hint_fun_num"] = 3;

            pjc.init(net, params);
            pjc.process(net, keys, features, output);
            break;
        }
        case petace::setops::PJCScheme::VOLE_PSI: {
            throw std::invalid_argument("not support pjc scheme type");
            break;
        }
        default: {
            throw std::invalid_argument("not support pjc scheme type");
        }
    }
    return output;
}

}  // namespace setops
}  // namespace petace
