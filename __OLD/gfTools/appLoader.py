import maya.cmds as cmds

# Load gfXtraTools
def gfXtraToolsLoad():
    from gfTools.gfXtraTools import gui as gfXtGui
    reload(gfXtGui)
    gfXtGui.gfXtraToolsUI()

def gfMayaToolsLoad():
    from gfTools.__OLD.gfTools import gfMayaTools as gfMt
    reload(gfMt)
    gfMt.gfMayaTools()

def gfGitToolLoad():
	import subprocess
	path = [("cd/"+r"Users\giulianofranca\Documents\maya\2016\scripts\gfTools\gfGitTool")]
	startPrompt = ['start', 'cmd', '/c', 'title', 'gfGitTool', 'for', 'Windows']
	space = ['^&^&']
	execFile = ['python', 'gfGitTool.py']
	posCmd = ['pause']
	finalCmd = []
	finalCmd.extend(startPrompt)
	finalCmd.extend(space)
	finalCmd.extend(path)
	finalCmd.extend(space)
	finalCmd.extend(execFile)
	finalCmd.extend(space)
	finalCmd.extend(posCmd)
	subprocess.Popen(finalCmd, shell=True)

def gfAutoRigLoad():
	from gfTools.gfAutoRig import gui as gfArGui
	reload(gfArGui)
	gfArGui.gfAutoRigUI()
