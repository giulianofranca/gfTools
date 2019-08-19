# Export the pose data to custom format
import os
import datetime
import json

from maya import cmds


# Collect ctrls attributes and attribute values
selList = cmds.ls(sl=True)
ctrlInfoList = {}
for sel in selList:
    attrList = cmds.listAttr(sel, k=True, u=True, sn=True)
    attrInfoList = {}
    if attrList:
        for attr in attrList:
            attrValue = cmds.getAttr('%s.%s' % (sel, attr))
            attrInfoList.setdefault(attr.encode(), attrValue)
        curCtrl = sel
        # Check the reference
        if cmds.referenceQuery(sel, inr=True):
            refPath = cmds.referenceQuery(sel, f=True)
            nameSpace = cmds.file(refPath, q=True, ns=True)
            curCtrl = sel.replace('%s:' % (nameSpace), '')
    ctrlInfoList.setdefault(curCtrl.encode(), attrInfoList)

# Data history
owner = os.getenv('USERNAME')
time = datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M %p")
mayaVersion = cmds.about(q=True, v=True)
version = '0.1'
dataList = {'control': ctrlInfoList, 'history': [owner, time, mayaVersion, version]}

# Write Pose Data C:\Users\gfranca\Desktop
dataPath = 'C:/Users/%s/Desktop/MyPose.gfpose' % (owner)
with open(dataPath, 'w') as doc:
    jsonData = json.dumps(dataList, indent=4)
    doc.write(jsonData)

# Create Pose Icon
poseIconPath = dataPath.replace('.gfpose', '.png')
curFrame = cmds.currentTime(q=True)
modelPanelList = cmds.getPanel(type='modelPanel')
for mPanel in modelPanelList:
    cmds.modelEditor(mPanel, e=True, alo=False, pm=True)
playblast = cmds.playblast(st=curFrame, et=curFrame, fmt='image', cc=True, v=False, orn=False, fp=1, p=100, c='png',
                           wh=[512, 512], cf=poseIconPath)

print("Successfull export My Pose Data.")
