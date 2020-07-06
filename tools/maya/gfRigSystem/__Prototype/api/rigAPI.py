# PROTOTYPING gfRigSystem
#
#
# RIG COLORS
# Main controllers = Yellow
# Secondary controllers = LightBlue
# Tertiary controllers = Red
# Settings controllers = DarkBlue
# Global controllers = Purple
#
# WORKFLOW
# Create Guides
# Setup initial skeleton
# Setup geodesic voxel skin to test deformation
# Create components joints
# Create controllers and attrs
# Setup components
# Create final skinCluster

import collections
import math
import os
import sys
import datetime
import xml.etree.ElementTree as et
import xml.dom.minidom as minidom
# IMPORT EXTERNAL DEPENDENCIES
# Get all external modules needed.
# "collections" to create a ordered dictionary, "math" to calculate custom mathematical
# operations, "os" to access directories and files in system, "sys" to print additional error
# messages, "json" to export a rig file from a dict.

import maya.cmds as cmds
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2
# IMPORT MAYA MODULES
# Get all Maya modules needed.
# "maya.cmds" to operate simple commands, "maya.api.OpenMaya" to have access to Maya Python Api 2.0
# who is faster than the Maya Python Api 1.0 and have more functions than the Maya Cmds module,
# "maya.api.OpenMayaAnim" to help with other functionalities like curves, skinCluster and lattices.

cmds.loadPlugin("gfToolsNodes.mll")
# IMPORT INTERNAL DEPENDENCIES
# Get the gfTools plugin.
# Load a custom library of C++ nodes who can be used to rig a character if needed.

kAPIVERSION = "1.0"
kREQUIREDVERSION = "0.9"
kAUTHOR = "Giuliano Franca"


#####################################################################################################
##############################            Utility functions            ##############################
#####################################################################################################
def _emitMessage(title, message, defaultBtn, cancelBtn):
    """
    Signature: _emitMessage(title, message, defaultBtn, cancelBtn)
    Parameters: title - string, message - string, defaultBtn - string,
        cancelBtn - string
    Returns: string
    Description: Emit a modal with message to confirm or cancel a action.
    """
    result = cmds.confirmDialog(title=title, message=message, button=[defaultBtn, cancelBtn],
                                defaultButton=defaultBtn, cancelButton=cancelBtn, dismissString=cancelBtn)

    return result


def _emitProgressBar():
    pass


def _readFilePath(title, dirPath=None, fileMode="File", ok="Save", cancel="Cancel", filters=list()):
    """
    Signature: _readFilePath(title, dirPath=None, fileMode="File", ok="Save", cancel="Cancel", filters=list())
    Parameters: title - string, dirPath=None - string, fileMode="File" - string,
        ok="Save" - string, cancel="Cancel" - string, filters=list() - list
    Returns: string
    Description: Read a file path from external window.
    """
    if fileMode == "Save":
        fm = 0
    elif fileMode == "File":
        fm = 1
    if fileMode == "Dir":
        fm = 3
    elif fileMode == "Files":
        fm = 4
    if dirPath == None:
        dirPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "characterData")
    if filters:
        ff = ';;'.join(filters)
    else:
        ff = 'All Files (*.*)'

    path = cmds.fileDialog2(ds=2, fm=fm, cap=title, dir=dirPath, okc=ok, cc=cancel, ff=ff)

    return path


def _convertInstanceToString(data):
    """
    Signature: _convertInstanceToString(data)
    Parameters: data - collections.OrderedDict
    Returns:
    Description: Convert a Maya API instance to a string type Dag Path or DG absolute name.
    """
    if not isinstance(data, collections.OrderedDict):
        om2.MGlobal.displayError("data argument must be a OrderedDict.")
        return

    for key, value in data.items():
        if key == "Instance":
            selList = om2.MSelectionList().add(value)
            try:
                obj = om2.MDagPath.getAPathTo(selList.getDependNode(0)).fullPathName()
            except TypeError as err:
                obj = om2.MFnDependencyNode(selList.getDependNode(0)).absoluteName()
            data[key] = obj
        if isinstance(value, collections.OrderedDict):
            _convertInstanceToString(value)


def _convertStringToInstance(data):
    """
    Signature: _convertStringToInstance(data)
    Parameters: data - collections.OrderedDict
    Returns:
    Description: Convert a string Dag Path or DG absolute name to a Maya API instance.
    """
    if not isinstance(data, collections.OrderedDict):
        om2.MGlobal.displayError("data argument must be a OrderedDict.")
        return

    for key, value in data.items():
        if key == "Instance":
            selList = om2.MSelectionList().add(value)
            obj = selList.getDependNode(0)
            data[key] = obj
        if isinstance(value, collections.OrderedDict):
            _convertStringToInstance(value)


def _convertDictToXMLElements(data, root):
    """
    Signature: _convertDictToXMLElements(data, root)
    Parameters: data - collections.OrderedDict, root - xml.etree.ElementTree.Element
    Returns:
    Description: Populate a xml element of dicts.
    """
    if not isinstance(data, collections.OrderedDict):
        om2.MGlobal.displayError("data argument must be a OrderedDict.")
        return
    if not isinstance(root, et.Element):
        om2.MGlobal.displayError("root argument must be a xml.etree.ElementTree.Element")
        return

    def attatchChild(name, root):
        node = et.SubElement(root, name)
        return node

    def attatchValue(name, value, root):
        node = et.SubElement(root, name)
        node.text = value
        if name == "Instance":
            type = om2.MFnDependencyNode(om2.MSelectionList().add(value).getDependNode(0)).typeName
            node.set("type", type)

    for key, value in data.items():
        if isinstance(value, collections.OrderedDict):
            child = attatchChild(key, root)
            _convertDictToXMLElements(value, child)
        else:
            attatchValue(key, value, root)


def _convertXMLElementsToDict(data, root):
    """
    Signature: _convertXMLElementsToDict(data, root)
    Parameters: data - collections.OrderedDict, root - xml.etree.ElementTree.Element
    Returns:
    Description: Populate a dict of xml elements.
    """
    if not isinstance(data, collections.OrderedDict):
        om2.MGlobal.displayError("data argument must be a OrderedDict.")
        return
    if not isinstance(root, et.Element):
        om2.MGlobal.displayError("root argument must be a xml.etree.ElementTree.Element")
        return

    for child in root:
        if len(child) > 0:
            data[child.tag] = collections.OrderedDict()
            _convertXMLElementsToDict(data[child.tag], child)
        else:
            value = child.text
            if value == None:
                value = collections.OrderedDict()
            data[child.tag] = value


def _createCharFromXMLElements(root):
    """
    Signature: _createCharFromXMLElements(root)
    Parameters: root - xml.etree.ElementTree.Element
    Returns:
    Description: Create a Character class from XML elements.
    """
    if not isinstance(root, et.Element):
        om2.MGlobal.displayError("root argument must be a xml.etree.ElementTree.Element")
        return

    for child in root:
        if len(child) > 0:
            _createCharFromXMLElements(child)
        else:
            if child.tag == "Instance":
                fullPath = child.text  # |Clovis_char|deform_hrc|baseSktn_defLyr
                type = child.attrib["type"]  # transform
                if '|' in fullPath:
                    # Dag Node
                    numParents = len(fullPath.split('|'))  # 4
                    name = fullPath.split('|')[-1]  # baseSktn_defLyr
                    parent = '|'.join(fullPath.split('|')[:numParents-1])  # |Clovis_char|deform_hrc
                    if parent == "":
                        instance = om2.MFnDagNode().create(type, name)
                        cmds.setAttr('%s.useOutlinerColor' % om2.MDagPath.getAPathTo(instance).fullPathName(), True)
                        cmds.setAttr('%s.outlinerColor' % om2.MDagPath.getAPathTo(instance).fullPathName(), 0.0, 1.0, 0.0)
                    else:
                        parentObj = om2.MSelectionList().add(parent).getDependNode(0)
                        instance = om2.MFnDagNode().create(type, name, parentObj)
                else:
                    # DG Node
                    pass


def _checkObjectExists(obj):
    """
    Signature: _checkObjectExists(obj)
    Parameters: obj - string | MObject
    Returns: bool
    Description: Check if object exists.
    """
    if not isinstance(obj, str) and not isinstance(obj, om2.MObject):
        om2.MGlobal.displayError("obj argument must be a string or MObject.")
        return

    if isinstance(obj, om2.MObject):
        try:
            obj = om2.MDagPath.getAPathTo(om2.MSelectionList().add(obj).getDependNode(0)).fullPathName()
        except TypeError as err:
            obj = om2.MFnDependencyNode(om2.MSelectionList().add(obj).getDependNode(0)).absoluteName()

    try:
        selList = om2.MSelectionList().add(obj)
        status = True
    except RuntimeError as err:
        status = False

    return status


def createAttribute(target, type, name):
    """
    Signature: createAttribute(target, type, name)
    Parameters: target - MObject, type - string, name - string
    Returns:
    Description: Create attribute in a target object.
    """
    pass
# def mirrorComponent(target, mirroedComponent=None):
#     """ Override means mirror in a already created component"""
#     return "new class component if component have kSIDE attribute"


#####################################################################################################
##############################            Character Class            ################################
#####################################################################################################

class Character(object):

    _kFreshInstance = True

    kMainColor = (1.000, 1.000, 0.176)          # RGB[0:1] Yellow
    kSecondaryColor = (0.119, 0.581, 0.687)     # RGB[0:1] LightBlue
    kTertiaryColor = (1.000, 0.103, 0.103)      # RGB[0:1] Red
    kSettingsColor = (0.025, 0.101, 0.551)      # RGB[0:1] DarkBlue
    kGlobalColor = (0.532, 0.064, 1.000)        # RGB[0:1] Purple

    def __new__(cls, name=""):
        if not isinstance(name, str):
            om2.MGlobal.displayError("\"name\" argument must be a string.")
            return

        if _checkObjectExists("%s_char" % name):
            om2.MGlobal.displayError("An character with this name already exists \"%s\"." % name)
            return

        return super(Character, cls).__new__(cls, name)

    def __init__(self, name=""):
        """
        Signature: Character(name)
        Parameters: name - string
        Returns: <Character> Instance
        Description: Initializes Character.
        """
        if name == "": name = "NewCharacter"
        self._createName = name
        self._data = collections.OrderedDict()

        if Character._kFreshInstance == True:
            self._initialize()

    def _initialize(self):
        char_instance = om2.MFnTransform().create(om2.MObject.kNullObj)
        deform_instance = om2.MFnTransform().create(om2.MObject.kNullObj)
        globalTransform_instance = om2.MFnTransform().create(om2.MObject.kNullObj)
        geometry_instance = om2.MFnTransform().create(om2.MObject.kNullObj)

        dagMod = om2.MDagModifier()
        dagMod.renameNode(char_instance, "%s_char" % self._createName)
        dagMod.renameNode(deform_instance, "deform_hrc")
        dagMod.renameNode(globalTransform_instance, "globalTransform_hrc")
        dagMod.renameNode(geometry_instance, "geometry_hrc")
        dagMod.reparentNode(deform_instance, char_instance)
        dagMod.reparentNode(globalTransform_instance, char_instance)
        dagMod.reparentNode(geometry_instance, char_instance)
        dagMod.doIt()

        cmds.setAttr('%s.useOutlinerColor' % om2.MDagPath.getAPathTo(char_instance).fullPathName(), True)
        cmds.setAttr('%s.outlinerColor' % om2.MDagPath.getAPathTo(char_instance).fullPathName(), 0.0, 1.0, 0.0)

        self._data["CharName"] = self._createName
        self._data["Instance"] = char_instance
        self._data["Content"] = collections.OrderedDict()
        self._data["Content"]["Deform"] = collections.OrderedDict()
        self._data["Content"]["Deform"]["Instance"] = deform_instance
        self._data["Content"]["Deform"]["DeformationLayers"] = collections.OrderedDict()
        self._data["Content"]["GlobalTransform"] = collections.OrderedDict()
        self._data["Content"]["GlobalTransform"]["Instance"] = globalTransform_instance
        self._data["Content"]["Geometry"] = collections.OrderedDict()
        self._data["Content"]["Geometry"]["Instance"] = geometry_instance
        self._data["Info"] = collections.OrderedDict()
        self._data["Info"]["Created"] = datetime.datetime.now().strftime("%b %d, %Y - %I:%M:%S %p")
        self._data["Info"]["LastModified"] = datetime.datetime.now().strftime("%b %d, %Y - %I:%M:%S %p")
        # self._data["Info"]["UseCustomTech"] = self.useCustomTech

        self._deformData = self._data["Content"]["Deform"]
        self._globalTransformData = self._data["Content"]["GlobalTransform"]
        self._geometryData = self._data["Content"]["Geometry"]

        return True

    def __repr__(self):
        return "gfRigSystem.api.rigAPI.Character(%s)" % self.charName

    @classmethod
    def fromCharacterFile(cls, recreate=False, path=None):
        """
        Signature: <Character>.fromCharacterFile(recreate=False)
        Parameters: recreate - bool
        Returns: Character
        Description: Create a new Character instance by loading an external file.
        """
        dirPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "characterData")
        if path == None:
            path = _readFilePath(title="Import Character File", dirPath=dirPath, fileMode="File",
                                 ok="Import", filters=['gfRig Files (*.gfRig)'])[0]

        existData = collections.OrderedDict()
        tree = et.parse(path)
        root = tree.getroot()
        attrs = root.attrib
        try:
            if "gfRigSystem" in attrs.values():
                if float(attrs["version"]) > float(kAPIVERSION):
                    om2.MGlobal.displayError(
                        "This api works on file versions %s or older, current: %s. Check your file version or update this api version."
                        % (kAPIVERSION, attrs["version"]))
                    return
                elif float(attrs["version"]) < float(kREQUIREDVERSION):
                    om2.MGlobal.displayError(
                        "This api requires a minimum file version of %s, receive %s."
                        % (kREQUIREDVERSION, attrs["version"]))
                    return
            else:
                om2.MGlobal.displayError("Application not recognized. Expects \"gfRigSystem\"")
                return
        except:
            om2.MGlobal.displayError("File not recognized.")
            return

        _convertXMLElementsToDict(existData, root)

        if not recreate:
            try:
                _convertStringToInstance(existData)
            except:
                result = _emitMessage("Something goes wrong!",
                                      "Cannot find %s nodes. Do you want to recreate these nodes?" % existData["CharName"], "Recreate", "Cancel")
                if result == "Recreate":
                    return Character.fromCharacterFile(recreate=True, path=path)
                else:
                    om2.MGlobal.displayWarning("Operation canceled!")
                    return
        else:
            if _checkObjectExists('%s_char' % existData["CharName"]):
                om2.MGlobal.displayError("%s nodes already created." % existData["CharName"])
                return

        name = existData["CharName"]
        Character._kFreshInstance = False
        newChar = cls(name)
        Character._kFreshInstance = True
        newChar._data = existData

        newChar._deformData = newChar._data["Content"]["Deform"]
        newChar._globalTransformData = newChar._data["Content"]["GlobalTransform"]
        newChar._geometryData = newChar._data["Content"]["Geometry"]

        if recreate:
            _createCharFromXMLElements(root)
            _convertStringToInstance(newChar._data)

        return newChar

    @property
    def charName(self):
        """
        Name: charName
        Type: string
        Access: R
        Description: Current name of char node.
        """
        return self._data["CharName"]

    @property
    def charPath(self):
        """
        Name: charPath
        Type: string
        Access: R
        Description: Absolute path of char node.
        """
        return om2.MDagPath.getAPathTo(self._data["Instance"]).fullPathName()

    @property
    def deformPath(self):
        """
        Name: deformPath
        Type: string
        Access: R
        Description: Absolute path of char deform parent node.
        """
        return om2.MDagPath.getAPathTo(self._deformData["Instance"]).fullPathName()

    @property
    def globalTransformPath(self):
        """
        Name: globalTransformPath
        Type: string
        Access: R
        Description: Absolute path of char globalTransform parent node.
        """
        return om2.MDagPath.getAPathTo(self._globalTransformData["Instance"]).fullPathName()

    @property
    def geometryPath(self):
        """
        Name: geometryPath
        Type: string
        Access: R
        Description: Absolute path of char geometry parent node.
        """
        return om2.MDagPath.getAPathTo(self._geometryData["Instance"]).fullPathName()

    @property
    def deformationLayers(self):
        """
        Name: deformationLayers
        Type: list
        Access: R
        Description: Names of all deformation layers nodes.
        """
        defLyrs = list()
        for layerName, layerValue in self._deformData["DeformationLayers"].items():
            defLyrs.append(layerName)

        return defLyrs

    def exportCharacterFile(self):
        """
        Signature: <Character>.exportCharacterFile()
        Parameters:
        Returns:
        Description: Export Character data to a external file (.gfRig).
        """
        oldLastModified = self._data["Info"]["LastModified"]
        try:
            self._data["Info"]["LastModified"] = datetime.datetime.now().strftime("%b %d, %Y - %I:%M:%S %p")
            dirPath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "characterData")
            defaultFilePath = os.path.join(dirPath, "%s.gfRig" % self.charName)
            path = _readFilePath(title="Export Character File", dirPath=defaultFilePath, fileMode="Save",
                                 ok="Export", filters=['gfRig Files (*.gfRig)'])[0]

            _convertInstanceToString(self._data)

            root = et.Element("Data", attrib={
                "application": "gfRigSystem",
                "version": kAPIVERSION
            })

            _convertDictToXMLElements(self._data, root)

            finalElement = minidom.parseString(et.tostring(root, 'utf-8')).toprettyxml(indent="    ")
            with open(path, 'w') as f:
                f.write(finalElement)

            _convertStringToInstance(self._data)
        except:
            self._data["Info"]["LastModified"] = oldLastModified
            sys.stderr.write("Unable to export character file.")

        return True

    def renameChar(self, name):
        """
        Signature: <Character>.renameChar(name)
        Parameters: name - string
        Returns:
        Description: Change the name of a Character class instance.
        """
        if _checkObjectExists(self._data["Instance"]):
            dagMod = om2.MDagModifier()
            dagMod.renameNode(self._data["Instance"], "%s_char" % name)
            dagMod.doIt()

            self._data["CharName"] = name

            return True
        else:
            om2.MGlobal.displayError("Cannot find character node.")
            return

    def createDeformationLayer(self, name):
        """
        Signature: <Character>.createDeformationLayer(name)
        Parameters: name - string
        Returns:
        Description: Create a deformation layer node in the character hierarchy.
        """
        if _checkObjectExists(self._deformData["Instance"]):
            defLyr = om2.MFnTransform().create(om2.MObject.kNullObj)
            dagMod = om2.MDagModifier()
            dagMod.renameNode(defLyr, "%s_defLyr" % name)
            dagMod.reparentNode(defLyr, self._deformData["Instance"])
            dagMod.doIt()

            self._deformData["DeformationLayers"][name] = collections.OrderedDict()
            self._deformData["DeformationLayers"][name]["Instance"] = defLyr
            self._deformData["DeformationLayers"][name]["Components"] = collections.OrderedDict()

            return True
        else:
            om2.MGlobal.displayError("Cannot find character deform node.")
            return

    def addGeometry(self, geoList):
        # Parent all geometry in the geometry hierarchy
        # Add all geometry in self.geometry dict
        pass

    def createAsset(self):
        pass

    def bindGeometry(self):
        pass

    def createSpaceSwitch(self):
        pass



#####################################################################################################
##############################            Component Classes            ##############################
#####################################################################################################
"""Main component class object"""


class Component(object):
    kName = None
    kType = None
    kParent = None
    kGuidesDefaultPos = dict()

    def __init__(self, defLyr):
        # __new__: Verify if character exists,
        # 1- Create a null transform node in character hierachy
        self.kTRANSFORM_PATH = None
        self.kJOINTS_PATH = None
        self.kCONTROLS_PATH = None
        self.kIKHANDLE_PATH = None
        self.kMISC_PATH = None
        self.kNONTRANSFORM_PATH = None

        self.character = char

    @classmethod
    def fromCreatedData(cls):
        pass

    def deleteComponent(self):
        pass


class HumanLeg(Component):

    thigh = []
    shin = []
    ankle = []
    toe = []
    legEnd = []

    def __init__(self, defLyr):
        pass


class HumanArm(Component):

    clavicle = []
    upperArm = []
    foreArm = []
    wrist = []
    palm = []
    armEnd = []

    def __init__(self, defLyr):
        pass


class HumanSpine(Component):

    hip = []
    spines = []
    chest = []

    def __init__(self, defLyr):
        pass


class HumanHead(Component):

    neck = []
    head = []
    headEnd = []

    def __init__(self, defLyr):
        pass


class Prop(Component):
    pass

###################################################################################################
##############################            Utility Classes            ##############################
###################################################################################################


class RotOrder(object):
    """ Available rotation orders in Euler rotations. """
    kXYZ = "xyz"
    kYZX = "yzx"
    kZXY = "zxy"
    kXZY = "xzy"
    kYXZ = "yxz"
    kZYX = "zyx"

    def __new__(cls, order):
        try:
            if (order.lower() == rotOrder.kXYZ or
                order.lower() == rotOrder.kYZX or
                order.lower() == rotOrder.kZXY or
                order.lower() == rotOrder.kXZY or
                order.lower() == rotOrder.kYXZ or
                    order.lower() == rotOrder.kZYX):
                return super(rotOrder, cls).__new__(cls, order.lower())
            else:
                raise RuntimeError, "Rotation order \"%s\" not recognized." % order.lower()
        except:
            raise RuntimeError, "Rotation order \"%s\" not recognized." % order.lower()

    def __init__(self, order):
        self._order = order

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        try:
            if (value.lower() == rotOrder.kXYZ or
                value.lower() == rotOrder.kYZX or
                value.lower() == rotOrder.kZXY or
                value.lower() == rotOrder.kXZY or
                value.lower() == rotOrder.kYXZ or
                    value.lower() == rotOrder.kZYX):
                self._order = value.lower()
            else:
                raise RuntimeError, "Rotation order \"%s\" not recognized." % value.lower()
        except:
            raise RuntimeError, "Rotation order \"%s\" not recognized." % value.lower()

    def __eq__(self, other):
        return self.order == other.order

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "gfRigSystem.api.rigAPI.rotOrder.r%s" % self._order.upper()

    def __repr__(self):
        return "gfRigSystem.api.rigAPI.rotOrder.r%s" % self._order.upper()
