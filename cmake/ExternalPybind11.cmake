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

FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.11.1
)
FetchContent_GetProperties(pybind11)

if(NOT pybind11_POPULATED)
    FetchContent_Populate(pybind11)

    mark_as_advanced(FETCHCONTENT_SOURCE_DIR_PYBIND11)
    mark_as_advanced(FETCHCONTENT_UPDATES_DISCONNECTED_PYBIND11)

    add_subdirectory(
        ${pybind11_SOURCE_DIR}
        ${THIRDPARTY_BINARY_DIR}/pybind11-build
        EXCLUDE_FROM_ALL)
endif()
