#include "../headers/n_gfRigIKVChain.h"

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
IKVChain::IKVChain() {}

// Destructor.
IKVChain::~IKVChain() {}


MObject IKVChain::inRoot;
MObject IKVChain::inHandle;
MObject IKVChain::inUpVector;
MObject IKVChain::inPreferredAngle;
MObject IKVChain::inPvMode;
MObject IKVChain::inTwist;
MObject IKVChain::inRestLength1;
MObject IKVChain::inRestLength2;
MObject IKVChain::inCompressionLimit;
MObject IKVChain::inSoft;
MObject IKVChain::inStretch;
MObject IKVChain::inClampStretch;
MObject IKVChain::inClampValue;
MObject IKVChain::inSquash;
MObject IKVChain::outChain;
MObject IKVChain::outStretchFactor;



void* IKVChain::creator() {
	// Maya creator function.
	return new IKVChain();
}


MStatus IKVChain::initialize() {
	/*
	Defines the set of attributes for this node. The attributes declared in this function are assigned
	as static members to IKVChain class. Instances of BlendTransform will use these attributes to create plugs
	for use in the compute() method.
	*/
	MStatus status = MStatus::kFailure;

	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;
	MFnUnitAttribute uAttr;
	MFnEnumAttribute eAttr;

	inRoot = mAttr.create("root", "root", MFnMatrixAttribute::kDouble, &status);
	INPUT_ATTR(mAttr);

	inHandle = mAttr.create("handle", "handle", MFnMatrixAttribute::kDouble, &status);
	INPUT_ATTR(mAttr);

	inUpVector = mAttr.create("upVector", "upv", MFnMatrixAttribute::kDouble, &status);
	INPUT_ATTR(mAttr);

	inPreferredAngle = uAttr.create("preferredAngle", "pa", MFnUnitAttribute::kAngle, 0.0, &status);
	uAttr.setMin(0.0);
	uAttr.setMax(2.0 * M_PI);
	INPUT_ATTR(uAttr);

	inPvMode = eAttr.create("pvMode", "pvm", 0, &status);
	eAttr.addField("Manual", 0);
	eAttr.addField("Auto", 1);
	INPUT_ATTR(eAttr);

	inTwist = uAttr.create("twist", "tw", MFnUnitAttribute::kAngle, 0.0, &status);
	INPUT_ATTR(uAttr);

	inRestLength1 = nAttr.create("restLength1", "rl1", MFnNumericData::kFloat, 1.0f, &status);
	nAttr.setMin(0.001f);
	INPUT_ATTR(nAttr);

	inRestLength2 = nAttr.create("restLength2", "rl2", MFnNumericData::kFloat, 1.0f, &status);
	nAttr.setMin(0.001f);
	INPUT_ATTR(nAttr);

	inCompressionLimit = nAttr.create("compressionLimit", "mc", MFnNumericData::kFloat, 0.05f, &status);
	nAttr.setMin(0.001f);
	nAttr.setMax(0.4f);
	INPUT_ATTR(nAttr);

	inSoft = nAttr.create("soft", "soft", MFnNumericData::kFloat, 0.0f, &status);
	nAttr.setMin(0.0f);
	nAttr.setSoftMax(0.4f);
	nAttr.setMax(1.0f);
	INPUT_ATTR(nAttr);

	inStretch = nAttr.create("stretch", "st", MFnNumericData::kFloat, 0.0f, &status);
	nAttr.setMin(0.0f);
	nAttr.setMax(1.0f);
	INPUT_ATTR(nAttr);

	inClampStretch = nAttr.create("clampStretch", "cst", MFnNumericData::kFloat, 0.0f, &status);
	nAttr.setMin(0.0f);
	nAttr.setMax(1.0f);
	INPUT_ATTR(nAttr);

	inClampValue = nAttr.create("clampValue", "cstv", MFnNumericData::kFloat, 1.5f, &status);
	nAttr.setMin(1.0f);
	nAttr.setSoftMax(2.0f);
	INPUT_ATTR(nAttr);

	inSquash = nAttr.create("squash", "sq", MFnNumericData::kFloat, 0.0f, &status);
	nAttr.setMin(0.0f);
	nAttr.setMax(1.0f);
	INPUT_ATTR(nAttr);

	outChain = mAttr.create("outChain", "oc", MFnMatrixAttribute::kDouble, &status);
	mAttr.setArray(true);
	OUTPUT_ATTR(mAttr);

	outStretchFactor = nAttr.create("stretchFactor", "sf", MFnNumericData::kFloat, 1.0f, &status);
	OUTPUT_ATTR(nAttr);

	addAttribute(inRoot);
	addAttribute(inHandle);
	addAttribute(inUpVector);
	addAttribute(inPreferredAngle);
	addAttribute(inPvMode);
	addAttribute(inTwist);
	addAttribute(inRestLength1);
	addAttribute(inRestLength2);
	addAttribute(inCompressionLimit);
	addAttribute(inSoft);
	addAttribute(inStretch);
	addAttribute(inClampStretch);
	addAttribute(inClampValue);
	addAttribute(inSquash);
	addAttribute(outChain);
	addAttribute(outStretchFactor);

	attributeAffects(inRoot, outChain);
	attributeAffects(inHandle, outChain);
	attributeAffects(inUpVector, outChain);
	attributeAffects(inPreferredAngle, outChain);
	attributeAffects(inPvMode, outChain);
	attributeAffects(inTwist, outChain);
	attributeAffects(inRestLength1, outChain);
	attributeAffects(inRestLength2, outChain);
	attributeAffects(inCompressionLimit, outChain);
	attributeAffects(inSoft, outChain);
	attributeAffects(inStretch, outChain);
	attributeAffects(inClampStretch, outChain);
	attributeAffects(inClampValue, outChain);
	attributeAffects(inSquash, outChain);
	attributeAffects(inRoot, outStretchFactor);
	attributeAffects(inHandle, outStretchFactor);
	attributeAffects(inUpVector, outStretchFactor);
	attributeAffects(inRestLength1, outStretchFactor);
	attributeAffects(inRestLength2, outStretchFactor);
	attributeAffects(inCompressionLimit, outStretchFactor);
	attributeAffects(inSoft, outStretchFactor);
	attributeAffects(inStretch, outStretchFactor);
	attributeAffects(inClampStretch, outStretchFactor);
	attributeAffects(inClampValue, outStretchFactor);

	return status;
}


MStatus IKVChain::compute(const MPlug & plug, MDataBlock & dataBlock) {
	/*
	Node computation method:
		* plug is a connection point related to one of our node attributes (either an input or an output).
		* dataBlock contains the data on which we will base our computations.
	*/

	// Get basis matrix
	short pvMode = dataBlock.inputValue(inPvMode).asShort();
	MMatrix mRoot = dataBlock.inputValue(inRoot).asMatrix();
	MMatrix mHandle = dataBlock.inputValue(inHandle).asMatrix();
	MMatrix mUpVector = dataBlock.inputValue(inUpVector).asMatrix();
	MAngle prefAngle = dataBlock.inputValue(inPreferredAngle).asAngle().asRadians();
	MAngle twist = dataBlock.inputValue(inTwist).asAngle().asRadians();
	MVector vRoot(mRoot[3]);
	MVector vHandle(mHandle[3]);
	MVector vUpVector(mUpVector[3]);
	MVector vXDirection = vHandle - vRoot;
	double xDist = vXDirection.length();
	MVector nXAxis = vXDirection.normal();
	MVector nYAxis;
	if (pvMode == 0) {
		MVector vUpDirection = vHandle - vRoot;
		MVector vYDirection = vUpDirection - ((vUpDirection * nXAxis) * nXAxis);
		nYAxis = vYDirection.normal();
	}
	else {
		nYAxis = MVector(std::cos(prefAngle.value()), 0.0, std::sin(prefAngle.value()));
	}
	MVector nZAxis = nXAxis ^ nYAxis;
	double basis[4][4] = {
		nXAxis.x, nXAxis.y, nXAxis.z, 0.0,
		nYAxis.x, nYAxis.y, nYAxis.z, 0.0,
		nZAxis.x, nZAxis.y, nZAxis.z, 0.0,
		vRoot.x, vRoot.y, vRoot.z, 1.0
	};
	MMatrix mBasisLocal(basis);
	MMatrix mTwist = MMatrix();
	mTwist[1][1] = std::cos(twist.value());
	mTwist[1][2] = std::sin(twist.value());
	mTwist[2][1] = -std::sin(twist.value());
	mTwist[2][2] = std::cos(twist.value());
	MMatrix mBasis = mTwist * mBasisLocal;

	// Solve Triangle
	float l1 = dataBlock.inputValue(inRestLength1).asFloat();
	float l2 = dataBlock.inputValue(inRestLength2).asFloat();
	float compressionLimit = dataBlock.inputValue(inCompressionLimit).asFloat();
	float softValue = dataBlock.inputValue(inSoft).asFloat();
	float l1m = l1; // Multiply by the single multiplier
	float l2m = l2; // Multiply by the single multiplier
	double chainLength = l1m + l2m;
	double l3rigid = std::max(std::min(xDist, chainLength * 1.0), chainLength * compressionLimit);
	double dc = chainLength;
	double da = (1.0 - softValue) * dc;
	double l3soft;
	double l3;
	if (xDist > da && softValue > 0.0f) {
		double ds = dc - da;
		l3soft = ds * (1.0 - std::pow(M_E, (da - xDist) / ds)) + da;
		l3 = l3soft;
	}
	else {
		l3 = l3rigid;
	}

	// Angle Mesurement
	double betaCos = l1m < 0.0001 ? 0.0 : (std::pow(l1m, 2.0) + std::pow(l3, 2.0) - std::pow(l2m, 2.0)) / (2.0 * l1m * l3);
	double beta = std::acos(betaCos);
	double betaSin = std::sin(beta);
	double gammaCos = l3 < 0.0001 ? 1.0 : (std::pow(l1m, 2.0) + std::pow(l2m, 2.0) - std::pow(l3, 2.0)) / (2.0 * l1m * l2m); // Rever isso!
	double gamma = std::acos(gammaCos);
	double gammaComplement = gamma + beta - M_PI;
	double gammaComplementCos = std::cos(gammaComplement);
	double gammaComplementSin = std::sin(gammaComplement);
	double alpha = M_PI - beta - gamma;
	double alphaCos = std::cos(alpha);
	double alphaSin = std::sin(alpha);

	// Cartoony Features
	float stretch = dataBlock.inputValue(inStretch).asFloat();
	if (stretch > 0.0f) {
		float clampStretch = dataBlock.inputValue(inClampStretch).asFloat();
		float clampStretchValue = dataBlock.inputValue(inClampValue).asFloat();
		float squash = dataBlock.inputValue(inSquash).asFloat();
		float scaleFactor;
		float stretchFactor;
		if (xDist > da && softValue > 0.0f) {
			scaleFactor = xDist / l3soft;
		}
		else {
			scaleFactor = xDist / chainLength;
		}
		if (xDist >= da) {
			float clampFactor = (1.0f - clampStretch) * scaleFactor + clampStretch * std::min(scaleFactor, clampStretchValue);
			stretchFactor = (1.0f - stretch) + stretch * clampFactor;
		}
		else {
			stretchFactor = 1.0f;
		}
	}

	return MStatus::kSuccess;




	//if (plug != outChain) {
	//	return MStatus::kUnknownParameter;
	//}

	//// Get Basis Matrix
	//const MMatrix mRoot = dataBlock.inputValue(inRoot).asMatrix();
	//const MMatrix mHandle = dataBlock.inputValue(inHandle).asMatrix();
	//const MMatrix mUpVector = dataBlock.inputValue(inUpVector).asMatrix();

	//MVector vRoot(mRoot[3]);
	//MVector vHandle(mHandle[3]);
	//MVector vUpVector(mUpVector[3]);

	//MVector vXDirection = vHandle - vRoot;
	//double xDistance = vXDirection.length();
	//MVector nXAxis = vXDirection.normal();
	//MVector vUpDirection = vUpVector - vHandle;
	//MVector vYDirection = ((nXAxis * vUpDirection) * nXAxis) - vUpDirection;
	//MVector nYAxis = vYDirection.normal();
	//MVector nZAxis = nXAxis ^ nYAxis;

	//double matrix[4][4] = { nXAxis.x, nXAxis.y, nXAxis.z, 0.0,
	//					    nYAxis.x, nYAxis.y, nYAxis.z, 0.0,
	//					    nZAxis.x, nZAxis.y, nZAxis.z, 0.0,
	//					    vRoot.x, vRoot.y, vRoot.z, 1.0 };
	//MMatrix mBasis(matrix);

	//// Solve Triangle
	//const double l1 = dataBlock.inputValue(inRestLength1).asDouble();
	//const double l2 = dataBlock.inputValue(inRestLength2).asDouble();
	//const float globalScaleValue = dataBlock.inputValue(inGlobalScale).asFloat();
	//const float softValue = 1.0f - dataBlock.inputValue(inSoft).asFloat();

	//double chainLength = (l1 + l2) * globalScaleValue;
	//double dChain = chainLength;
	//double dA = dChain * softValue;
	//double dSoft = dChain - dA + 0.00001;
	//double l3;
	//if (softValue > 0.0f && dA < xDistance) {
	//	l3 = dSoft * (1.0 - std::pow(M_E, (dA - xDistance) / dSoft)) + dA;
	//}
	//else {
	//	l3 = std::max(std::min(xDistance, chainLength), chainLength * 0.15); // minExtension | maxCompression
	//}

	//// Angle Mesurement
	//double cosBeta = l1 < 0.00001 ? 0.0 :
	//	(std::pow(l1, 2.0) + std::pow(l3, 2.0) - std::pow(l2, 2.0)) / (2.0 * l1 * l3);
	//double beta = std::acos(cosBeta);
	//double sinBeta = std::sin(beta);
	//double cosGamma = l3 < 0.00001 ? 1.0 :
	//	(std::pow(l1, 2.0) + std::pow(l2, 2.0) - std::pow(l3, 2.0)) / (2.0 * l1 * l2);
	//double gamma = std::acos(cosGamma);
	//double sinGamma = std::sin(gamma);
	//double alpha = M_PI - gamma - beta;
	//double cosAlpha = std::cos(alpha);
	//double sinAlpha = std::sin(alpha);

	///*double cosAlpha = (std::pow(l2, 2.0) + std::pow(l3, 2.0) - std::pow(l1, 2.0)) / (2.0 * l2 * l3);
	//double alpha;
	//try {
	//	alpha = std::acos(cosAlpha);
	//}
	//catch (const std::exception& e){
	//	(void)e;
	//	alpha = 0.0;
	//}
	//double sinAlpha = std::sin(alpha);
	//double cosBeta = (std::pow(l1, 2.0) + std::pow(l3, 2.0) - std::pow(l2, 2.0)) / (2.0 * l1 * l3);
	//double beta;
	//try {
	//	beta = std::acos(cosBeta);
	//}
	//catch (const std::exception& e) {
	//	(void)e;
	//	beta = 0.0;
	//}
	//double sinBeta = std::sin(beta);
	//double gamma = M_PI - alpha - beta;
	//double cosGamma = std::cos(gamma);
	//double sinGamma = std::sin(gamma);*/

	//// Output Transforms
	//bool hierarchy = dataBlock.inputValue(inHierarchicalMode).asBool();
	//MArrayDataHandle outChainHdle = dataBlock.outputArrayValue(outChain);
	//uint32_t index = outChainHdle.elementCount();
	//std::vector<MMatrix> srtList;

	//if (hierarchy) {
	//	// First Joint
	//	MMatrix mLocal = MMatrix();
	//	mLocal[0][0] = cosBeta;
	//	mLocal[0][1] = sinBeta;
	//	mLocal[1][0] = -sinBeta;
	//	mLocal[1][1] = cosBeta;
	//	MMatrix mResult = mLocal * mBasis;
	//	srtList.push_back(mResult);

	//	// Second Joint
	//	mLocal = MMatrix();
	//	mLocal[0][0] = std::cos(gamma - M_PI);
	//	mLocal[0][1] = std::sin(gamma - M_PI);
	//	mLocal[1][0] = -std::sin(gamma - M_PI);
	//	mLocal[1][1] = std::cos(gamma - M_PI);
	//	mLocal[3][0] = l1;
	//	srtList.push_back(mLocal);

	//	// Third Joint
	//	mLocal = MMatrix();
	//	mLocal[0][0] = cosAlpha;
	//	mLocal[0][1] = sinAlpha;
	//	mLocal[1][0] = -sinAlpha;
	//	mLocal[1][1] = cosAlpha;
	//	mLocal[3][0] = l2;
	//	srtList.push_back(mLocal);
	//}
	//else {
	//	// First Joint
	//	MMatrix mLocal = MMatrix();
	//	mLocal[0][0] = cosBeta;
	//	mLocal[0][1] = sinBeta;
	//	mLocal[1][0] = -sinBeta;
	//	mLocal[1][1] = cosBeta;
	//	MMatrix mResult = mLocal * mBasis;
	//	srtList.push_back(mResult);

	//	// Second Joint
	//	mLocal = MMatrix();
	//	mLocal[0][0] = std::cos(beta + gamma - M_PI);
	//	mLocal[0][1] = std::sin(beta + gamma - M_PI);
	//	mLocal[1][0] = -std::sin(beta + gamma - M_PI);
	//	mLocal[1][1] = std::cos(beta + gamma - M_PI);
	//	mLocal[3][0] = cosBeta * l1;
	//	mLocal[3][1] = sinBeta * l1;
	//	mResult = mLocal * mBasis;
	//	srtList.push_back(mResult);

	//	// Third Joint
	//	mResult = mHandle;
	//	mResult[3][0] = mBasis[3][0] + mBasis[0][0] * l3;
	//	mResult[3][1] = mBasis[3][1] + mBasis[0][1] * l3;
	//	mResult[3][2] = mBasis[3][2] + mBasis[0][2] * l3;
	//	srtList.push_back(mResult);
	//}

	//for (uint32_t i = 0; i < index; i++) {
	//	outChainHdle.jumpToArrayElement(i);
	//	MDataHandle resultHdle = outChainHdle.outputValue();

	//	if (i < index && i < srtList.size()) {
	//		resultHdle.setMMatrix(srtList[i]);
	//	}
	//	else {
	//		MMatrix id = MMatrix();
	//		resultHdle.setMMatrix(id);
	//	}
	//}

	//outChainHdle.setAllClean();
}