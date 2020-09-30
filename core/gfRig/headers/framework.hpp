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

TODO:
    * Create a method to delete a list of attributes from selection 
        or from list of objects.
    * Learn typedef
    * Learn C++ style casting
*/
#pragma once

#include <string>

#include <gfRig/version.hpp>




// Full namespace example: gfRig::gfTools10000::Types::AtributeTypes::kInt
// Usage of namespace example: gfRig::Types::AttributeTypes::kInt

#define GFTOOLS_MAIN_NAMESPACE gfRig
#define GFTOOLS_TYPES_NAMESPACE Types
#define GFTOOLS_PYTHON_NAMESPACE Python

#define OPEN_GFTOOLS_MAIN_NAMESPACE                                 \
    namespace GFTOOLS_MAIN_NAMESPACE{                               \
        inline namespace GFTOOLS_VERSION_NAMESPACE{

#define OPEN_GFTOOLS_TYPES_NAMESPACE                                \
    namespace GFTOOLS_MAIN_NAMESPACE{                               \
        inline namespace GFTOOLS_VERSION_NAMESPACE{                 \
            namespace GFTOOLS_TYPES_NAMESPACE{

#define OPEN_GFTOOLS_PYTHON_NAMESPACE                               \
    namespace GFTOOLS_MAIN_NAMESPACE{                               \
        inline namespace GFTOOLS_VERSION_NAMESPACE{                 \
            namespace GFTOOLS_PYTHON_NAMESPACE{

#define CLOSE_GFTOOLS_MAIN_NAMESPACE }}
#define CLOSE_GFTOOLS_TYPES_NAMESPACE }}}
#define CLOSE_GFTOOLS_PYTHON_NAMESPACE }}}

// #define USE_GFTOOLS_NAMESPACE_ALIAS                         
//     namespace gfTools = GFTOOLS_MAIN_NAMESPACE::GFTOOLS_VERSION_NAMESPACE;
