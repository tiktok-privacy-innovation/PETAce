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

from petace.duet.vm import VM


class GlobalVm:
    vm = None


GLOBALVM = GlobalVm()


def set_vm(vm: VM):
    GLOBALVM.vm = vm


def get_vm() -> VM:
    if GLOBALVM.vm is None:
        raise RuntimeError("Global VM is not initialized")
    return GLOBALVM.vm
