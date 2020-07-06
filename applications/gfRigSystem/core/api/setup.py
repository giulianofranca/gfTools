"""
Setup.py is the build script

python setup.py build
"""

import sys
import os
import platform
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    """ CMake Extension Class """
    def __init__(self, name, cmakeListsDir=".", sources=[], **kwa):
        # pylint: disable=dangerous-default-value
        Extension.__init__(self, name, sources=sources, **kwa)
        self.cmakeListsDir = os.path.abspath(cmakeListsDir)


class CMakeBuildExt(build_ext):
    """ Build class """
    def build_extensions(self):
        # Ensure that CMake is present and working
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("Cannot find CMake executable")

        for ext in self.extensions:
            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
            # cfg = "Debug" if options["--debug"] == "ON" else "Release"
            cfg = "Release"

            cmakeArgs = [
                '-DCMAKE_BUILD_TYPE=%s' % cfg,
                # Ask CMake to place the resulting lib in the directory containing the extension
                '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_%s=%s' % (cfg.upper(), extdir),
                # Other intermediate static libraries are placed in a temporary build directory instead
                '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_%s=%s' % (cfg.upper(), self.build_temp),
                # Hint CMake to use the same Python executable that is launching the build, prevents possible mismatching
                # if multiple versions of Python are installed
                '-DPYTHON_EXECUTABLE=%s' % sys.executable
                # Add other project-specific CMake arguments if needed
            ]

            # We can handle some platform-specific settings at our discretion
            if platform.system() == "Windows":
                plat = ("x64" if platform.architecture()[0] == "64bit" else "Win32")
                cmakeArgs += [
                    # These options are likely to be needed under Windows
                    "-DCMAKE_WINDOWS_EXPORT_ALL_SYMBOLS=TRUE",
                    "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_%s=%s" % (cfg.upper(), extdir)
                ]
                # Assuming that Visual Studio and MinGW are supported compilers
                if self.compiler.compiler_type == "msvc":
                    cmakeArgs += [
                        "-DCMAKE_GENERATOR_PLATFORM=%s" % plat
                    ]
                else:
                    cmakeArgs += [
                        "-G", "MinGW Makefiles"
                    ]

            # cmakeArgs += cmake_cmd_args

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config
            subprocess.check_call(["cmake", ext.cmakeListsDir] + cmakeArgs, cwd=self.build_temp)

            # Build
            subprocess.check_call(["cmake", "--build", ".", "--config", cfg], cwd=self.build_temp)


sourceFiles = [
    "source/main.cpp"
    "source/headers/utils.h"
    "source/utils.cpp"
    "source/headers/testClass.h"
    "source/testClass.cpp"
]

module = CMakeExtension("_gfRigSystemAPI", sources=sourceFiles)

setup(
    name="_gfRigSystemAPI",
    version="0.1.0",
    ext_modules=[module],
    cmdclass={'build_ext':CMakeBuildExt}
)
