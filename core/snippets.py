cmds.setAttr("gfRigPSDVectorAngle_P1.targetEnvelope[0]", 1.0)
cmds.setAttr("gfRigPSDVectorAngle_P1.targetFalloff[0]", 45.0)
cmds.setAttr("gfRigPSD_P1.targetEnvelope[0]", 1.0)
cmds.setAttr("gfRigPSD_P1.targetFalloff[0]", 45.0)

cmds.setAttr("multMatrix1.matrixIn[0]", cmds.getAttr("offset.matrixSum"), type="matrix")
cmds.setAttr("decomposeMatrix2.inputMatrix", cmds.getAttr("offset.matrixSum"), type="matrix")
cmds.setAttr("multMatrix1.matrixIn[0]", cmds.getAttr("obj.worldMatrix"), type="matrix")
cmds.setAttr("gfUtilAimConstraint_P1.offset", cmds.getAttr("offset.matrixSum"), type="matrix")
cmds.setAttr("gfUtilAimConstraint_P1.offset", cmds.getAttr("inverseMatrix1.outputMatrix"), type="matrix")


cmds.setAttr("multMatrix1.matrixIn[0]", cmds.getAttr("offset.matrixSum"), type="matrix")
cmds.setAttr("multMatrix2.matrixIn[0]", cmds.getAttr("offset.matrixSum"), type="matrix")

# import autopep8
# path = "C:/Users/gfranca/Documents/maya/2017/scripts/gfTools/core/nodesDev/gfToolsNodes/py/n_gfRigPSDVectorAngle.py"
# class Options(object):
#     def __init__(self):
#         self.in_place = True
#             self.pep8_passes = -1
#             self.list_fixes = None
#             self.jobs = 0
#             self.ignore = []
#             self.verbose = 0
#             self.diff = None
#             self.select = []
#             self.exclude = []
#             self.aggressive = 2
#             self.line_range = []
#             self.recursive = None
#             self.max_line_length= 100
#             self.indent_size = 4
#             self.experimental = False
#             self.hang_closing = []
# options = Options()
# autopep8.fix_file(path, options)
"""
cd core\nodesDev\gfToolsNodes\py
python3 -m autopep8 --in-place --aggressive --max-line-length 160 n_gfRigPSDVectorAngle.py
"""