# Copyright 2020 Giuliano Franca
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
#
set(GFTOOLS_MAJOR_VERSION "1")
set(GFTOOLS_MINOR_VERSION "0")
set(GFTOOLS_PATCH_VERSION "0")
set(GFTOOLS_STR_VERSION "1.0.0-alpha")
math(EXPR GFTOOLS_VERSION "${GFTOOLS_MAJOR_VERSION} * 10000 + 
    ${GFTOOLS_MINOR_VERSION} * 100 + ${GFTOOLS_PATCH_VERSION}")
set(GFTOOLS_MAYA_VERSIONS_COMPATIBLE "2018" "2019" "2020")
