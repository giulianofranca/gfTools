#include "headers/visualizeVector.hpp"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)      \
    FNATTR.setWritable(true);   \
    FNATTR.setReadable(true);   \
    FNATTR.setStorable(true);   \
    FNATTR.setKeyable(true);    \
    CHECK_MSTATUS_AND_RETURN_IT(status);


// Constructors and Destructors
VisualizeVector::VisualizeVector() {}
VisualizeVector::~VisualizeVector() {}


// Members initialization
MObject VisualizeVector::inColor;
MObject VisualizeVector::inXRay;
MObject VisualizeVector::inVector;
MObject VisualizeVector::inNormalize;

// Use and internal attribute to store if any attribute which affects
// the geometry created by MPxGeometryOverride has changed since the last time
// MPxGeometryOVerride was executed. Storing this information here is breaking our
// abstraction. MPxSurfaceShape hast to know about details of how MPxGeometryOverride
// works that it really shouldn't know. However, attributes are stored in the
// MDataBlock and the MDataBlock is context aware storage, so internal attributes are
// a good way to communicate between the MPxSurfaceShape and the MPxGeometryOverride
// which is safe to use with VP2 Custom Caching.
MObject VisualizeVector::geometryVP2Update;




void* VisualizeVector::creator(){
    return new VisualizeVector();
}

MStatus VisualizeVector::initialize(){
    // Defines the set of attributes for this node. The attributes declared in this 
    // function are assigned as static members to VisualizeVector class. Instances of 
    // VisualizeVector will use these attributes to create plugs for use in the compute()
    // method.
    MStatus status;
    MFnNumericAttribute nAttr;

    inColor = nAttr.createColor("color", "color", &status);
    nAttr.setDefault(1.0, 1.0, 0.0);
    INPUT_ATTR(nAttr);

    inXRay = nAttr.create("xray", "xray", MFnNumericData::kBoolean, false, &status);
    nAttr.setNiceNameOverride("XRay");
    INPUT_ATTR(nAttr);

    inVector = nAttr.createPoint("vector", "vector", &status);
    nAttr.setDefault(1.0, 0.0, 0.0);
    INPUT_ATTR(nAttr);

    inNormalize = nAttr.create("normalize", "norm", MFnNumericData::kBoolean, false, &status);
    INPUT_ATTR(nAttr);

    geometryVP2Update = nAttr.create("geometryVP2Update", "geometryVP2Update",
    MFnNumericData::kBoolean, true);
    nAttr.setStorable(false);
    nAttr.setHidden(true);
    nAttr.setConnectable(false);

    addAttribute(inVector);
    addAttribute(inNormalize);
    addAttribute(inXRay);
    addAttribute(inColor);
    addAttribute(geometryVP2Update);

    return MStatus::kSuccess;
}

void VisualizeVector::postConstructor(){
    // Internally Maya creates two objects when a user defined node is created, the
    // internal MObject and the user derived object. The association between the these
    // two objects is not made until after the MPxNode constructor is called. This
    // implies that no MPxNode member function can be called from the MPxNode
    // constructor. The postConstructor will get called immediately after the
    // constructor when it is safe to call any MPxNode member function.

    // Update the points to properly draw the bounding box for the first time.
    updateDrawInfo();

    // Rename the nodes.
    MObject thisMob = thisMObject();
    MFnDependencyNode nodeFn(thisMob);
    nodeFn.setName("gfVisualizeVectorShape#");
}

MStatus VisualizeVector::setDependentsDirty(const MPlug& plugBeingDirtied,
MPlugArray& affectedPlugs){
    // Use setDependentsDirty to tap into Maya's dirty propagation to track when
    // the size plug changes so that MPxGeometryOverride can find out if it needs
    // to update geometry. Warning: Any time you implement setDependentsDirty you
    // probably also need to implement something similar in preEvaluation() or 
    // postEvaluation() so the code works correctly with Evaluation Manager enabled.
    if (plugBeingDirtied.isChild()){
        if ((plugBeingDirtied.parent().partialName() == "vector") ||
            (plugBeingDirtied.parent().partialName() == "color"))
            setGeometryVP2Update(true);
    }
    else{
        if ((plugBeingDirtied.partialName() == "vector") ||
            (plugBeingDirtied.partialName() == "xray") ||
            (plugBeingDirtied.partialName() == "color") ||
            (plugBeingDirtied.partialName() == "norm"))
            setGeometryVP2Update(true);
    }

    return MStatus::kSuccess;
}

MStatus VisualizeVector::postEvaluation(const MDGContext& context,
const MEvaluationNode& evaluationNode, PostEvaluationType evalType){
    // Use postEvaluation to tap into Evaluation Manager dirty information to track
    // when the attributes changes so that MPxGeometryOverride can find out if it
    // needs to update geometry. Evaluation Caching: It is critical for Evaluation
    // Caching that the EM dirty information is accessed from postEvaluation rather
    // than preEvaluation. During Evaluation Caching restore (or VP2 Custom Caching 
    // restore) preEvaluation will not be called, causing the geometryVP2Update flag
    // to be set incorrectly and preventing VP2 from updating to use the new data
    // restored from the cache. preEvaluation should be used to prepare for the drawing
    // override calls. postEvaluation should be used to notify consumers of the data
    // (VP2) that new data is ready. Warning: Any time you implement preEvaluation or
    // postEvaluation and use dirtyPlugExists you probably also need to implement
    // something similar in setDependentsDirty() so the code works correctly without
    // Evaluation Manager.
    MStatus status;
    if ((evaluationNode.dirtyPlugExists(inVector, &status) && status) ||
        (evaluationNode.dirtyPlugExists(inXRay, &status) && status) ||
        (evaluationNode.dirtyPlugExists(inColor, &status) && status) ||
        (evaluationNode.dirtyPlugExists(inNormalize, &status) && status)){
            setGeometryVP2Update(true);
            return MStatus::kSuccess;
        }
    MPlugArray compoundPlugs;
    compoundPlugs.append(MPlug(thisMObject(), inVector));
    compoundPlugs.append(MPlug(thisMObject(), inColor));
    for (unsigned int i = 0; compoundPlugs.length(); i++){
        MPlug cPlug = compoundPlugs[i];
        for(unsigned int j = 0; cPlug.numChildren(); j++){
            MPlug curChild = cPlug.child(j);
            if (evaluationNode.dirtyPlugExists(curChild.attribute(), &status) && status){
                setGeometryVP2Update(true);
                return MStatus::kSuccess;
            }
        }
    }

    return MStatus::kSuccess;
}

bool VisualizeVector::getGeometryVP2Update(){
    // Calling forceCache here should be fast. Possible calling sites are:
    //  - setDependentsDirty() -> the normal context is current.
    //  - preparing the draw in VP2 -> the normal context is current.
    //  - background evaluation postEvaluation() -> datablock for background context already exists.
    //  - background evaluation for VP2 Custom Caching -> datablock for background context already
    // exists.
    MDataBlock dataBlock = forceCache();
    MDataHandle attrChangedVP2UpdateHandle = dataBlock.outputValue(geometryVP2Update);
    return attrChangedVP2UpdateHandle.asBool();
}

void VisualizeVector::setGeometryVP2Update(bool attrChanged){
    // Calling forceCache here should be fast. Possible calling sites are:
    //  - setDependentsDirty() -> the normal context is current.
    //  - preparing the draw in VP2 -> the normal context is current.
    //  - background evaluation postEvaluation() -> datablock for background context already exists.
    //  - background evaluation for VP2 Custom Caching -> datablock for background context already
    // exists.
    MDataBlock dataBlock = forceCache();
    MDataHandle attrChangedVP2UpdateHandle = dataBlock.outputValue(geometryVP2Update);
    attrChangedVP2UpdateHandle.setBool(attrChanged);
}

bool VisualizeVector::isBounded() const{
    return true;
}

MBoundingBox VisualizeVector::boundingBox() const{
    MBoundingBox bbox;
    for (unsigned int i = 0; i < mPoints.length(); i++){
        bbox.expand(mPoints[i]);
    }

    return bbox;
}

MSelectionMask VisualizeVector::getShapeSelectionMask() const{
    // The selection mask of the shape
    MSelectionMask::SelectionType selType = MSelectionMask::kSelectLocators;
    return MSelectionMask(selType);
}

void VisualizeVector::updateDrawInfo(){
    MObject thisMob = thisMObject();
    bool normalize = MPlug(thisMob, inNormalize).asBool();
    MFloatVector vector = MPlug(thisMob, inVector).asMDataHandle().asFloatVector();
    if (normalize)
        vector.normalize();
    MPoint base(0.0, 0.0, 0.0);
    MPoint tip(vector);
    mPoints.clear();
    mPoints.append(base);
    mPoints.append(tip);
    mXRay = MPlug(thisMob, inXRay).asBool();
    MFloatVector color = MPlug(thisMob, inColor).asMDataHandle().asFloatVector();
    mColor = MColor(color.x, color.y, color.z);
}

MPointArray& VisualizeVector::getVectorPoints(){
    return mPoints;
}

bool& VisualizeVector::getXRay(){
    return mXRay;
}

MColor& VisualizeVector::getColor(){
    return mColor;
}




// Constructors and Destructors
VisualizeVectorOverride::VisualizeVectorOverride(const MObject& obj)
: MHWRender::MPxGeometryOverride(obj), mShape(nullptr), mShapeMob(obj){
    // Get the real mesh object from the MObject
    MStatus status;
    MFnDependencyNode nodeFn(mShapeMob, &status);
    if (status)
        mShape = dynamic_cast<VisualizeVector*>(nodeFn.userNode());
}
VisualizeVectorOverride::~VisualizeVectorOverride() {
    // Delete mShape pointer?
}




MHWRender::MPxGeometryOverride* VisualizeVectorOverride::creator(const MObject&
obj){
    return new VisualizeVectorOverride(obj);
}

MHWRender::DrawAPI VisualizeVectorOverride::supportedDrawAPIs() const{
    return (MHWRender::kOpenGL | MHWRender::kOpenGLCoreProfile | MHWRender::kDirectX11);
}

bool VisualizeVectorOverride::isIndexingDirty(const MHWRender::MRenderItem& item){
    return false;
}

bool VisualizeVectorOverride::isStreamDirty(const MHWRender::MVertexBufferDescriptor& desc){
    return mShape->getGeometryVP2Update();
}

#if MAYA_API_VERSION >= 20190000
bool VisualizeVectorOverride::requiresGeometryUpdate() const{
    return mShape->getGeometryVP2Update();
}
#endif

void VisualizeVectorOverride::updateDG(){
    // Perform any work required to translate the geometry data that needs to get
    // information from the dependency graph. This should be the only place that
    // dependency graph evaluation occurs. Any data retrieved should be cached for
    // later stages.
    if (mShape->getGeometryVP2Update())
        mShape->updateDrawInfo();
}

void VisualizeVectorOverride::updateRenderItems(const MDagPath& path,
MHWRender::MRenderItemList& list){
    // This method is called for each instance of the associated DAG object whenever 
    // the object changes and receive the path to the instance and the current list 
    // of render items associated with that instance. Implementations of this method 
    // may add, remove or modify items in the list. As an alternative this method 
    // can enable or disable items that must be used or not based on some properties.
    // A render item represents a single renderable entity and contain many properties 
    // to let the Viewport 2.0 to know how to render the entity. By example, A render 
    // item contain a name, a type, the geometry primitive type, a set of geometry 
    // buffers and a shader instance.
}

void VisualizeVectorOverride::populateGeometry(const MHWRender::MGeometryRequirements& 
requirements, const MHWRender::MRenderItemList& renderItems,
MHWRender::MGeometry& data){
    // Fill in data and index streams based on the requirements passed in.
    // Associate indexing with the render items passed in.
    mShape->setGeometryVP2Update(false);
}

void VisualizeVectorOverride::cleanUp(){
    // Clean up any cached data stored from the updateDG() phase.
}

bool VisualizeVectorOverride::hasUIDrawables() const{
    // In order for any override for the addUIDrawables() method to be called this
    // method must also be overridden to return true.
    return true;
}

void VisualizeVectorOverride::addUIDrawables(const MDagPath& path, MUIDrawManager&
drawManager, const MFrameContext& frameContext){
    // For each instance of the object, besides the render items updated in
    // updateRenderItems() there is also a render item list for rendering simple UI
    // elements. updateAuxiliaryItems() is called just after updateRenderItems().
    //      [in] path = The path to the instance to update auxiliary items for.
    //      [in] drawManager = The draw manager used to draw simple geometry.
    //      [in] frameContext = Frame level context information.
    MHWRender::DisplayStatus status = MHWRender::MGeometryUtilities::displayStatus(path);
    drawManager.beginDrawable();
    if (mShape->getXRay())
        drawManager.beginDrawInXray();

    if (status == MHWRender::DisplayStatus::kActive)
        drawManager.setColor(MColor(1.0, 1.0, 1.0));
    else if (status == MHWRender::DisplayStatus::kLead)
        drawManager.setColor(MColor(0.263, 1.0, 0.639));
    else if (status == MHWRender::DisplayStatus::kDormant)
        drawManager.setColor(mShape->getColor());
    drawManager.setLineWidth(2);
    drawManager.setPointSize(5);
    MPointArray pnts = MPointArray(mShape->getVectorPoints());
    pnts.remove(1);
    drawManager.mesh(MHWRender::MUIDrawManager::kLines, mShape->getVectorPoints());
    drawManager.mesh(MHWRender::MUIDrawManager::kPoints, pnts);

    if (mShape->getXRay())
        drawManager.endDrawInXray();
    drawManager.endDrawable();
}