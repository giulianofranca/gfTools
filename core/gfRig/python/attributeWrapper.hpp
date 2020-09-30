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

#include "../headers/attribute.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

namespace py = pybind11;

template <typename... Args>
using overload_cast_ = py::detail::overload_cast_impl<Args...>;



OPEN_GFTOOLS_PYTHON_NAMESPACE

//===================================================================================
//  AttributeTypes enum class
//===================================================================================

inline void wrapAttributeTypesEnum(py::module m){
    py::enum_<gfRig::Types::AttributeTypes>(m, "AttributeTypes",
    py::arithmetic(), "Enum that classifies all attribute types.")
        .value("kNone", gfRig::Types::AttributeTypes::kNone,
            "None type.")
        .value("kInt", gfRig::Types::AttributeTypes::kInt,
            "Used to create int attribute.")
        .value("kFloat", gfRig::Types::AttributeTypes::kFloat,
            "Docstring to type.")
        .value("kDouble", gfRig::Types::AttributeTypes::kDouble,
            "Docstring to type.")
        .value("kShort", gfRig::Types::AttributeTypes::kShort,
            "Docstring to type.")
        .value("kBool", gfRig::Types::AttributeTypes::kBool,
            "Docstring to type.")
        .value("kAngle", gfRig::Types::AttributeTypes::kAngle,
            "Docstring to type.")
        .value("kDistance", gfRig::Types::AttributeTypes::kDistance,
            "Docstring to type.")
        .value("kTime", gfRig::Types::AttributeTypes::kTime,
            "Docstring to type.")
        .value("kIntVector", gfRig::Types::AttributeTypes::kIntVector,
            "Docstring to type.")
        .value("kFloatVector", gfRig::Types::AttributeTypes::kFloatVector,
            "Docstring to type.")
        .value("kDoubleVector", gfRig::Types::AttributeTypes::kDoubleVector,
            "Docstring to type.")
        .value("kShortVector", gfRig::Types::AttributeTypes::kShortVector,
            "Docstring to type.")
        .value("kAngleVector", gfRig::Types::AttributeTypes::kAngleVector,
            "Docstring to type.")
        .value("kDistanceVector", gfRig::Types::AttributeTypes::kDistanceVector,
            "Docstring to type.")
        .value("kFloatMatrix", gfRig::Types::AttributeTypes::kFloatMatrix,
            "Docstring to type.")
        .value("kDoubleMatrix", gfRig::Types::AttributeTypes::kDoubleMatrix,
            "Docstring to type.")
        .value("kString", gfRig::Types::AttributeTypes::kString,
            "Docstring to type.")
        .value("kEnum", gfRig::Types::AttributeTypes::kEnum,
            "Docstring to type.")
        .value("kMesh", gfRig::Types::AttributeTypes::kMesh,
            "Docstring to type.")
        .value("kNurbsCurve", gfRig::Types::AttributeTypes::kNurbsCurve,
            "Docstring to type.")
        .value("kNurbsSurface", gfRig::Types::AttributeTypes::kNurbsSurface,
            "Docstring to type.")
        .value("kIntArray", gfRig::Types::AttributeTypes::kIntArray,
            "Docstring to type.")
        .value("kDoubleArray", gfRig::Types::AttributeTypes::kDoubleArray,
            "Docstring to type.")
        .value("kPointArray", gfRig::Types::AttributeTypes::kPointArray,
            "Docstring to type.")
        .value("kVectorArray", gfRig::Types::AttributeTypes::kVectorArray,
            "Docstring to type.")
        .value("kStringArray", gfRig::Types::AttributeTypes::kStringArray,
            "Docstring to type.");
}

inline const char* _attributeTypesToString(gfRig::Types::AttributeTypes t){
    switch (t){
    case Types::AttributeTypes::kNone: return "AttributeTypes.kNone";
    case Types::AttributeTypes::kInt: return "AttributeTypes.kInt";
    case Types::AttributeTypes::kFloat: return "AttributeTypes.kFloat";
    case Types::AttributeTypes::kDouble: return "AttributeTypes.kDouble";
    case Types::AttributeTypes::kShort: return "AttributeTypes.kShort";
    case Types::AttributeTypes::kBool: return "AttributeTypes.kBool";
    case Types::AttributeTypes::kAngle: return "AttributeTypes.kAngle";
    case Types::AttributeTypes::kDistance: return "AttributeTypes.kDistance";
    case Types::AttributeTypes::kTime: return "AttributeTypes.kTime";
    case Types::AttributeTypes::kIntVector: return "AttributeTypes.kIntVector";
    case Types::AttributeTypes::kFloatVector: return "AttributeTypes.kFloatVector";
    case Types::AttributeTypes::kDoubleVector: return "AttributeTypes.kDoubleVector";
    case Types::AttributeTypes::kShortVector: return "AttributeTypes.kShortVector";
    case Types::AttributeTypes::kAngleVector: return "AttributeTypes.kAngleVector";
    case Types::AttributeTypes::kDistanceVector: return "AttributeTypes.kDistanceVector";
    case Types::AttributeTypes::kFloatMatrix: return "AttributeTypes.kFloatMatrix";
    case Types::AttributeTypes::kDoubleMatrix: return "AttributeTypes.kDoubleMatrix";
    case Types::AttributeTypes::kString: return "AttributeTypes.kString";
    case Types::AttributeTypes::kEnum: return "AttributeTypes.kEnum";
    case Types::AttributeTypes::kMesh: return "AttributeTypes.kMesh";
    case Types::AttributeTypes::kNurbsCurve: return "AttributeTypes.kNurbsCurve";
    case Types::AttributeTypes::kNurbsSurface: return "AttributeTypes.kNurbsSurface";
    case Types::AttributeTypes::kIntArray: return "AttributeTypes.kIntArray";
    case Types::AttributeTypes::kDoubleArray: return "AttributeTypes.kDoubleArray";
    case Types::AttributeTypes::kPointArray: return "AttributeTypes.kPointArray";
    case Types::AttributeTypes::kVectorArray: return "AttributeTypes.kVectorArray";
    case Types::AttributeTypes::kStringArray: return "AttributeTypes.kStringArray";
    default: return "AttributeTypes.kNone";
    }
}


//===================================================================================
//  Attribute class
//===================================================================================

namespace Attribute{

    //-------------------------------------------------------------------------------
    // Special methods

    inline std::string __repr__(const gfRig::Attribute &obj){
        std::string objName("None");
        if (obj.objectName() != std::string())
            objName = "\"" + obj.objectName() + "\"";
        std::string attrName("None");
        if (obj.attributeName() != std::string())
            attrName = "\"" + obj.attributeName() + "\"";

        std::string result = "gfTools.Attribute(" + objName + ", " + attrName + ", " + 
        gfRig::Python::_attributeTypesToString(obj.attributeType()) + ")";
        return result;
    }

    inline std::string __str__(const gfRig::Attribute &obj){
        return obj.asString();
    }
}

//-----------------------------------------------------------------------------------
//  Actual class wrap

inline void wrapAttributeClass(py::module m){
    py::class_<gfRig::Attribute> gfAttrib(m, "Attribute");
    gfAttrib.def(py::init<>())
        .def(py::init<std::string&>(),
            py::arg("objName"))
        .def(py::init<std::string&, std::string&>(),
            py::arg("objName"), py::arg("attribName"))
        .def(py::self == py::self, py::arg("attribute"))
        .def(py::self != py::self, py::arg("attribute"))
        .def("__repr__", &gfRig::Python::Attribute::__repr__)
        .def("__str__", &gfRig::Python::Attribute::__str__)
        .def("asString", &gfRig::Attribute::asString,
            "Return the attribute object as string.")
        .def("isValid", &gfRig::Attribute::isValid,
            "Check if object and attribute is valid.")
        .def("objectName", &gfRig::Attribute::objectName,
            "Return the object name attatched to this object.")
        .def("setObject",
            overload_cast_<std::string&>()(&gfRig::Attribute::setObject),
            "Set the object by object name.",
            py::arg("objName"))
        .def("attributeName", &gfRig::Attribute::attributeName,
            "Return the attribute name attatched to this object.")
        .def("setAttribute",
            overload_cast_<std::string&>()(&gfRig::Attribute::setAttribute),
            "Set the attribute by name.",
            py::arg("attrName"))
        .def("attributeType", &gfRig::Attribute::attributeType,
            "Return the type of the attribute attatched to this object.")
        .def("attributeCount", &gfRig::Attribute::attributeCount,
            "Return the number of attributes in the object.",
            py::arg("onlyExtraAttrs") = false)
        .def("listAllAttributes", &gfRig::Attribute::listAllAttributes,
            "Return a list containing all the attributes names.")
        .def("listExtraAttributes", &gfRig::Attribute::listExtraAttributes,
            "Return a list containing all the extra attributes names.")
        .def("setNiceName",
            overload_cast_<std::string&>()(&gfRig::Attribute::setNiceName),
            "Change the attribute nice name.",
            py::arg("niceName"))
        .def("resetNiceName", &gfRig::Attribute::resetNiceName,
            "Reset the attribute nice name to default.")
        .def("findAttributeType", &gfRig::Attribute::findAttributeType,
            "Return the attribute type.");
}


CLOSE_GFTOOLS_PYTHON_NAMESPACE

