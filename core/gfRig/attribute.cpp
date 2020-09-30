#include "headers/attribute.hpp"




gfRig::Attribute::Attribute()
    : mObjectName(std::string()), mAttribName(std::string()),
      mAttribType(gfRig::Types::AttributeTypes::kNone) {
}




gfRig::Attribute::Attribute(std::string& objName)
    : mObjectName(objName), mAttribName(std::string()),
      mAttribType(gfRig::Types::AttributeTypes::kNone){

    // Check if object is valid
    bool status = this->setObject(objName);
    if (!status){
        MGlobal::displayError("Could not find object. Default constructor called.");
        this->mObjectName = std::string();
    }
}




gfRig::Attribute::Attribute(MString& objName)
    : mObjectName(objName.asChar()), mAttribName(std::string()),
      mAttribType(gfRig::Types::AttributeTypes::kNone){

    // Check if object is valid
    bool status = this->setObject(objName);
    if (!status){
        MGlobal::displayError("Could not find object. Default constructor called.");
        this->mObjectName = std::string();
    }
}




gfRig::Attribute::Attribute(std::string& objName, std::string& attribName)
    : mObjectName(objName), mAttribName(attribName),
      mAttribType(gfRig::Types::AttributeTypes::kNone) {

    // Check if object is valid
    bool status = this->setObject(objName);
    if (!status){
        MGlobal::displayError("Could not find object. Initialized without object.");
        this->mObjectName = std::string();
    }

    // Check if attribute is valid
    status = this->setAttribute(attribName);
    if (!status){
        MGlobal::displayError("Could not find attribute. Initialized without attribute.");
        this->mAttribName = std::string();
    }
}




gfRig::Attribute::Attribute(MString& objName, MString& attribName)
    : mObjectName(objName.asChar()), mAttribName(attribName.asChar()),
      mAttribType(gfRig::Types::AttributeTypes::kNone){

    // Check if object is valid
    bool status = this->setObject(objName);
    if (!status){
        MGlobal::displayError("Could not find object. Initialized without object.");
        this->mObjectName = std::string();
    }

    // Check if attribute is valid
    status = this->setAttribute(attribName);
    if (!status){
        MGlobal::displayError("Could not find attribute. Initialized without attribute.");
        this->mAttribName = std::string();
    }
}




gfRig::Attribute::Attribute(MPlug& attrPlug)
    : mObjectName(std::string()), mAttribName(std::string()),
      mAttribType(gfRig::Types::AttributeTypes::kNone){

    // Check if object is valid
    MFnDependencyNode nodeFn(attrPlug.node());
    MString objName = nodeFn.name();
    bool status = this->setObject(objName);
    if (!status)
        MGlobal::displayError("Could not find object. Initialized without object.");

    // Check if attribute is valid
    status = this->setAttribute(attrPlug);
    if (!status)
        MGlobal::displayError("Coult not find attribute. Initialized without attribute.");
}




gfRig::Attribute::~Attribute () {}




bool gfRig::Attribute::operator==(const Attribute& other) const{
    return this->mObjectName == other.mObjectName && 
        this->mAttribName == other.mAttribName;
}




bool gfRig::Attribute::operator!=(const Attribute& other) const{
    return !(*this == other);
}




const std::string gfRig::Attribute::asString() const{
    std::string result("");
    if (this->isValid())
        result = mObjectName + "." + mAttribName;
    return result;
}




const char* gfRig::Attribute::asChar() const{
    std::string result("");
    if (this->isValid())
        result = mObjectName + "." + mAttribName;
    return result.data();
}




MPlug gfRig::Attribute::asMPlug() const{
    // If the object is not valid return an empy MPlug
    if (!this->isValid())
        return MPlug();

    MObject objMob = this->object();
    MFnDependencyNode nodeFn(objMob);
    MString attrName = MString(this->mAttribName.data());
    MPlug objPlug = nodeFn.findPlug(attrName, false);

    return objPlug;
}




bool gfRig::Attribute::isValid() const {
    // Check if it is any object attatched
    if (this->mObjectName == std::string())
        return false;

    // Check if it is any attribute attatched
    if (this->mAttribName == std::string())
        return false;

    // Check if object exists
    MSelectionList selList;
    MStatus status = selList.add(this->mObjectName.data());
    if (!status)
        // Object does not exists
        return false;

    // Check if attribute exists
    MObject objMob;
    selList.getDependNode(0, objMob);
    MFnDependencyNode nodeFn(objMob);
    MString attrName = MString(this->mAttribName.data());
    MPlug objPlug = nodeFn.findPlug(attrName, false, &status);
    if (!status)
        // Attribute does not exists
        return false;

    return true;
}




MObject gfRig::Attribute::object() const{
    MSelectionList selList;
    MStatus status = selList.add(this->mObjectName.data());
    if (!status)
        return MObject::kNullObj;
    MObject objMob;
    selList.getDependNode(0, objMob);
    return objMob;
}




MObject gfRig::Attribute::attribute() const{
    MObject objMob = this->object();
    if (objMob.isNull())
        return MObject::kNullObj;
    MFnDependencyNode nodeFn(objMob);
    MString attrName = MString(this->mAttribName.data());
    MStatus status;
    MPlug objPlug = nodeFn.findPlug(attrName, false, &status);
    if (!status)
        return MObject::kNullObj;
    return objPlug.attribute();
}




const std::string& gfRig::Attribute::objectName() const{
    return this->mObjectName;
}




bool gfRig::Attribute::setObject(std::string& objName){
    MString mString(objName.data());

    MSelectionList selList;
    MStatus status = selList.add(mString);
    if (!status){
        // Cannot add to MSelectionList, object does not exists or have duplicated name.
        MGlobal::displayError("Object does not exists or have duplicated name.");
        return false;
    }

    MObject objMob;
    std::string name;
    selList.getDependNode(0, objMob);
    if (objMob.hasFn(MFn::Type::kDagNode)){
        MDagPath objPath;
        MDagPath::getAPathTo(objMob, objPath);
        name = std::string(objPath.partialPathName().asChar());
    }
    else{
        MFnDependencyNode nodeFn(objMob);
        name = nodeFn.name().asChar();
    }

    this->mObjectName = name;
    return true;
}




bool gfRig::Attribute::setObject(MString& objName){
    MSelectionList selList;
    MStatus status = selList.add(objName);
    if (!status){
        // Cannot add to MSelectionList, object does not exists or have duplicated name.
        MGlobal::displayError("Object does not exists or have duplicated name.");
        return false;
    }

    MObject objMob;
    std::string name;
    selList.getDependNode(0, objMob);
    if (objMob.hasFn(MFn::Type::kDagNode)){
        MDagPath objPath;
        MDagPath::getAPathTo(objMob, objPath);
        name = std::string(objPath.partialPathName().asChar());
    }
    else{
        MFnDependencyNode nodeFn(objMob);
        name = nodeFn.name().asChar();
    }

    this->mObjectName = name;
    return true;
}




bool gfRig::Attribute::setObject(MDagPath& objPath){
    MObject objMob = objPath.node();
    if (objMob.isNull())
        return false;

    this->mObjectName = std::string(objPath.partialPathName().asChar());
    return true;
}




bool gfRig::Attribute::setObject(MObject& objMob){
    if (objMob.isNull())
        return false;

    std::string name;
    if (objMob.hasFn(MFn::kDagNode)){
        MDagPath objPath;
        MDagPath::getAPathTo(objMob, objPath);
        name = objPath.partialPathName().asChar();
    }
    else{
        MFnDependencyNode nodeFn(objMob);
        name = nodeFn.name().asChar();
    }
    this->mObjectName = name;
    return true;
}




const std::string& gfRig::Attribute::attributeName() const{
    return this->mAttribName;
}




bool gfRig::Attribute::setAttribute(std::string& attrName){
    MString mString(this->mObjectName.data());

    MSelectionList selList;
    MStatus status = selList.add(mString);
    if (!status){
        // Object is not valid
        MGlobal::displayError("Object is not valid. Operation skipped.");
        return false;
    }

    MObject objMob;
    status = selList.getDependNode(0, objMob);
    if (!status){
        // Something strange here
        MGlobal::displayError("Could not set attribute. Operation skipped.");
        return false;
    }

    MFnDependencyNode nodeFn(objMob);
    mString = MString(attrName.data());
    MPlug objPlug = nodeFn.findPlug(mString, false, &status);
    if (!status){
        // MPlug not founded.
        MGlobal::displayError("Attribute not founded.");
        return false;
    }

    MString plugName = objPlug.partialName(false, false, true, false, false, true);
    this->mAttribName = std::string(plugName.asChar());

    // TODO: Find the attribute type
    // TODO: Check if the attribute returned is kNone. Raise error if it is.
    this->mAttribType = this->findAttributeType();

    return true;
}




bool gfRig::Attribute::setAttribute(MString& attrName){
    MSelectionList selList;
    MStatus status = selList.add(attrName);
    if (!status){
        // Object is not valid
        MGlobal::displayError("Object is not valid. Operation skipped.");
        return false;
    }

    MObject objMob;
    status = selList.getDependNode(0, objMob);
    if (!status){
        // Something strange here
        MGlobal::displayError("Could not set attribute. Operation skipped.");
        return false;
    }

    MFnDependencyNode nodeFn(objMob);
    MPlug objPlug = nodeFn.findPlug(attrName, false, &status);
    if (!status){
        // MPlug not founded.
        MGlobal::displayError("Attribute not founded.");
        return false;
    }

    MString plugName = objPlug.partialName(false, false, true, false, false, true);
    this->mAttribName = std::string(plugName.asChar());

    // TODO: Find the attribute type
    // TODO: Check if the attribute returned is kNone. Raise error if it is.
    this->mAttribType = this->findAttributeType();

    return true;
}




bool gfRig::Attribute::setAttribute(MPlug& attrPlug){
    MObject plugMob = attrPlug.node();
    if (plugMob.isNull()){
        // Object is not valid
        MGlobal::displayError("Object is not valid. Operation skipped.");
        return false;
    }
    MStatus status;
    MString plugName = attrPlug.name(&status);
    if (!status){
        // Attribute is not valid
        MGlobal::displayError("Attribute is not valid. Operation skipped.");
        return false;
    }
    MString attrName = attrPlug.partialName(false, false, true, false, false, true);
    this->mAttribName = std::string(attrName.asChar());

    // TODO: Find the attribute type
    // TODO: Check if the attribute returned is kNone. Raise error if it is.
    this->mAttribType = this->findAttributeType();

    return true;
}




const gfRig::Types::AttributeTypes& gfRig::Attribute::attributeType() const{
    return this->mAttribType;
}




uint32_t gfRig::Attribute::attributeCount(bool onlyExtraAttrs=false) const{
    // Get All Attributes
    MObject objMob = this->object();
    MFnDependencyNode nodeFn(objMob);
    uint32_t count = nodeFn.attributeCount();
    if (!onlyExtraAttrs)
        return count;

    // Get extra attributes
    MDagModifier dagMod;
    MStatus status;
    MFnDependencyNode dummyNodeFn;
    MObject dummyObj = dummyNodeFn.create(nodeFn.typeName(), &status);
    if (!status)
        return count;
    dummyNodeFn.setObject(dummyObj);
    uint32_t dummyCount = dummyNodeFn.attributeCount();
    uint32_t userCount = count - dummyCount;
    dagMod.deleteNode(dummyObj);
    dagMod.doIt();

    return userCount;
}




std::vector<std::string> gfRig::Attribute::listAllAttributes() const{
    // Check if it is any object attatched
    if (this->mObjectName == std::string()){
        std::vector<std::string> empty;
        return empty;
    }

    // Check if object exists
    MSelectionList selList;
    MStatus status = selList.add(this->mObjectName.data());
    if (!status){
        std::vector<std::string> empty;
        return empty;
    }

    uint32_t count = this->attributeCount();
    MFnDependencyNode nodeFn(this->object());
    std::vector<std::string> attrList;
    attrList.reserve(count);
    MObject attrMob;
    MPlug attrPlug;
    MString attrName;
    for (uint32_t i = 0; i < count; i++){
        attrMob = nodeFn.attribute(i);
        attrPlug = MPlug(nodeFn.object(), attrMob);
        attrName = attrPlug.partialName(false, false, true, false, false, true);
        attrList.emplace_back(attrName.asChar());
    }

    return attrList;
}




std::vector<std::string> gfRig::Attribute::listExtraAttributes() const{
    // Check if it is any object attatched
    if (this->mObjectName == std::string()){
        std::vector<std::string> empty;
        return empty;
    }

    // Check if object exists
    MSelectionList selList;
    MStatus status = selList.add(this->mObjectName.data());
    if (!status){
        std::vector<std::string> empty;
        return empty;
    }

    // Get attribute count
    MObject objMob = this->object();
    MFnDependencyNode nodeFn(objMob);
    uint32_t count = nodeFn.attributeCount();

    // Get extra attributes
    MDagModifier dagMod;
    MFnDependencyNode dummyNodeFn;
    MObject dummyObj = dummyNodeFn.create(nodeFn.typeName(), &status);
    dummyNodeFn.setObject(dummyObj);
    uint32_t dummyCount = dummyNodeFn.attributeCount();

    std::vector<std::string> attrList;
    attrList.reserve(count - dummyCount);
    MObject attrMob;
    MPlug attrPlug;
    MString attrName;
    for (uint32_t i = dummyCount; i < count; i++){
        attrMob = nodeFn.attribute(i, &status);
        attrPlug = MPlug(objMob, attrMob);
        attrName = attrPlug.partialName(false, false, true, false, false, true);
        attrList.emplace_back(attrName.asChar());
    }
    dagMod.deleteNode(dummyObj);
    dagMod.doIt();

    return attrList;
}




bool gfRig::Attribute::setNiceName(std::string& niceName){
    // FIX (M2019): After changing the nice name the UI has to update to take effects.
    if (!this->isValid())
        return false;
    if (niceName == std::string(""))
        return false;

    MPlug attrPlug = this->asMPlug();
    MObject attrMob = attrPlug.attribute();
    MFnAttribute attrFn(attrMob);
    MString newNiceName(niceName.data());
    MStatus status = attrFn.setNiceNameOverride(newNiceName);
    if (status)
        return true;
    return false;
}




bool gfRig::Attribute::setNiceName(MString& name){
    // FIX (M2019): After changing the nice name the UI has to update to take effects.
    if (!this->isValid())
        return false;
    if (name == MString(""))
        return false;

    MPlug attrPlug = this->asMPlug();
    MObject attrMob = attrPlug.attribute();
    MFnAttribute attrFn(attrMob);
    MStatus status = attrFn.setNiceNameOverride(name);
    if (status)
        return true;
    return false;
}




bool gfRig::Attribute::resetNiceName(){
    if (!this->isValid())
        return false;

    std::string name(this->mAttribName);
    std::regex camelCaseReg("([a-zA-Z0-9][a-z]+)|([A-Z]+)|([0-9]+)");
    std::vector<std::string> names(
        std::sregex_token_iterator(name.begin(), name.end(), camelCaseReg),
        std::sregex_token_iterator());
    std::string newName;
    for (uint32_t i = 0; i < names.size(); i++){
        newName += names[i];
        if (i < names.size() - 1)
            newName += " ";
    }
    newName[0] = std::toupper(name[0]);
    bool result = this->setNiceName(newName);
    return result;
}




gfRig::Types::AttributeTypes gfRig::Attribute::findAttributeType(){
    // TODO: Change this method to be private
    // TODO: Fix WorldMatrix attribute returning kTypedAttribute
    // TODO: Find a way to differentiate float matrix to double matrix

    if (!this->isValid())
        return Types::AttributeTypes::kNone;

    MPlug attrPlug = this->asMPlug();
    MObject attrMob = attrPlug.attribute();

    std::vector<MFn::Type> typesList{
        MFn::kNumericAttribute, MFn::kUnitAttribute, MFn::kEnumAttribute,
        MFn::kTimeAttribute, MFn::kTypedAttribute, MFn::kCompoundAttribute,
        MFn::kMatrixAttribute, MFn::kFloatMatrixAttribute, MFn::kMessageAttribute
    };

    MFn::Type attrType;
    uint32_t i;
    for(i = 0; i < typesList.size(); i++){
        if (attrMob.hasFn(typesList[i])){
            attrType = typesList[i];
            break;
        }
    }

    {
        MString toPrint;
        if (attrType){
            toPrint = "Found attribute type: ";
            toPrint += attrType;
        }
        else{
            toPrint = "Could not find the attribute type: ";
            toPrint += attrType;
        }
        MGlobal::displayInfo(toPrint);
    }

    MStatus status;
    // -------------------------------
    // Numeric types

    if (attrType == MFn::kNumericAttribute){
        MFnNumericAttribute fnAttr(attrMob);
        MFnNumericData::Type realType = fnAttr.unitType(&status);
        if (!status)
            return Types::AttributeTypes::kNone;
        
        if (attrPlug.isCompound()){
            // Vector Types
            // Fix this to return the vector type of the childrens
            switch (realType){
            case MFnNumericData::k2Int: case MFnNumericData::k3Int:
                return Types::AttributeTypes::kIntVector;
            case MFnNumericData::k2Float: case MFnNumericData::k3Float:
                return Types::AttributeTypes::kFloatVector;
            case MFnNumericData::k2Double: case MFnNumericData::k3Double:
            case MFnNumericData::k4Double:
                return Types::AttributeTypes::kDoubleVector;
            case MFnNumericData::k2Short : case MFnNumericData::k3Short:
                return Types::AttributeTypes::kShortVector;
            default:
                return Types::AttributeTypes::kNone;
            }
        }
        switch (realType){
        case MFnNumericData::kInt:
            return Types::AttributeTypes::kInt;
        case MFnNumericData::kFloat:
            return Types::AttributeTypes::kFloat;
        case MFnNumericData::kDouble:
            return Types::AttributeTypes::kDouble;
        case MFnNumericData::kShort:
            return Types::AttributeTypes::kShort;
        case MFnNumericData::kBoolean:
            return Types::AttributeTypes::kBool;
        default:
            return Types::AttributeTypes::kNone;
        }
    }
    // -------------------------------
    // Unit types

    else if(attrType == MFn::kUnitAttribute){
        MFnUnitAttribute fnAttr(attrMob);
        MFnUnitAttribute::Type realType = fnAttr.unitType(&status);
        if (!status)
            return Types::AttributeTypes::kNone;

        switch (realType){
        case MFnUnitAttribute::kAngle:
            return Types::AttributeTypes::kAngle;
        case MFnUnitAttribute::kDistance:
            return Types::AttributeTypes::kDistance;
        case MFnUnitAttribute::kTime:
            return Types::AttributeTypes::kTime;
        default:
            return Types::AttributeTypes::kNone;
        }
    }
    // -------------------------------
    // Enum types

    else if (attrType == MFn::kEnumAttribute){
        return Types::AttributeTypes::kEnum;
    }

    // -------------------------------
    // Typed types

    else if (attrType == MFn::kTypedAttribute){
        MFnTypedAttribute fnAttr(attrMob);
        MFnData::Type realType = fnAttr.attrType(&status);
        if (!status)
            return Types::AttributeTypes::kNone;

        if (attrPlug.isCompound())
            MGlobal::displayInfo("Is compound");

        if (attrPlug.isArray())
            MGlobal::displayInfo("Is array");

        switch (realType){
        case MFnData::Type::kMatrix:
            MGlobal::displayInfo("MFnData::Type::kMatrix");
            return Types::AttributeTypes::kNone;
        default:
            return Types::AttributeTypes::kNone;
        }
    }
    return Types::AttributeTypes::kNone;
}