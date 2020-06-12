# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Giuliano França

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

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

Sources:
    * https://docs.python.org/3/reference/datamodel.html#special-method-names

This code supports Pylint. Rc file in project.
"""
import os
import collections
import maya.cmds as cmds


kPocketFileExt = ".pocket"


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
        self.mayaVersion = cmds.about(v=True)
        self.name = name
        self.tools = tools
        if self.tools is None:
            self.tools = []

    def __repr__(self):
        """Repr."""
        return "%s(name='%s', tools=%s)" %(self.__class__, str(self.name), str(self.tools))

    def __str__(self):
        """Str."""
        return self.name


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
    def fromFile(cls):
        pass


    ####################################
    # STATIC METHODS


    ####################################
    # REGULAR METHODS

    def writeFile(self):
        # Create in which maya version?
        pass

    def readFile(self):
        pass

    def deletePocket(self):
        pass

    def addTool(self):
        pass

    def removeTool(self):
        pass

    def reorderTools(self):
        pass

