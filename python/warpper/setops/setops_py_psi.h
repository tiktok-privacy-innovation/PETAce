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

#include <string>
#include <vector>

#include "setops/pjc/pjc.h"
#include "setops/psi/psi.h"

namespace petace {
namespace setops {

/**
 * @brief PSI python api warpper.
 *
 * Both parties input their sets and get the intersection of their sets.
 *
 * @param[in] input The set of each party.
 * @param[in] party_id The party id of the set owner.
 * @param[in] obtain_result True if this party needs to get result.
 * @param[in] verbose True when needs to print log.
 * @param[in] net The network interface (e.g., PETAce-Network interface).
 * @param[in] psi_scheme The psi scheme type.
 * @return The intersection.
 */
std::vector<std::string> psi(const std::vector<std::string>& input, std::size_t party_id, bool obtain_result,
        bool verbose, const std::shared_ptr<petace::network::Network>& net, petace::setops::PSIScheme psi_scheme);

/**
 * @brief PJC python api warpper.
 *
 * Both parties input their sets and get secert share of the intersection of
 * their sets.
 *
 * @param[in] keys The master key.
 * @param[in] features The features corresponding to keys.
 * @param[in] party_id The party id of the set owner.
 * @param[in] verbose True when needs to print log.
 * @param[in] net The network interface (e.g., PETAce-Network interface).
 * @param[in] pjc_scheme The pjc scheme type.
 * @return The intersection.
 */
std::vector<std::vector<std::uint64_t>> pjc(const std::vector<std::string>& keys,
        const std::vector<std::vector<std::uint64_t>>& features, std::size_t party_id, bool verbose,
        const std::shared_ptr<petace::network::Network>& net, petace::setops::PJCScheme pjc_scheme);

}  // namespace setops
}  // namespace petace
