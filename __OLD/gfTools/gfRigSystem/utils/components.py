import os
import json
import maya.cmds as cmds


def findComponents():
    filePath = os.path.abspath(__file__).split('\\')
    filePath = '/'.join(filePath[:len(filePath)-1])
    with open(filePath+'/guides.json', 'r') as fileContent:
        data = json.load(fileContent)
    for component in data['Components']:
        pass
    return data['Components']
