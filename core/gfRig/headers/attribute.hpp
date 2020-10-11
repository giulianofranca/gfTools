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

* \author Giuliano Franca
* \version 1.0.0-alpha
* \date 2020-10-09
* \bug when clicking on the X in the corner the application does not terminate correctly.
* \warning improper use of this code may void your car's warranty
* \copyright GNU Public License
* \mainpage The teensy LED controller
* \section intro_sec Introduction
* This code was developed to torture students.
* \section compile_sec Compilation
* Here I would describe how to compile this code with cmake and make.
* \subsection Step 1 - CMake
* How to use cmake
* \subsection Step 2 - Make
* How to use make

TODO:
    * Create a method to delete a list of attributes from selection 
        or from list of objects.
    * Learn typedef
    * Learn C++ style casting
    * attributeList.hpp
    * character.hpp
    * color.hpp
    * colorCoding.hpp
    * component.hpp
    * compoundAttribute.hpp
    * enumAttribute.hpp
    * geometry.hpp
    * matrixAttribute.hpp
    * messageAttribute.hpp
    * namingConvention.hpp
    * numericAttribute.hpp
    * objectAttribute.hpp
    * space.hpp
    * stringAttribute.hpp
    * tag.hpp
    * vectorAttribute.hpp
    * vertexList.hpp
*/
#pragma once

#include <string>
#include <iostream>
#include <vector>
#include <cstdint>
#include <regex>
#include <cctype>

#include <maya/MGlobal.h>
#include <maya/MString.h>
#include <maya/MStringArray.h>
#include <maya/MDagPath.h>
#include <maya/MDagModifier.h>
#include <maya/MSelectionList.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MPlug.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include "framework.hpp"




OPEN_GFTOOLS_TYPES_NAMESPACE

//! \todo: Learn how to deal with vector and array attributes
//! \todo: Add vector of units
//! \todo: Recognize vector types looking at child's types.
//! \todo: Fix AttributeTypes in Python not working with int numbers

enum class AttributeTypes{
    kNone = 0,                  //!< No attribute attatched
    kInt = 1,                   //!< Numeric attribute
    kFloat = 2,                 //!< Numeric attribute
    kDouble = 3,                //!< Numeric attribute
    kShort = 4,                 //!< Numeric attribute
    kBool = 5,                  //!< Numeric attribute
    kAngle = 6,                 //!< Numeric attribute
    kDistance = 7,              //!< Numeric attribute
    kTime = 8,                  //!< Numeric attribute
    kIntVector = 9,             //!< Vector attribute
    kFloatVector = 10,          //!< Vector attribute
    kDoubleVector = 11,         //!< Vector attribute
    kShortVector = 12,          //!< Vector attribute
    kAngleVector = 13,          //!< Vector attribute
    kDistanceVector = 14,       //!< Vector attribute
    kFloatMatrix = 15,          //!< Matrix attribute
    kDoubleMatrix = 16,         //!< Matrix attribute
    kString = 17,               //!< String attribute
    kEnum = 18,                 //!< Enum Attribute
    kMesh = 19,                 //!< Object attribute
    kNurbsCurve = 20,           //!< Object attribute
    kNurbsSurface = 21,         //!< Object attribute
    kIntArray = 22,             //!< Array attribute
    kDoubleArray = 23,          //!< Array attribute
    kPointArray = 24,           //!< Array attribute
    kVectorArray = 25,          //!< Array attribute
    kStringArray = 26           //!< Array attribute
};


CLOSE_GFTOOLS_TYPES_NAMESPACE

OPEN_GFTOOLS_MAIN_NAMESPACE




//! \todo: deleteAttribute()
//! \todo: equal operator
//! \todo: loadAttribute(attrName) - Return a specified typed attribute class instance
//! \todo: Move attributes in channel box (upper and lower)
//! \todo: Review std::string reference and copies for Attribute class members.
//! \todo: Check if this attribute is the same type of another.
//! \todo: Create separator attributes (static)
//! \todo: In child classes: setAttr value function()
//! \todo: transferAttributes()
//! \todo: Add constructor that use MPlug
//! \todo: Add copy constructor
//! \todo: Convert Attribute class to Typed Attribute class (e.g.: asNumericAttribute())
//! \todo: Create AttributeList class
//! \todo: Convert listAllAttributes() and listExtraAttributes() to return AttributeList class
//! \todo: Fix display errors and return bool at the same time
//! \todo: static findMFnType()
//! \todo: setAttribute(MObject) overload
//! \todo: Add = operator to child classes
//! \todo: Change objectName and attributeName to properties

//! \brief A vector math class for vectors of doubles.
/*!
This class provides access to Maya's internal vector math library allowing
vectors to be handled easily, and in a manner compatible with internal
Maya data structures.

All methods that query the vector are threadsafe, all methods that
modify the vector are not threadsafe.
    \param[in] src the vector object to copy
    \see Nothing here
    \note A little note
    \attention A little more important than a note
*/
/// ## Example
/// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.cpp
/// MyClass* a = new MyClass();     // A comment
/// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/*! \details For this function to work, the widget class must have pointer for all
* widgets that we want to modify from the core.
*/


class Attribute{
    public:
        Attribute();
        /*!
            Class constructor.  Initializes the vector with the
            explicit x, y and z values provided as arguments.

            \param[in] xx the x component of the vector
            \param[in] yy the y component of the vector
            \param[in] zz the z component of the vector.  Defaults to 0.0.
            \return Bool True of the vectors are equivalent and false otherwise.
        */
        Attribute(std::string& objName);
        Attribute(MString& objName);
        Attribute(std::string& objName, std::string& attribName);
        Attribute(MString& objName, MString& attribName);
        Attribute(MPlug& attrPlug);
        /*!
            Class destructor.
        */
        virtual ~Attribute();

        /*!
            The assignment operator.  Allows assignment between MVectors.

            \param[in] src Vector to copy from.
        */
        virtual bool                                operator==(const Attribute& other) const;
        virtual bool                                operator!=(const Attribute& other) const;
        // return !(*this == other)

        virtual const std::string                   asString() const;
        virtual const char*                         asChar() const;
        virtual MPlug                               asMPlug() const;

        virtual bool                                isValid() const;
        virtual MObject                             object() const;
        virtual MObject                             attribute() const;

        virtual const std::string&                  objectName() const;
        virtual bool                                setObject(std::string& objName);
        virtual bool                                setObject(MString& objName);
        virtual bool                                setObject(MDagPath& objPath);
        virtual bool                                setObject(MObject& objMob);

        virtual const std::string&                  attributeName() const;
        virtual bool                                setAttribute(std::string& attrName);
        virtual bool                                setAttribute(MString& attrName);
        virtual bool                                setAttribute(MPlug& attrPlug);
        virtual const Types::AttributeTypes&        attributeType() const;
        virtual u_int32_t                           attributeCount(bool onlyExtraAttrs) const;

        virtual std::vector<std::string>            listAllAttributes() const;
        virtual std::vector<std::string>            listExtraAttributes() const;

        virtual bool                                setNiceName(std::string& niceName);
        virtual bool                                setNiceName(MString& niceName);
        virtual bool                                resetNiceName();

        Types::AttributeTypes                       findAttributeType();
        // virtual MFn::Type                           getMFnType() const;
        // virtual uint32_t                            getMFnTypeStr() const;
        // virtual bool                            renameAttribute(const std::string& name,
                                                                // const std::string& niceName);

        // void*                                   changeAttributeType(gf::types::AttributeTypes type);

        // static auto                             createFromType(const std::string& name,
                                                            //    const std::string& niceName,
                                                            //    gf::types::AttributeTypes type);


    protected:
        std::string                                 mObjectName;
        std::string                                 mAttribName;
        Types::AttributeTypes                       mAttribType;
};


CLOSE_GFTOOLS_MAIN_NAMESPACE