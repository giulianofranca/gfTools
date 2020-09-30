#include "headers/utils.hpp"

gfRig::Utils::Utils() {}
gfRig::Utils::~Utils() {}

const std::string gfRig::Utils::getPoleVectorPosition(){
    MSelectionList sel;
    MGlobal::getActiveSelectionList(sel);
    if (sel.length() >= 3){
        MDagPath root, mid, end;
        sel.getDagPath(0, root);
        sel.getDagPath(1, mid);
        sel.getDagPath(2, end);
        MFnTransform transFn(root);
        MVector vStart = transFn.getTranslation(MSpace::kWorld);
        transFn.setObject(mid);
        MVector vMid = transFn.getTranslation(MSpace::kWorld);
        transFn.setObject(end);
        MVector vEnd = transFn.getTranslation(MSpace::kWorld);
        
        MVector vFirstBone = vMid - vStart;
        MVector vSecondBone = vEnd - vMid;
        MVector nLengthBone = (vEnd - vStart).normal();

        MVector vProj = (vFirstBone * nLengthBone) * nLengthBone;
        MVector vArrow = vFirstBone - vProj;
        MVector nArrow = vArrow.normal();
        double length = (vFirstBone.length() + vSecondBone.length()) * 0.5;
        MVector vPole = vMid + nArrow * length;

        MVector nUp = nLengthBone ^ vFirstBone;
        nUp.normalize();
        MVector nBinormal = vPole ^ nUp;
        nBinormal.normalize();

        double matrix[4][4] = {
            {nArrow.x, nArrow.y, nArrow.z, 0.0},
            {nUp.x, nUp.y, nUp.z, 0.0},
            {nBinormal.x, nBinormal.y, nBinormal.z, 0.0},
            {vPole.x, vPole.y, vPole.z, 1.0}
        };
        double scale[3] = {1.0, 1.0, 1.0};
        MMatrix mPole(matrix);
        MTransformationMatrix mtxFn(mPole);
        mtxFn.setScale(scale, MSpace::kWorld);

        MDagModifier dagMod;
        MObject poleObj = dagMod.createNode("transform");
        dagMod.renameNode(poleObj, "PoleVectorObj");
        MStatus status = dagMod.doIt();
        if (!status)
            return std::string("");
        transFn.setObject(poleObj);
        transFn.set(mtxFn);
        MDagPath polePath;
        MDagPath::getAPathTo(poleObj, polePath);

        MSelectionList outSel;
        outSel.add(polePath);
        MGlobal::setActiveSelectionList(outSel);
        return std::string(polePath.fullPathName().asChar());
    }
    return std::string("");
}


const std::string gfRig::Utils::getPoleVectorPosition(double distance){
    MSelectionList sel;
    MGlobal::getActiveSelectionList(sel);
    if (sel.length() >= 3){
        MDagPath root, mid, end;
        sel.getDagPath(0, root);
        sel.getDagPath(1, mid);
        sel.getDagPath(2, end);
        MFnTransform transFn(root);
        MVector vStart = transFn.getTranslation(MSpace::kWorld);
        transFn.setObject(mid);
        MVector vMid = transFn.getTranslation(MSpace::kWorld);
        transFn.setObject(end);
        MVector vEnd = transFn.getTranslation(MSpace::kWorld);
        
        MVector vFirstBone = vMid - vStart;
        MVector vSecondBone = vEnd - vMid;
        MVector nLengthBone = (vEnd - vStart).normal();

        MVector vProj = (vFirstBone * nLengthBone) * nLengthBone;
        MVector vArrow = vFirstBone - vProj;
        MVector nArrow = vArrow.normal();
        double length = distance;
        MVector vPole = vMid + nArrow * length;

        MVector nUp = nLengthBone ^ vFirstBone;
        nUp.normalize();
        MVector nBinormal = vPole ^ nUp;
        nBinormal.normalize();

        double matrix[4][4] = {
            {nArrow.x, nArrow.y, nArrow.z, 0.0},
            {nUp.x, nUp.y, nUp.z, 0.0},
            {nBinormal.x, nBinormal.y, nBinormal.z, 0.0},
            {vPole.x, vPole.y, vPole.z, 1.0}
        };
        double scale[3] = {1.0, 1.0, 1.0};
        MMatrix mPole(matrix);
        MTransformationMatrix mtxFn(mPole);
        mtxFn.setScale(scale, MSpace::kWorld);

        MDagModifier dagMod;
        MObject poleObj = dagMod.createNode("transform");
        dagMod.renameNode(poleObj, "PoleVectorObj");
        MStatus status = dagMod.doIt();
        if (!status)
            return std::string("");
        transFn.setObject(poleObj);
        transFn.set(mtxFn);
        MDagPath polePath;
        MDagPath::getAPathTo(poleObj, polePath);

        MSelectionList outSel;
        outSel.add(polePath);
        MGlobal::setActiveSelectionList(outSel);
        return std::string(polePath.fullPathName().asChar());
    }
    return std::string("");
}