#include "../headers/n_gfRigPSD.h"

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



SphericalPSD::SphericalPSD() {}

SphericalPSD::~SphericalPSD() {}


MObject SphericalPSD::inBase;
MObject SphericalPSD::inPose;
MObject SphericalPSD::inTarget;
MObject SphericalPSD::inTargetEnvelope;
MObject SphericalPSD::inTargetFalloff;
MObject SphericalPSD::outWeight;


void * SphericalPSD::creator() {
	return new SphericalPSD();
}


MStatus SphericalPSD::initialize() {
	MStatus status = MStatus::kFailure;

	MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;

	inBase = mAttr.create("baseMtx", "bmtx", MFnMatrixAttribute::kDouble, &status);
	INPUT_ATTR(mAttr);

	inPose = mAttr.create("poseMtx", "pmtx", MFnMatrixAttribute::kDouble, &status);
	INPUT_ATTR(mAttr);

	inTarget = mAttr.create("targetMtx", "tmtx", MFnMatrixAttribute::kDouble, &status);
	mAttr.setArray(true);
	INPUT_ATTR(mAttr);

	inTargetEnvelope = nAttr.create("targetEnvelope", "te", MFnNumericData::kDouble, 1.0, &status);
	nAttr.setMin(0.0);
	nAttr.setMax(1.0);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	inTargetFalloff = nAttr.create("targetFalloff", "tf", MFnNumericData::kDouble, 45.0, &status);
	nAttr.setMin(0.0);
	nAttr.setSoftMax(135.0);
	nAttr.setMax(180.0);
	nAttr.setArray(true);
	INPUT_ATTR(nAttr);

	outWeight = nAttr.create("outWeights", "ow", MFnNumericData::kDouble, 0.0, &status);
	nAttr.setMin(0.0);
	nAttr.setMax(1.0);
	nAttr.setArray(true);
	OUTPUT_ATTR(nAttr);

	addAttribute(inBase);
	addAttribute(inPose);
	addAttribute(inTarget);
	addAttribute(inTargetEnvelope);
	addAttribute(inTargetFalloff);
	addAttribute(outWeight);

	attributeAffects(inBase, outWeight);
	attributeAffects(inPose, outWeight);
	attributeAffects(inTarget, outWeight);
	attributeAffects(inTargetEnvelope, outWeight);
	attributeAffects(inTargetFalloff, outWeight);

	return status;
}


MStatus SphericalPSD::compute(const MPlug & plug, MDataBlock & dataBlock) {
	if (plug != outWeight) {
		return MStatus::kUnknownParameter;
	}

	MMatrix baseMtx = dataBlock.inputValue(inBase).asMatrix();
	MMatrix poseMtx = dataBlock.inputValue(inPose).asMatrix();
	MArrayDataHandle targetHandle = dataBlock.inputArrayValue(inTarget);
	MArrayDataHandle envelopeHandle = dataBlock.inputArrayValue(inTargetEnvelope);
	MArrayDataHandle falloffHandle = dataBlock.inputArrayValue(inTargetFalloff);
	MArrayDataHandle weightsHandle = dataBlock.outputArrayValue(outWeight);

	MTransformationMatrix mtxFn(baseMtx);
	MVector vBase = mtxFn.translation(MSpace::kWorld);
	mtxFn = MTransformationMatrix(poseMtx);
	MVector vPose = mtxFn.translation(MSpace::kWorld);

	MVector vCurPose = vPose - vBase;
	MVector nCurPose = vCurPose.normal();

	std::vector<MVector> targetPoseList;
	std::vector<double> envelopeList;
	std::vector<double> falloffList;

	uint32_t index = targetHandle.elementCount();
	for (uint32_t i = 0; i < index; i++) {
		targetHandle.jumpToArrayElement(i);
		MMatrix mtx(targetHandle.inputValue().asMatrix());
		mtxFn = MTransformationMatrix(mtx);
		MVector vector(mtxFn.translation(MSpace::kWorld));
		MVector vTargetPose = vector - vBase;
		MVector nTargetPose = vTargetPose.normal();
		targetPoseList.push_back(nTargetPose);
	}

	index = envelopeHandle.elementCount();
	for (uint32_t i = 0; i < index; i++) {
		envelopeHandle.jumpToArrayElement(i);
		double env = envelopeHandle.inputValue().asDouble();
		envelopeList.push_back(env);
	}

	index = falloffHandle.elementCount();
	for (uint32_t i = 0; i < index; i++) {
		falloffHandle.jumpToArrayElement(i);
		double falloff = falloffHandle.inputValue().asDouble() * M_PI / 180.0;
		falloffList.push_back(falloff);
	}

	for (uint32_t i = 0; i < weightsHandle.elementCount(); i++) {
		weightsHandle.jumpToArrayElement(i);
		MDataHandle resultHandle = weightsHandle.outputValue();

		if ((i < weightsHandle.elementCount()) &&
			(i < targetPoseList.size()) &&
			(i < falloffList.size()) &&
			(i < envelopeList.size())) {

			double alpha = std::acos(targetPoseList[i] * nCurPose);
			double ratio = std::min(std::max(alpha / falloffList[i], -1.0), 1.0);

			double resultWeight;
			if (ratio == 0.0) {
				resultWeight = envelopeList[i] * 1.0;
			}
			else if (ratio > 0.0) {
				resultWeight = envelopeList[i] * (1.0 - ratio);
			}
			else if (ratio < 0.0) {
				resultWeight = envelopeList[i] * (1.0 + ratio);
			}

			resultHandle.setDouble(resultWeight);
		}
		else {
			resultHandle.setDouble(0.0);
		}
		
	}

	weightsHandle.setAllClean();

	return MStatus::kSuccess;
}