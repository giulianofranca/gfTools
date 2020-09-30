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

#include <string>

#include <maya/MSelectionList.h>
#include <maya/MGlobal.h>
#include <maya/MDagPath.h>
#include <maya/MFnTransform.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MDagModifier.h>
#include <maya/MString.h>

#include "framework.hpp"



OPEN_GFTOOLS_MAIN_NAMESPACE

class Utils{
    public:
        Utils();
        ~Utils();

        // Find the right pole vector position based on selection.
        static const std::string                getPoleVectorPosition();
        static const std::string                getPoleVectorPosition(double distance);
};

CLOSE_GFTOOLS_MAIN_NAMESPACE