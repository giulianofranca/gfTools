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



PvDebug::PvDebug(){}

PvDebug::~PvDebug(){}


MObject PvDebug::inStart;
MObject PvDebug::inMid;
MObject PvDebug::inEnd;
MObject PvDebug::inDistMult;
MObject PvDebug::outPos;
MObject PvDebug::outRot;
MObject PvDebug::outRotX;
MObject PvDebug::outRotY;
MObject PvDebug::outRotZ;
MObject PvDebug::outResult;



void* PvDebug::creator() {
	return new PvDebug();
}


MStatus PvDebug::initialize() {
	MStatus status = MStatus::kFailure;

	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;

	inStart = mAttr.create("startMtx", "smtx", MFnMatrixAttribute::kFloat, &status);
	INPUT_ATTR(mAttr);

	inMid = mAttr.create("midMtx", "mmtx", MFnMatrixAttribute::kFloat, &status);
	INPUT_ATTR(mAttr);

	inEnd = mAttr.create("endMtx", "emtx", MFnMatrixAttribute::kFloat, &status);
	INPUT_ATTR(mAttr);

	inDistMult = nAttr.create("distanceMultiplier", "dist", MFnNumericData::kFloat, 1.0f, &status);
	nAttr.setMin(0.00001f);
	nAttr.setSoftMax(4.0f);
	nAttr.setMax(10.0f);
	INPUT_ATTR(nAttr);

	outPos = nAttr.createPoint("outPos", "op", &status);
	OUTPUT_ATTR(nAttr);

	outRotX = uAttr.create("outRotX", "orox", MFnUnitAttribute::kAngle, 0.0, &status);
	outRotY = uAttr.create("outRotY", "oroy", MFnUnitAttribute::kAngle, 0.0, &status);
	outRotZ = uAttr.create("outRotZ", "oroz", MFnUnitAttribute::kAngle, 0.0, &status);
	outRot = nAttr.create("outRot", "oro", outRotX, outRotY, outRotZ);
	OUTPUT_ATTR(nAttr);

	outResult = nAttr.createColor("result", "res", &status);
	nAttr.setUsedAsColor(true);
	OUTPUT_ATTR(nAttr);

	addAttribute(inStart);
	addAttribute(inMid);
	addAttribute(inEnd);
	addAttribute(inDistMult);
	addAttribute(outPos);
	addAttribute(outRot);
	addAttribute(outResult);

	attributeAffects(inStart, outPos);
	attributeAffects(inMid, outPos);
	attributeAffects(inEnd, outPos);
	attributeAffects(inDistMult, outPos);
	attributeAffects(inStart, outRot);
	attributeAffects(inMid, outRot);
	attributeAffects(inEnd, outRot);
	attributeAffects(inDistMult, outRot);
	attributeAffects(inStart, outResult);
	attributeAffects(inMid, outResult);
	attributeAffects(inEnd, outResult);

	return status;
}


LocationData PvDebug::retriveLocation(MFloatVector& startPos, MFloatVector& midPos, MFloatVector& endPos, float dist) {
	MFloatVector vStartEnd = endPos - startPos;
	MFloatVector vStartMid = midPos - startPos;
	float dot = vStartMid * vStartEnd;
	float proj = dot / vStartEnd.length();
	MFloatVector nStartEnd = vStartEnd.normal();
	MFloatVector vProj = nStartEnd * proj;
	MFloatVector vArrow = vStartMid - vProj;
	vArrow *= dist;
	MFloatVector vFinal = vArrow + midPos;
	MFloatVector vCross1 = vStartEnd ^ vArrow;
	vCross1.normalize();
	MFloatVector vCross2 = vCross1 ^ vArrow;
	vCross2.normalize();
	vArrow.normalize();
	double matrix[4][4] = { vArrow.x, vArrow.y, vArrow.z, 0.0f,
							vCross1.x, vCross1.y, vCross1.z, 0.0f,
							vCross2.x, vCross2.y, vCross2.z, 0.0f,
							0.0f, 0.0f, 0.0f, 1.0f };
	MMatrix mMatrix(matrix);
	MTransformationMatrix mtxFn(mMatrix);
	MEulerRotation eRot = mtxFn.eulerRotation();

	return { vFinal, eRot };
}


MFloatVector PvDebug::pvLocationRatioColor(MFloatVector& startPos, MFloatVector& midPos, MFloatVector& pvPos) {
	MFloatVector vStartMidPos = midPos - startPos;
	float startMidDist = vStartMidPos.length();
	MFloatVector vMidPvPos = pvPos - midPos;
	float midPvDist = vMidPvPos.length();

	float okRatio = startMidDist / 4.0f;
	float badRatio = 0.0f;
	float okHColor = 240.0f;
	float badHColor = 0.0f;
	float colorH = PvDebug::fit(midPvDist, badRatio, okRatio, badHColor, okHColor);
	float colorHRemaped = PvDebug::fit(colorH, 0.0f, 360.0f, 0.0f, 1.0f);
	float colorS = 1.0f;
	float colorV = 1.0f;
	MFloatVector rgb = PvDebug::convertHSVtoRGB(colorHRemaped, colorS, colorV);

	return rgb;
}


MFloatVector PvDebug::convertHSVtoRGB(float hValue, float sValue, float vValue) {
	float c = vValue * sValue; //Chroma
	float x = c * (1.0f - std::fabsf(std::fmodf(hValue / 60.0f, 2.0f) - 1.0f));
	float m = vValue - c;
	MFloatVector rgb;
	if (0.0f <= hValue && hValue < 60.0f)
		rgb = MFloatVector(c, x, 0.0f);
	else if (60.0f <= hValue && hValue < 120.0f)
		rgb = MFloatVector(x, c, 0.0f);
	else if (120.0f <= hValue && hValue < 180.0f)
		rgb = MFloatVector(0.0f, c, x);
	else if (180.0f <= hValue && hValue < 240.0f)
		rgb = MFloatVector(0.0f, x, c);
	else if (240.0f <= hValue && hValue < 300.0f)
		rgb = MFloatVector(x, 0.0f, c);
	else if (300.0f <= hValue && hValue < 360.0f)
		rgb = MFloatVector(c, 0.0f, x);
	else
		rgb = MFloatVector(0.0f, 0.0f, 0.0f);

	MFloatVector finalColor(rgb.x + m, rgb.y + m, rgb.z + m);
	
	return finalColor;
}


float PvDebug::fit(float value, float oldMin, float oldMax, float newMin, float newMax) {
	float oldRange = oldMax - oldMin;
	float newRange = newMax - newMin;
	float newValue = (((value - oldMin) * newRange) / oldRange) + newMin;
	if (value >= oldMax)
		newValue = newMax;
	else if (value <= oldMin)
		newValue = newMin;

	return newValue;
}


MStatus PvDebug::compute(const MPlug & plug, MDataBlock & dataBlock) {
	MFloatMatrix mStart = dataBlock.inputValue(inStart).asFloatMatrix();
	MFloatMatrix mMid = dataBlock.inputValue(inMid).asFloatMatrix();
	MFloatMatrix mEnd = dataBlock.inputValue(inEnd).asFloatMatrix();
	float distMult = dataBlock.inputValue(inDistMult).asFloat();

	MFloatVector vStart = mStart[3];
	MFloatVector vMid = mMid[3];
	MFloatVector vEnd = mEnd[3];

	LocationData data = PvDebug::retriveLocation(vStart, vMid, vEnd, distMult);

	if (plug == outPos) {
		MDataHandle outPosHdle = dataBlock.outputValue(outPos);
		outPosHdle.set3Float(data.translate.x, data.translate.y, data.translate.z);
		outPosHdle.setClean();
	}

	else if (plug == outRot) {
		MDataHandle outRotHdle = dataBlock.outputValue(outRot);
		MDataHandle outRotXHdle = outRotHdle.child(outRotX);
		MDataHandle outRotYHdle = outRotHdle.child(outRotY);
		MDataHandle outRotZHdle = outRotHdle.child(outRotZ);
		outRotXHdle.setMAngle(MAngle(data.rotate.x));
		outRotYHdle.setMAngle(MAngle(data.rotate.y));
		outRotZHdle.setMAngle(MAngle(data.rotate.z));
		outRotHdle.setClean();
	}

	else if (plug == outResult) {
		MFloatVector color = PvDebug::pvLocationRatioColor(vStart, vMid, data.translate);
		MDataHandle outResultHdle = dataBlock.outputValue(outResult);
		outResultHdle.setMFloatVector(color);
		outResultHdle.setClean();
	}

	else {
		return MStatus::kUnknownParameter;
	}

	return MStatus::kSuccess;
}