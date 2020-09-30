/*
Copyright 2020 Giuliano Franca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#pragma once

#include "../headers/gfTools.hpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;




OPEN_GFTOOLS_PYTHON_NAMESPACE

inline void wrapGFToolsFuncs(py::module m){
    m.def("version", &gfTools::version,
        "Return the gfTools current version.")
    .def("mayaVersion", &gfTools::mayaVersion,
        "Return the Maya version compatible with this build.")
    .def("platform", &gfTools::platform,
        "Return the platform compatible with this build.");
}

CLOSE_GFTOOLS_PYTHON_NAMESPACE