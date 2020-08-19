# -*- coding: utf-8 -*-
"""
Copyright 2020 Giuliano Franca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

====================================================================================================

How to use:
    * Copy the parent folder to the MAYA_SCRIPT_PATH.
    * To find MAYA_SCRIPT_PATH paste this command in a Python tab:
        import os; os.environ["MAYA_SCRIPT_PATH"].split(";")
    * In Maya, go to Windows > Settings/Preferences > Plug-in Manager.
    * Browse for "gfTools > plug-ins > dev > python"
    * Find gfTools_P.py and import it.

Requirements:
    * Maya 2017 or above.

Todo:
    * Add commands to generate/read settings for the application
    * Binary file or json file?

Sources:
    * https://docs.python.org/3/reference/datamodel.html#special-method-names

This code supports Pylint. Rc file in project.
"""
import sys
import os
from collections import OrderedDict

if sys.version_info.major >= 3:
    import pickle
else:
    import cPickle as pickle

from gfUtilitiesBelt.core import appInfo
from gfUtilitiesBelt.core import getMayaInfo
reload(appInfo)
reload(getMayaInfo)


kPocketFileExt = ".gfpocket"




class Pocket(object):
    """
    Read, write and perform operations between Pockets.

    Constructors:

    Pocket(name)             | name - str\n
    Pocket(name, tools)      | name - str; tools - list of strings\n

    Sequence Support:

    An Pocket is treated like a sequence of n string tools. ["This", "is", "a", "tool"].
    len() returns the number of tools present in this class instance.
    Indexing is supported but element assignment not.

    Number Support:

    Pocket = Pocket + Pocket | Concatenate tools from one Pocket to another.\n
    Pocket += Pocket         | Concatenate tools from one Pocket to another.\n
    Pocket = Pocket - Pocket | Remove tools from one Pocket to another.\n
    Pocket -= Pocket         | Remove tools from one Pocket to another.\n

    Comparison Support:

    Pocket == Pocket         | Returns True if tool list from one Pocket is exactly equal to another Pocket.\n
    Pocket != Pocket         | Returns False if tool list from one Pocket is not exactly equal to another Pocket.
    """

    ####################################
    # INIT METHODS

    def __init__(self, name, tools=None):
        """Constructor."""
        self.mayaVersion = appInfo.kMayaVersion
        self.filePath = None
        self.name = name
        self.tools = tools
        if self.tools is None:
            self.tools = []

    def __repr__(self):
        """Repr."""
        return "%s.core.pockets.Pocket(name='%s', tools=%s)" %(appInfo.kApplicationName, str(self.name), str(self.tools))

    def __str__(self):
        """Str."""
        return str(self.tools)


    ####################################
    # CONTENT METHODS

    def __len__(self):
        """How much tools is in this pocket."""
        return len(self.tools)

    def __contains__(self, tool):
        """If this pocket contains this tool."""
        if isinstance(tool, str):
            return tool in self.tools
        else:
            raise TypeError("Tool must be an string.")

    def __getitem__(self, key):
        """Retrieve a pocket tool by index."""
        if isinstance(key, int):
            pocketLen = len(self) - 1
            if key <= pocketLen:
                return self.tools[key]
            else:
                raise IndexError("List index out of range.")
        else:
            raise TypeError("Key index must be an integer.")

    def __delitem__(self, key):
        """Delete a pocket tool by index."""
        if isinstance(key, int):
            pocketLen = len(self) - 1
            if key <= pocketLen:
                del self.tools[key]
            else:
                raise IndexError("List index out of range.")
        else:
            raise TypeError("Key index must be an integer.")

    def __add__(self, otherPocket):
        """Concatenate content from another pocket to this pocket."""
        newTools = [tool for tool in self.tools]
        if isinstance(otherPocket, self):
            newTools = list(dict.fromkeys(newTools.extend(otherPocket.tools)))
            return Pocket(self.name, newTools)
        else:
            raise TypeError("Cannot add Pocket to another type object.")

    def __iadd__(self, otherPocket):
        """Concatenate content from another pocket to this pocket."""
        if isinstance(otherPocket, self):
            return self + otherPocket
        else:
            raise TypeError("Cannot add Pocket to another type object.")

    def __sub__(self, otherPocket):
        """Remove content from another pocket to this pocket."""
        if isinstance(otherPocket, self):
            newTools = [tool for tool in self.tools if tool not in otherPocket.tools]
            return Pocket(self.name, newTools)
        else:
            raise TypeError("Cannot subtract Pocket to another type object.")

    def __isub__(self, otherPocket):
        """Remove content from another pocket to this pocket."""
        if isinstance(otherPocket, self):
            return self - otherPocket
        else:
            raise TypeError("Cannot subtract Pocket to another type object.")


    ####################################
    # COMPARISON METHODS

    def __eq__(self, otherPocket):
        """If this pocket is equal to another pocket."""
        if isinstance(otherPocket, self):
            return self.tools == otherPocket.tools
        else:
            raise TypeError("Cannot compare Pocket to another type object.")

    def __ne__(self, otherPocket):
        """If this pocket is not equal to another pocket."""
        if isinstance(otherPocket, self):
            return self.tools != otherPocket.tools
        else:
            raise TypeError("Cannot compare Pocket to another type object.")

    def __lt__(self, otherPocket):
        """If this pocket size is small than another pocket."""
        if isinstance(otherPocket, self):
            return len(self) < len(otherPocket)
        else:
            raise TypeError("Cannot compare Pocket to another type object.")

    def __le__(self, otherPocket):
        """If this pocket size is small or equal to another pocket."""
        if isinstance(otherPocket, self):
            return len(self) <= len(otherPocket)
        else:
            raise TypeError("Cannot compare Pocket to another type object.")

    def __gt__(self, otherPocket):
        """If this pocket size is bigger than another pocket."""
        if isinstance(otherPocket, self):
            return len(self) > len(otherPocket)
        else:
            raise TypeError("Cannot compare Pocket to another type object.")

    def __ge__(self, otherPocket):
        """If this pocket size is bigger or equal to another pocket."""
        if isinstance(otherPocket, self):
            return len(self) >= len(otherPocket)
        else:
            raise TypeError("Cannot compare Pocket to another type object.")


    ####################################
    # CLASS METHODS

    @classmethod
    def fromFile(cls, filepath):
        """Create a Pocket instance from a Pocket file.

        Args:
            filepath (str): The path where the file is.

        Returns:
            Pocket: The Pocket instance with all information.

        Raises:
            RuntimeError: If the file is not recognized.
        """
        status = cls.checkFile(filepath)
        if not status:
            raise RuntimeError("File %s was not recognized." % os.path.basename(filepath))
        with open(filepath, "rb") as f:
            content = pickle.load(f)
        newPocket = cls(content["Name"], content["Tools"])
        newPocket.mayaVersion = content["Maya Version"]
        newPocket.filePath = filepath
        return newPocket


    ####################################
    # STATIC METHODS

    @staticmethod
    def checkFile(filepath):
        """Check if the file specified is a Pocket file.

        Args:
            filepath (str): The filepath of the Pocket file.

        Returns:
            True or False: True if the file is valid or False if is not.
        """
        fileName = os.path.basename(filepath)
        # 1- Check if the file have the right extension: .gfpocket.
        if not fileName.upper().endswith(kPocketFileExt.upper()):
            return False
        try:
            with open(filepath, "rb") as f:
                content = pickle.load(f)
            # 2- Check if application name is right inside the file.
            if content["Application"] != appInfo.kApplicationName:
                return False
            # 3- Check if the file version is compatible with application version.
            status = appInfo.checkVersion(content["Version"])
            if not status:
                return False
            # 4- Check if the Maya version is greater or equal the current Maya version.
            status = appInfo.checkMayaVersion(content["Maya Version"])
            if not status:
                sys.stdout.write("[%s] The pocket %s was created in a newest Maya version. You may notice some unexpected results." % (appInfo.kApplicationName, fileName))
            # 5- Check if tools are valid Maya tools or valid custom tools.
            # TODO: Review this. Return False here?
            mayaData = getMayaInfo.readMayaInfoFile()
            for tool in content["Tools"]:
                if tool not in mayaData.keys():
                    sys.stdout.write("[%s] The tool %s was not recognized as a Maya valid tool. You may notice some unexpected results." % (appInfo.kApplicationName, tool))
        except Exception:
            return False
        return True


    ####################################
    # REGULAR METHODS

    def writeFile(self, output):
        """Write a gfpocket file with all the informations about a Pocket.

        Args:
            output (str): The path to save the file.

        Returns:
            True: If succeeded.
        """
        content = OrderedDict()
        content["Application"] = appInfo.kApplicationName
        content["Version"] = appInfo.kApplicationVersion
        content["Maya Version"] = self.mayaVersion
        content["Name"] = self.name
        content["Tools"] = self.tools
        with open(output, "wb") as f:
            pickle.dump(content, f, pickle.HIGHEST_PROTOCOL)
        return True


    def readFile(self, filepath):
        """Read the gfpocket file with all the informations about a Pocket.

        Args:
            filepath (str): The path where the file is.

        Returns:
            Pocket: The Pocket instance with all information.

        Raises:
            RuntimeError: If the file is not recognized.
        """
        status = self.checkFile(filepath)
        if not status:
            raise RuntimeError("File %s was not recognized." % filepath)
        with open(filepath, "rb") as f:
            content = pickle.load(f)
        newPocket = Pocket(content["Name"], content["Tools"])
        newPocket.mayaVersion = content["Maya Version"]
        newPocket.filePath = filepath
        return newPocket


    def deletePocket(self):
        pass


    def addTool(self):
        pass


    def removeTool(self):
        pass


    def moveToolUp(self):
        pass


    def moveToolDown(self):
        pass

