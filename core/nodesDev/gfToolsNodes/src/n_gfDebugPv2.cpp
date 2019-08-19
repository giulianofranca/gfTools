#include "../headers/n_gfDebugPv.h"

#define INPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(true);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(true);	\
	FNATTR.setKeyable(true);	\

#define OUTPUT_ATTR(FNATTR)		\
	FNATTR.setWritable(false);	\
	FNATTR.setReadable(true);	\
	FNATTR.setStorable(false);	\
	FNATTR.setKeyable(false);	\



pvDebugNode::pvDebugNode() {}

pvDebugNode::~pvDebugNode() {}


MObject pvDebugNode::inStartPos;
MObject pvDebugNode::inMidPos;
MObject pvDebugNode::inEndPos;
MObject pvDebugNode::outPos;
MObject pvDebugNode::outRot;
MObject pvDebugNode::outRotX;
MObject pvDebugNode::outRotY;
MObject pvDebugNode::outRotZ;
MObject pvDebugNode::outResult;



void* pvDebugNode::creator() {
	return new pvDebugNode();
}


MStatus pvDebugNode::initialize() {
	MStatus status = MStatus::kFailure;

	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;

	inStartPos = nAttr.createPoint("startPos", "sp", &status);
	INPUT_ATTR(nAttr);

	inMidPos = nAttr.createPoint("midPos", "mp", &status);
	INPUT_ATTR(nAttr);

	inEndPos = nAttr.createPoint("endPos", "ep", &status);
	INPUT_ATTR(nAttr);

	outPos = nAttr.createPoint("outPos", "op", &status);
	OUTPUT_ATTR(nAttr);

	outRotX = uAttr.create("outRotX", "orox", MFnUnitAttribute::kAngle, 0.0, &status);
	outRotY = uAttr.create("outRotY", "oroy", MFnUnitAttribute::kAngle, 0.0, &status);
	outRotZ = uAttr.create("outRotZ", "oroz", MFnUnitAttribute::kAngle, 0.0, &status);
	outRot = nAttr.create("outRot", "oro", outRotX, outRotY, outRotZ);
	OUTPUT_ATTR(nAttr);

	outResult = nAttr.createColor("result", "res", &status);
	OUTPUT_ATTR(nAttr);

	addAttribute(inStartPos);
	addAttribute(inMidPos);
	addAttribute(inEndPos);
	addAttribute(outPos);
	addAttribute(outRot);
	addAttribute(outResult);

	attributeAffects(inStartPos, outPos);
	attributeAffects(inMidPos, outPos);
	attributeAffects(inEndPos, outPos);
	attributeAffects(inStartPos, outRot);
	attributeAffects(inMidPos, outRot);
	attributeAffects(inEndPos, outRot);
	attributeAffects(inStartPos, outResult);
	attributeAffects(inMidPos, outResult);
	attributeAffects(inEndPos, outResult);

	return status;
}


LocationData pvDebugNode::retriveLocation(float3& startPos, float3& midPos, float3& endPos){
	MVector vStart = MVector(startPos[0], startPos[1], startPos[2]);
	MVector vMid = MVector(midPos[0], midPos[1], midPos[2]);
	MVector vEnd = MVector(endPos[0], endPos[1], endPos[2]);
	MVector vStartEnd = vEnd - vStart;
	MVector vStartMid = vMid - vStart;
	double dotP = vStartMid * vStartEnd;
	double proj = dotP / vStartEnd.length();
	MVector nStartEnd = vStartEnd.normal();
	MVector vProj = nStartEnd * proj;
	MVector vArrow = vStartMid - vProj;
	vArrow *= 1;  // Multiplier
	MVector vFinal = vArrow + vMid;
	MVector vCross1 = vStartEnd ^ vArrow;
	vCross1.normalize();
	MVector vCross2 = vCross1 ^ vArrow;
	vCross2.normalize();
	vArrow.normalize();
	double matrix[4][4] = { vArrow.x, vArrow.y, vArrow.z, 0.0,
						   vCross1.x, vCross1.y, vCross1.z, 0.0,
						   vCross2.x, vCross2.y, vCross2.z, 0.0,
						   0.0, 0.0, 0.0, 1.0 };
	MMatrix mMatrix = MMatrix(matrix);
	MTransformationMatrix matrixFn = MTransformationMatrix(mMatrix);
	MEulerRotation eRot = matrixFn.eulerRotation();

	return {vFinal, eRot};
}


MFloatVector pvDebugNode::pvLocationRatioColor(float3& startPos, float3& midPos, MVector& pvPos) {
	float startToMidPosDist = std::sqrt(std::pow(startPos[0] - midPos[0], 2) +
										std::pow(startPos[1] - midPos[1], 2) +
										std::pow(startPos[2] - midPos[2], 2));
	float midToPvPosDist = std::sqrt(std::pow(midPos[0] - pvPos.x, 2) +
									 std::pow(midPos[1] - pvPos.y, 2) +
									 std::pow(midPos[2] - pvPos.z, 2));
	float okRatio = startToMidPosDist / 4.f;
	float badRatio = 0.f;
	float okHColor = 240.f;
	float badHColor = 0.f;
	float colorH = pvDebugNode::fit(midToPvPosDist, badRatio, okRatio, badHColor, okHColor);
	float colorHRemaped = pvDebugNode::fit(colorH, 0.f, 360.f, 0.f, 1.f);
	float colorS = 1.f;
	float colorV = 1.f;
	MFloatVector rgb = pvDebugNode::convertHSVtoRGB(colorHRemaped, colorS, colorV);

	return rgb;
}


MFloatVector pvDebugNode::convertHSVtoRGB(float hValue, float sValue, float vValue) {
	float c = vValue * sValue; //Chroma
	float hPrime = std::fmod(hValue / 60.f, 6.f);
	float x = c * (1 - std::fabs(std::fmod(hPrime, 2) - 1));
	float m = vValue - c;
	MFloatVector rgb;
	if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(c, x, 0.f);
	else if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(x, c, 0.f);
	else if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(0.f, c, x);
	else if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(0.f, x, c);
	else if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(x, 0.f, c);
	else if (0.f <= hPrime && hPrime < 1.f)
		rgb = MFloatVector(c, 0.f, x);
	else
		rgb = MFloatVector(0.f, 0.f, 0.f);
	MFloatVector finalColor = MFloatVector(rgb.x + m, rgb.y + m, rgb.z + m);

	return finalColor;
}


float pvDebugNode::fit(float value, float oldMin, float oldMax, float newMin, float newMax) {
	float oldRange = oldMax - oldMin;
	float newRange = newMax - newMin;
	float newValue = (((value - oldMin) * newRange) / oldRange) + newMin;
	if (value >= oldMax)
		newValue = newMax;
	else if (value <= oldMin)
		newValue = newMin;
	
	return newValue;
}


MStatus pvDebugNode::compute(const MPlug & plug, MDataBlock & dataBlock) {
	float3& startPos = dataBlock.inputValue(inStartPos).asFloat3();
	float3& midPos = dataBlock.inputValue(inMidPos).asFloat3();
	float3& endPos = dataBlock.inputValue(inEndPos).asFloat3();

	LocationData data = pvDebugNode::retriveLocation(startPos, midPos, endPos);

	if (plug == outPos) {
		MDataHandle outPosHandle = dataBlock.outputValue(outPos);
		outPosHandle.set3Float(data.translate.x, data.translate.y, data.translate.z);
		outPosHandle.setClean();
	}

	else if (plug == outRot) {
		MDataHandle outRotHandle = dataBlock.outputValue(outRot);
		MDataHandle outRotXHandle = outRotHandle.child(outRotX);
		MDataHandle outRotYHandle = outRotHandle.child(outRotY);
		MDataHandle outRotZHandle = outRotHandle.child(outRotZ);
		outRotXHandle.setMAngle(MAngle(data.rotate.x));
		outRotYHandle.setMAngle(MAngle(data.rotate.y));
		outRotZHandle.setMAngle(MAngle(data.rotate.z));
		outRotHandle.setClean();
	}

	else if (plug == outResult) {
		MFloatVector color = pvDebugNode::pvLocationRatioColor(startPos, midPos, data.translate);
		MDataHandle outColorResult = dataBlock.outputValue(outResult);
		outColorResult.setMFloatVector(color);
		outColorResult.setClean();
	}

	else {
		return MStatus::kUnknownParameter;
	}

	return MStatus::kSuccess;
}