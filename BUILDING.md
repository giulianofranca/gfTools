# Build gfTools

This is the documentation on how to build gfTools from source code.

## Build Dependencies
* C++ Compiler
* [CMake](https://cmake.org/download/)
* [Maya Devkit](https://www.autodesk.com/developer-network/platform-technologies/maya)
* [Qt](https://www.qt.io/download-open-source)
* [Python 2.7](https://www.python.org/downloads/)
* [Doxygen](https://www.doxygen.nl/download.html)
* [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page)
* [Pybind11](https://github.com/pybind/pybind11/releases)
* [Ninja](https://github.com/ninja-build/ninja/releases) (Optional)

> **Note:** The python build script will download and install Pybind11 and Eigen automatically. You can pass --ignore-dependencies flag to tell the python script you will install these libraries manually.

## Configure Steps

1. Getting the source code

        git clone https://github.com/giuliano-franca/gfTools.git
        cd gfTools

2. Installing the dependencies
    - **Linux**
        1. Setting up C++ environment.

            For Linux we are gonna use gcc as the C++ compiler. To setup the build environment type the following commands on your terminal:

            Fedora, CentOS

                sudo dnf groupinstall "Development Tools"
                sudo dnf groupinstall "Development Libraries"
                sudo dnf install gcc gcc-c++ make automake cmake doxygen ninja-build

            > **Note:** These commands will install the optional dependency Ninja. If you don't want to use Ninja just skip `ninja-build` in the command line.

        2. Setting up Python environment.

            We need to install Python 2.7 to build the Python bindings. We need version 2.7 to be able to use the bindings within Maya.

            To setup Python 2.7 enviroment run the following command on your terminal:

            Fedora, CentOS

                sudo dnf install python27
                sudo python2.7 -m ensurepip
                sudo python2.7 -m pip install --upgrade pip
            
            > **Note:** If your system ships with Python 2.7 you can skip this block.
        
        3. Getting and installing Maya Devkit.

            Go to [Maya Development Center website](https://www.autodesk.com/developer-network/platform-technologies/maya) and download the devkit for your Maya version.

            Extract the .tgz file inside your Autodesk Maya installation directory. (Normally is /usr/autodesk/maya\<version>). You shoud then get a filetree like this: /usr/autodesk/maya2019/devkitBase

            Inside your extracted devkitBase folder, go to cmake folder and extract the Qt CMake .tar.gz file inside it.

            Back to your extracted devkitBase folder, go to include folder and extract all the.tgz files inside it. (Should be pyside2, qt and shiboken2)

            Finally, go back to your extracted devkitBase folder, inside mkspecs, extract the qt mkspecs .tar.gz file inside it.

            Done! You installed Maya Devkit.

        4. Getting Qt Open Source.

            In the [Qt Open Source website](https://www.qt.io/download-open-source), go to offline installers and download the Qt version compatible with your Maya version.

            | Maya 	| 2018  	| 2019  	| 2020   	|
            |------	|-------	|-------	|--------	|
            | Qt   	| 5.6.1 	| 5.6.1 	| 5.12.5 	|

            Follow the instructions of the Qt Installer.

            After installation, add the Qt lib and bin directory to your LD_LIBRARY_PATH and PATH environment variables respectively.

            Fedora

                echo 'export PATH="/opt/Qt5.12.5/5.12.5/gcc_64/bin:$PATH"' >> ~/.bashrc
                echo 'export LD_LIBRARY_PATH="/opt/Qt5.12.5/5.12.5/gcc_64/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc

            > **Note:** Change the paths above to the paths where you installed Qt.

            > **Note:** Here I'm using .bashrc file to store environment variables on my Fedora 32 system. Can be another filename in other Linux distributions.

        5. Done! You can build gfTools!
        - TODO: Add ubuntu/debian based commands examples.
    - **Windows**
        - TODO: Show how to setup Windows environment
    - **MacOS**
        - TODO: Show how to setup MacOS environment

## Build with Python script

- TODO: Show how to build with Python script.
- TODO: Show script arguments.

## Build with CMake

- TODO: Show how to install Pybind11 and Eigen manually.
- TODO: Show how to build with CMake.


<!-- For Windows we are gonna use Visual Studio as the C++ compiler. You can download and install Visual Studio [here](https://visualstudio.microsoft.com/pt-br/vs/older-downloads/) (Recommended version 2017 community). -->