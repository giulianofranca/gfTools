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

#include "../headers/utils.hpp"

#include <pybind11/pybind11.h>

namespace py = pybind11;

template <typename... Args>
using overload_cast_ = py::detail::overload_cast_impl<Args...>;



OPEN_GFTOOLS_PYTHON_NAMESPACE

    //===============================================================================
    //  Utils class
    //===============================================================================

    inline void wrapUtilsClass(py::module m){
        py::class_<gfRig::Utils> gfUtils(m, "Utils");
        gfUtils.def(py::init<>())
            .def_static("getPoleVectorPosition",
                overload_cast_<>()(&gfRig::Utils::getPoleVectorPosition),
                "Find the right pole vector position based on selection.")
            .def_static("getPoleVectorPosition",
                overload_cast_<double>()(&gfRig::Utils::getPoleVectorPosition),
                "Find the right pole vector position based on selection "
                "maintaining the distance specified.",
                py::arg("distance"));
    }


CLOSE_GFTOOLS_PYTHON_NAMESPACE
