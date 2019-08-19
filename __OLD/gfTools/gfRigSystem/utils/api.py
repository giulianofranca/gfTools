import sys, os
import maya.cmds as cmds
import maya.OpenMaya as om

from gfTools.gfRigSystem.utils import log
from gfTools.gfRigSystem.utils import guides
from gfTools.gfRigSystem.utils import components

reload(log)
reload(guides)
reload(components)


def _getObjectName(v, t, cv, c=None, s=None):
    ''' Convert naming convention. | v = var, c = component, s = side, t = type, cv = convention '''
    obj = ''
    if cv == 0:
        if c != None: obj += c + '_'
        if s != None: obj += s.upper() + '_'
        obj += v + '_'
        obj += t
        return obj
    elif cv == 1:
        obj += t + '_'
        if s != None: obj += s.upper() + '_'
        if c != None: obj += c + '_'
        obj += v
        return obj
    else: sys.stderr.write("Naming convention (%s) don't exists"%(cv)); return False


def queryNamingConvention(index=None):
    ''' Query all naming convention types. '''
    nc = {0:'[component]_[side]_[var]_[type]',
        1:'[type]_[side]_[component]_[var]'}
    if index == None:
        for keys, value in nc.items():
            log.writeLog(t='info', msg='Naming convention [%s]: %s'%(keys, value))
    else:
        try:
            log.writeLog(t='info', msg='Naming convention setted to [%s]'%(index))
            return [index, nc[index]]
        except Exception:
            log.writeLog(t='error', msg="Naming convention [%s] don't exists."%(index))


def loadModel():
    ''' Load and prepare geometry model. '''
    pass

def enableLog(catch=True, preserve=False):
    ''' Enable catch log to export in a file later. '''
    log.enableLog(enable=catch, preserve=preserve)

def queryLog(w=False):
    logResult = log.checkLog(write=w)

def exportLogFile():
    ''' Export catched log to a file in specific path. '''
    user = os.getenv('USERNAME')
    fullPath = cmds.fileDialog2(ff='*.log', ds=2, cap='Export rig log...', fm=0, dir='C:/Users/%s/Desktop'%(user))[0]
    export = log.exportFile(fullPath)

def loadAllGuides(components):
    ''' Load components guides. '''
    for i in components:
        i.loadGuides()

def readAllGuides(components):
    ''' Read component guides transformations. '''
    for i in components:
        i.readGuides()

def loadComponent(type, name, side):
    cmpntsRAW = components.findComponents()
    cmpnts = []
    for cmpnt in cmpntsRAW: cmpnts.append(cmpnt['Name'].lower())
    if type.lower() in cmpnts:
        if side.lower() == 'left':
            side = 'L'
            return Component(type=type.lower(), name=name, side=side)
        if side.lower() == 'right':
            side = 'R'
            return Component(type=type.lower(), name=name, side=side)
        if side.lower() == 'middle':
            side = 'M'
            return Component(type=type.lower(), name=name, side=side)
        else: log.writeLog(t='error', msg='Side not found. Operation skipped. Must be [left, right or middle].')
    else:
        log.writeLog(t='error', msg='Component not found. Operation skipped. type [queryAllComponents()] to see all available components.')
        return False

def queryAllComponents():
    ''' Query all components names whitch contains string name or all flag. '''
    cmpntsRAW = components.findComponents()
    cmpnts = []
    for cmpnt in cmpntsRAW:
        cmpnts.append(cmpnt['Name'])
    return cmpnts

# -----------------------------------------------------------------------------------------------------------------------------------
# ------------------------------ Object Classes -------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------


class Char(object):

    _charInstances = dict()

    def __new__(cls, name):

        """ Verify if character instance exists. """

        if name in Char._charInstances:
            result = cmds.confirmDialog(t='Confirm', m='This character already exists. Do you want to override it?', b=['Yes', 'No'],
                db='No', cb='No', ds='No', ma='center')

            if result == 'Yes':
                return super(Char, cls).__new__(cls)
            else:
                log.writeLog(t='warning', msg='Char creation skipped...')
                return Char._charInstances[name]
        else:
            return super(Char, cls).__new__(cls)



    def __init__(self, name):

        """ Initialize a character object instance. """

        Char._charInstances[name] = self
        self.name = name
        self.geometryList = list()
        self.nameCV = None
        self.hierarchyNode = None
        self.components = list()

        log.writeLog(t='info', msg='Char (%s) created successfully.'%(self.name))



    def _checkNamingConvention(self):

        """ Check if naming convention is consistent. """

        if not self.nameCV[0] is int():
            return False
        elif self.nameCV is None:
            return False
        else:
            return True



    def loadAllGuides(self):

        """ Load all component guides connected to this character instance. """

        pass



    def readAllGuides(self):

        """ Read all component guides transformations connected to this character instance. """

        pass



    def loadGeometryGroup(self, geometryGrp):

        """ Load all geometry to character. """

        if cmds.objectType(geometryGrp) == 'transform':
            children = cmds.listRelatives(geometryGrp, c=True)
            for c in children:
                if cmds.objectType(c) == 'transform':
                    if cmds.objectType(cmds.listRelatives(c, s=True)) == 'mesh':
                        cmds.parent(c, ('|'+self.hierarchyNode+'|'+_getObjectName(t='hrc', v='geo', cv=self.nameCV[0])))
                        cmds.select(cl=True)
                        self.geometryList.append(c)
            if cmds.listRelatives(geometryGrp, c=True) == None:
                cmds.delete(geometryGrp)
        else:
            log.writeLog(t='error', msg='(%s) is not a group of geometries.'%(geometryGrp))



    def addGeometry(self, geo):

        """ Add geometry to character instance. """

        grpGeo = '|' + self.hierarchyNode + '|' + _getObjectName(t='hrc', v='geo', cv=self.nameCV[0])
        if geo == '@selection':
            sel = cmds.ls(sl=True, fl=True)
            if sel == []:
                log.writeLog(t='error', msg='Nothing is selected. Select at least one object and run this command.')
            else:
                for mesh in sel:
                    if cmds.objectType(cmds.listRelatives(mesh, s=True)) == 'mesh':
                        cmds.parent(mesh, grpGeo)
        else:
            if type(geo).__name__ == 'list':
                for mesh in geo:
                    if cmds.objectType(cmds.listRelatives(mesh, s=True)) == 'mesh':
                        cmds.parent(mesh, grpGeo)
            else:
                log.writeLog(t='error', msg='Argument must be a (list) type. Current type is (%s)'%(type(geo).__name__))
        cmds.select(cl=True)



    def removeGeometry(self, geo=None):

        """ Remove geometry from character instance. """

        grpGeo = '|' + self.hierarchyNode + '|' + _getObjectName(t='hrc', v='geo', cv=self.nameCV[0])
        grpNewGeo = cmds.group(em=True, n=(_getObjectName(t='geo', v=self.name, cv=self.nameCV[0])))
        if geo == None:
            for mesh in cmds.listRelatives(grpGeo, c=True):
                cmds.parent(mesh, grpNewGeo)
        else:
            for mesh in geo:
                cmds.parent(mesh, grpNewGeo)
        cmds.select(cl=True)



    def wireframeGeometry(self):

        """ Wireframe all geometry in geometry list. """

        geoGrp = '|' + self.hierarchyNode + '|' + _getObjectName(t='hrc', v='geo', cv=self.nameCV[0])
        tgl = cmds.getAttr(geoGrp+'.overrideShading')
        if tgl == 0:
            cmds.setAttr(geoGrp+'.overrideShading', 1)
        elif tgl == 1:
            cmds.setAttr(geoGrp+'.overrideShading', 0)
        else:
            log.writeLog(t='error', msg='Toggle override shading value unrecognized.')



    def createHierarchy(self):

        """ Create a character hierarchy based on a naming convention. """

        nameCV = self._checkNamingConvention()

        if nameCV == True:

            # Create group nodes
            grpChar = cmds.group(em=True, n=_getObjectName(t='char', v=self.name, cv=self.nameCV[0]))
            grpGbl = cmds.group(em=True, n=_getObjectName(t='hrc', v='gbl', cv=self.nameCV[0]), p=grpChar)
            grpSktn = cmds.group(em=True, n=_getObjectName(t='hrc', v='sktn', cv=self.nameCV[0]), p=grpGbl)
            grpCtrl = cmds.group(em=True, n=_getObjectName(t='hrc', v='ctrl', cv=self.nameCV[0]), p=grpGbl)
            grpIk = cmds.group(em=True, n=_getObjectName(t='hrc', v='ikHdle', cv=self.nameCV[0]), p=grpGbl)
            grpCtrlGbl = cmds.group(em=True, n=_getObjectName(t='hrc', v='ctrlGbl', cv=self.nameCV[0]), p=grpChar)
            grpGeo = cmds.group(em=True, n=_getObjectName(t='hrc', v='geo', cv=self.nameCV[0]), p=grpChar)
            grpPSD = cmds.group(em=True, n=_getObjectName(t='hrc', v='psd', cv=self.nameCV[0]), p=grpChar)
            grpXtra = cmds.group(em=True, n=_getObjectName(t='hrc', v='xtra', cv=self.nameCV[0]), p=grpChar)
            grpXtraShow = cmds.group(em=True, n=_getObjectName(t='hrc', v='xtraToShow', cv=self.nameCV[0]), p=grpXtra)
            grpXtraHide = cmds.group(em=True, n=_getObjectName(t='hrc', v='xtraToHide', cv=self.nameCV[0]), p=grpXtra)

            # Setup group nodes
            cmds.setAttr(grpChar+".useOutlinerColor", 1)
            cmds.setAttr(grpChar+".outlinerColor", 0.18039, 0.80000, 0.44314)
            cmds.setAttr((grpIk+".v"), False)
            cmds.setAttr((grpPSD+".v"), False)
            cmds.setAttr((grpXtraHide+".v"), False)
            cmds.setAttr((grpIk+".overrideEnabled"), True)
            cmds.setAttr((grpGeo+".overrideEnabled"), True)
            cmds.setAttr((grpPSD+".overrideEnabled"), True)
            cmds.setAttr((grpXtraHide+".overrideEnabled"), True)
            cmds.setAttr((grpIk+".overrideDisplayType"), 2)
            cmds.setAttr((grpGeo+".overrideDisplayType"), 2)
            cmds.setAttr((grpPSD+".overrideDisplayType"), 2)
            cmds.setAttr((grpXtraHide+".overrideDisplayType"), 2)

            self.hierarchyNode = grpChar
            log.writeLog(t='info', msg='(%s) hierarchy created.'%(self.name))
            cmds.select(cl=True)






class Component(object):
    def __init__(self, type, name, side):
        self.type = type
        self.name = name
        self.side = side
        self.parent = None
        self.jntsRes = None
        self.jntsFK = None
        self.jntsIK = None
        self.jntsRib = None
        self.ikHandle = None

    # def __repr__(self):
    #     return "api.loadComponent('%s', '%s', '%s')" %(self.type, self.name, self.side)

    @property
    def objectType(self):
        pass

    @objectType.deleter
    def objectType(self):
        # del self
        pass

    @property
    def guidesInfo(self):
        guidesInfo = guides.loadComponentGuidesInfo(self.type, self.side)
        return guidesInfo

    @guidesInfo.setter
    def guidesInfo(self, name, side):
        pass

    @guidesInfo.deleter
    def guidesInfo(self):
        self.guidesInfo = None

    def loadGuides(self):
        cmds.warning('In development')

    def readGuides(self):
        cmds.warning('In development')

    def createJoints(self, ro):
        pass

    def setParent(self):
        pass

class HumanLeg(Component):
    def __init__(self):
        Component.__init__(type, name, side)

    def __repr__(self):
        importPath = 'from gfTools.gfRigSystem.utils import api'
        return "api.loadComponent('HumanLeg')"




class objectName(object):
    var = ''
    type = ''
    component = ''
    side = ''
    name = ''
    indexConvention = ''
    def __init__(self, v, t, cv, c=None, s=None):
        objectName.var = v
        objectName.type = t
        objectName.component = c
        objectName.side = s
        objectName.indexConvention = cv[0]
        name = ''
        if cv[0] == 0:
            if c != None: name += c + '_'
            if s != None: name += s.upper() + '_'
            name += v + '_'
            name += t
        objectName.name = name
