# Import the pose data to scene.
import os
import datetime
import json

from maya import cmds


owner = os.getenv('USERNAME')
dataPath = 'C:/Users/%s/Desktop/MyPose.gfpose' % (owner)

with open(dataPath, 'r') as doc:
    dataList = json.load(doc)

selList = cmds.ls(sl=True)
for sel in selList:
    curCtrl = sel
    if cmds.referenceQuery(sel, inr=True):
        refPath = cmds.referenceQuery(sel, f=True)
        nameSpace = cmds.file(refPath, q=True, ns=True)
        curCtrl = sel.replace('%s:' % (nameSpace), '')
    if curCtrl in dataList['control']:
        attrList = dataList['control'][curCtrl]
        for attr in attrList:
            attrValue = attrList[attr]
            cmds.setAttr('%s.%s' % (sel, attr), attrValue)

print("Successfull import My Pose Data.")
