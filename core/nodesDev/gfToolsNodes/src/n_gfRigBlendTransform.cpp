#include "../headers/n_gfRigBlendTransform.h"

// Configure a input attribute.
#define INPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(true);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(true);	\
	FNATTR.setKeyable(true);	\

// Configure a output attribute.
#define OUTPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(false);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(false);	\
	FNATTR.setKeyable(false);	\


// Constructor.
BlendTransform::BlendTransform() {}

// Destructor.
BlendTransform::~BlendTransform() {}


MObject BlendTransform::inBlender;
MObject BlendTransform::inRotInterp;
MObject BlendTransform::inTrans1;
MObject BlendTransform::inRot1;
MObject BlendTransform::inSca1;
MObject BlendTransform::inTransform1;
MObject BlendTransform::inTrans2;
MObject BlendTransform::inRot2;
MObject BlendTransform::inSca2;
MObject BlendTransform::inTransform2;
MObject BlendTransform::outTrans;
MObject BlendTransform::outRot;
MObject BlendTransform::outSca;
MObject BlendTransform::outVis;
MObject BlendTransform::outRevVis;



void * BlendTransform::creator() {
	// Maya creator function.
	return new BlendTransform();
}


MStatus BlendTransform::initialize() {
	/*
	Defines the set of attributes for this node. The attributes declared in this function are assigned
	as static members to BlendTransform class. Instances of BlendTransform will use these attributes to create plugs
	for use in the compute() method.
	*/
	MStatus status = MStatus::kFailure;

	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;
	MFnEnumAttribute eAttr;

	inBlender = nAttr.create("blender", "blender", MFnNumericData::kFloat, 0.5f, &status);
	nAttr.setMin(0.0f);
	nAttr.setMax(1.0f);
	INPUT_ATTR(nAttr);

	inRotInterp = eAttr.create("rotationInterpolation", "roti", 0, &status);
	eAttr.addField("Euler Lerp", 0);
	eAttr.addField("Quaternion Slerp", 1);
	INPUT_ATTR(eAttr);

	inTrans1 = nAttr.createPoint("translate1", "t1", &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	static MObject rot1X = uAttr.create("rotate1X", "ro1x", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject rot1Y = uAttr.create("rotate1Y", "ro1y", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject rot1Z = uAttr.create("rotate1Z", "ro1z", MFnUnitAttribute::kAngle, 0.0, &status);
	inRot1 = nAttr.create("rotate1", "ro1", rot1X, rot1Y, rot1Z, &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	inSca1 = nAttr.createPoint("scale1", "sca1", &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	inTransform1 = cAttr.create("transform1", "tr1", &status);
	cAttr.addChild(inTrans1);
	cAttr.addChild(inRot1);
	cAttr.addChild(inSca1);

	inTrans2 = nAttr.createPoint("translate2", "t2", &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	static MObject rot2X = uAttr.create("rotate2X", "ro2x", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject rot2Y = uAttr.create("rotate2Y", "ro2y", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject rot2Z = uAttr.create("rotate2Z", "ro2z", MFnUnitAttribute::kAngle, 0.0, &status);
	inRot2 = nAttr.create("rotate2", "ro2", rot2X, rot2Y, rot2Z, &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	inSca2 = nAttr.createPoint("scale2", "sca2", &status);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	inTransform2 = cAttr.create("transform2", "tr2", &status);
	cAttr.addChild(inTrans2);
	cAttr.addChild(inRot2);
	cAttr.addChild(inSca2);

	outTrans = nAttr.createPoint("outTranslate", "ot", &status);
	nAttr.setArray(true);
	OUTPUT_ATTR(nAttr);

	static MObject oRotX = uAttr.create("outRotateX", "orox", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject oRotY = uAttr.create("outRotateY", "oroy", MFnUnitAttribute::kAngle, 0.0, &status);
	static MObject oRotZ = uAttr.create("outRotateZ", "oroz", MFnUnitAttribute::kAngle, 0.0, &status);
	outRot = nAttr.create("outRotate", "oro", oRotX, oRotY, oRotZ, &status);
	nAttr.setArray(true);
	OUTPUT_ATTR(nAttr);

	outSca = nAttr.createPoint("outScale", "osca", &status);
	nAttr.setArray(true);
	OUTPUT_ATTR(nAttr);

	outVis = nAttr.create("visibility", "vis", MFnNumericData::kBoolean, true, &status);
	OUTPUT_ATTR(nAttr);

	outRevVis = nAttr.create("reverseVisibility", "rvis", MFnNumericData::kBoolean, false, &status);
	OUTPUT_ATTR(nAttr);

	addAttribute(inBlender);
	addAttribute(inRotInterp);
	addAttribute(inTransform1);
	addAttribute(inTransform2);
	addAttribute(outTrans);
	addAttribute(outRot);
	addAttribute(outSca);
	addAttribute(outVis);
	addAttribute(outRevVis);

	attributeAffects(inBlender, outTrans);
	attributeAffects(inTrans1, outTrans);
	attributeAffects(inTrans2, outTrans);
	attributeAffects(inBlender, outRot);
	attributeAffects(inRotInterp, outRot);
	attributeAffects(inRot1, outRot);
	attributeAffects(inRot2, outRot);
	attributeAffects(inBlender, outSca);
	attributeAffects(inSca1, outSca);
	attributeAffects(inSca2, outSca);
	attributeAffects(inBlender, outVis);
	attributeAffects(inBlender, outRevVis);

	return status;
}


MStatus BlendTransform::compute(const MPlug & plug, MDataBlock & dataBlock) {
	/*
	Node computation method:
		* plug is a connection point related to one of our node attributes (either an input or an output).
		* dataBlock contains the data on which we will base our computations.
	*/
	float blender = dataBlock.inputValue(inBlender).asFloat();
	if (plug == outTrans) {
		MArrayDataHandle trans1Handle = dataBlock.inputArrayValue(inTrans1);
		MArrayDataHandle trans2Handle = dataBlock.inputArrayValue(inTrans2);
		MArrayDataHandle outTransHandle = dataBlock.outputArrayValue(outTrans);
		std::vector<MFloatVector> outList;
		uint32_t index = std::min(trans1Handle.elementCount(), trans2Handle.elementCount());
		for (uint32_t i = 0; i < index; i++) {
			trans1Handle.jumpToArrayElement(i);
			trans2Handle.jumpToArrayElement(i);
			MFloatVector vTrans1 = trans1Handle.inputValue().asFloatVector();
			MFloatVector vTrans2 = trans2Handle.inputValue().asFloatVector();
			MFloatVector vOut = (1.0f - blender) * vTrans1 + blender * vTrans2;
			outList.push_back(vOut);
		}
		for (uint32_t i = 0; i < outTransHandle.elementCount(); i++) {
			outTransHandle.jumpToArrayElement(i);
			MDataHandle resultHandle = outTransHandle.outputValue();
			if (i < outTransHandle.elementCount() && i < outList.size()) {
				resultHandle.setMFloatVector(outList[i]);
			}
			else {
				resultHandle.setMFloatVector(MFloatVector());
			}
		}
		outTransHandle.setAllClean();
		return MStatus::kSuccess;
	}

	else if (plug == outRot) {
		short rotInterp = dataBlock.inputValue(inRotInterp).asShort();
		MArrayDataHandle rot1Handle = dataBlock.inputArrayValue(inRot1);
		MArrayDataHandle rot2Handle = dataBlock.inputArrayValue(inRot2);
		MArrayDataHandle outRotHandle = dataBlock.outputArrayValue(outRot);
		double blenderD = (double)blender;
		std::vector<MVector> outList;
		uint32_t index = std::min(rot1Handle.elementCount(), rot2Handle.elementCount());
		for (uint32_t i = 0; i < index; i++) {
			rot1Handle.jumpToArrayElement(i);
			rot2Handle.jumpToArrayElement(i);
			MVector vRot1 = rot1Handle.inputValue().asVector();
			MVector vRot2 = rot2Handle.inputValue().asVector();
			if (rotInterp == 0) {
				MVector vOut = (1.0 - blenderD) * vRot1 + blenderD * vRot2;
				outList.push_back(vOut);
			}
			else {
				MQuaternion qRot1 = MEulerRotation(vRot1).asQuaternion();
				MQuaternion qRot2 = MEulerRotation(vRot2).asQuaternion();
				MVector vOut = slerp(qRot1, qRot2, blenderD).asEulerRotation().asVector();
				outList.push_back(vOut);
			}
		}
		for (uint32_t i = 0; i < outRotHandle.elementCount(); i++) {
			outRotHandle.jumpToArrayElement(i);
			MDataHandle resultHandle = outRotHandle.outputValue();
			if (i < outRotHandle.elementCount() && i < outList.size()) {
				resultHandle.setMVector(outList[i]);
			}
			else {
				resultHandle.setMVector(MVector());
			}
		}
		outRotHandle.setAllClean();
		return MStatus::kSuccess;
	}

	else if (plug == outSca) {
		MArrayDataHandle sca1Handle = dataBlock.inputArrayValue(inSca1);
		MArrayDataHandle sca2Handle = dataBlock.inputArrayValue(inSca2);
		MArrayDataHandle outScaHandle = dataBlock.outputArrayValue(outSca);
		std::vector<MFloatVector> outList;
		uint32_t index = std::min(sca1Handle.elementCount(), sca2Handle.elementCount());
		for (uint32_t i = 0; i < index; i++) {
			sca1Handle.jumpToArrayElement(i);
			sca2Handle.jumpToArrayElement(i);
			MFloatVector vSca1 = sca1Handle.inputValue().asFloatVector();
			MFloatVector vSca2 = sca2Handle.inputValue().asFloatVector();
			MFloatVector vOut = (1.0f - blender) * vSca1 + blender * vSca2;
			outList.push_back(vOut);
		}
		for (uint32_t i = 0; i < outScaHandle.elementCount(); i++) {
			outScaHandle.jumpToArrayElement(i);
			MDataHandle resultHandle = outScaHandle.outputValue();
			if (i < outScaHandle.elementCount() && i < outList.size()) {
				resultHandle.setMFloatVector(outList[i]);
			}
			else {
				resultHandle.setMFloatVector(MFloatVector());
			}
		}
		outScaHandle.setAllClean();
		return MStatus::kSuccess;
	}

	else if (plug == outVis || plug == outRevVis) {
		MDataHandle outVisHandle = dataBlock.outputValue(outVis);
		MDataHandle outRevVisHandle = dataBlock.outputValue(outRevVis);
		VisibilityData data = BlendTransform::visibilityCalculation(blender);
		outVisHandle.setBool(data.visibility);
		outRevVisHandle.setBool(data.reverseVisibility);
		outVisHandle.setClean();
		outRevVisHandle.setClean();
		return MStatus::kSuccess;
	}
	else {
		return MStatus::kUnknownParameter;
	}
}


VisibilityData BlendTransform::visibilityCalculation(float blender) {
	/*
	Calculate the visibility of the objects based on blender value.Threshold can be changed
	in code to affect the calculation.
	*/
	float threshold = 0.1f;
	bool visValue;
	bool revVisValue;
	if (blender <= 0.0f + threshold) {
		visValue = false;
		revVisValue = true;
	}
	else if (blender >= 1.0f - threshold) {
		visValue = true;
		revVisValue = false;
	}
	else {
		visValue = true;
		revVisValue = true;
	}

	return { visValue, revVisValue };
}