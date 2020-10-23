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

Todo:
    * In gfTools API MayaUtils class make makeInputAttr() and makeOutputAttr() to use in nodes.

Sources:
    * devkitBase > devkit > plug-ins > geometryOverrideExample1
    * devkitBase > devkit > plug-ins > footPrintNode_GeometryOverride
*/
#pragma once

#include <maya/MPxSurfaceShape.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MPointArray.h>
#include <maya/MColor.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MEvaluationNode.h>
#include <maya/MPlugArray.h>

#include <maya/MPxGeometryOverride.h>
#include <maya/MHWGeometry.h>
#include <maya/MHWGeometryUtilities.h>


class VisualizeVector : public MPxSurfaceShape{
public:
    VisualizeVector();
    ~VisualizeVector() override;

    // Public Override Methods
    bool                isBounded() const override;
    MBoundingBox        boundingBox() const override;
    MSelectionMask      getShapeSelectionMask() const override;
    void                postConstructor() override;
    MStatus             setDependentsDirty(const MPlug& plugBeingDirtied, 
                                           MPlugArray& affectedPlugs) override;
    MStatus             postEvaluation(const MDGContext& context,
                                       const MEvaluationNode& evaluationNode,
                                       PostEvaluationType evalType) override;

    // Public Methods
    bool            getGeometryVP2Update();
    void            setGeometryVP2Update(bool attrChanged);
    void            updateDrawInfo();
    MPointArray&    getVectorPoints();
    bool&           getXRay();
    MColor&         getColor();

    // Public Static Methods
    static MStatus      initialize();
    static void*        creator();

    // Public Members
    const static MString    kNodeName;
    const static MString    kNodeClassify;
    const static MString    kNodeRegistrantID;
    const static MTypeId    kNodeID;

    // Attributes
    static MObject      inColor;
    static MObject      inXRay;
    static MObject      inVector;
    static MObject      inNormalize;
    static MObject      geometryVP2Update;

private:
    // Private Members
    MPointArray     mPoints;
    bool            mXRay;
    MColor          mColor;
};




class VisualizeVectorOverride : public MHWRender::MPxGeometryOverride{
public:
    VisualizeVectorOverride(const MObject& obj);
    ~VisualizeVectorOverride() override;

    // Public Override Methods
    MHWRender::DrawAPI      supportedDrawAPIs() const override;
    void                    updateDG() override;
    void                    updateRenderItems(const MDagPath& path,
                                              MHWRender::MRenderItemList& list) override;
    void                    populateGeometry(const MHWRender::MGeometryRequirements& requirements,
                                             const MHWRender::MRenderItemList& renderItems,
                                             MHWRender::MGeometry& data) override;
    void                    cleanUp() override;
    bool                    isIndexingDirty(const MHWRender::MRenderItem& item) override;
    bool                    isStreamDirty(const MHWRender::MVertexBufferDescriptor& desc) 
                                          override;
    bool                    hasUIDrawables() const override;
    void                    addUIDrawables(const MDagPath& path, MUIDrawManager& drawManager,
                                           const MFrameContext& frameContext) override;
    #if MAYA_API_VERSION >= 20190000
    bool                    requiresGeometryUpdate() const override;
    #endif

    // Public Static Methods
    static MHWRender::MPxGeometryOverride*      creator(const MObject& obj);

private:
    // Private Members
    VisualizeVector*        mShape;
    MObject                 mShapeMob;
};