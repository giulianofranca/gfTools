import os
import logging
import datetime
import maya.cmds as cmds

currentPath = os.getcwd()
user = os.getenv('USERNAME')
logPath = 'C:/Users/%s/Documents/maya/2017/scripts/gfTools/gfRigSystem/utils'%(user)
logger = logging.getLogger('gfRigSystem')

def enableLog(enable=True, preserve=False):
    os.chdir(logPath)
    allHandlers = list(logger.handlers)
    if enable == True:
        if allHandlers == []:
            logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(name)s] [%(levelname)s]: %(message)s')
            fileHandler = logging.FileHandler('gfRigSystemAPI.log')
            fileHandler.setFormatter(formatter)
            fileHandler.setLevel(logging.DEBUG)
            logger.addHandler(fileHandler)
            writeLog(t='info', msg='Log catcher initialized.')
        else: writeLog(t='warning', msg='Log catcher already enabled.')
    else:
        if not allHandlers == []:
            if preserve == True: writeLog(t='info', msg='Log catcher paused.')
            for i in allHandlers:
                logger.removeHandler(i)
                i.flush()
                i.close()
            if preserve == False:
                if os.path.isfile('gfRigSystemAPI.log'):
                    os.remove('gfRigSystemAPI.log')
                writeLog(t='info', msg='Log catcher disabled.')
        else: writeLog(t='warning', msg='Log catcher already disabled.')
    os.chdir(currentPath)

def checkLog(write=False):
    allHandlers = list(logger.handlers)
    if allHandlers == []:
        if write == True: print('Log catcher is disabled.')
        return False
    else:
        if write == True: writeLog(t='info', msg='Log catcher is enabled.')
        return True

def writeLog(msg, t):
    log = checkLog()
    if log == True:
        if t.lower() == 'debug': logger.debug(msg)
        elif t.lower() == 'info': logger.info(msg)
        elif t.lower() == 'warning': logger.warning(msg)
        elif t.lower() == 'error': logger.error(msg)
        else: logger.error("Log type don't recognized! Available types (debug, info, warning, error).")
    else:
        if t.lower() == 'debug': print(msg)
        elif t.lower() == 'info': print(msg)
        elif t.lower() == 'warning': cmds.warning(msg)
        elif t.lower() == 'error': cmds.error(msg, sl=False, n=False)
        else: print("Log type don't recognized! Available types (debug, info, warning, error).")

def exportFile(fullPath):
    fileName = fullPath.split('/')[-1]
    path = fullPath.split('/')
    path.remove(fileName)
    path = '/'.join(path)
    if os.path.isdir(path):
        os.chdir(logPath)
        lines = []
        writeLog(t='info', msg='Log file exported successfully to (%s)\n'%(fullPath))
        with open('gfRigSystemAPI.log', 'r') as mainFile:
            lines.append(mainFile.readlines())
        os.chdir(path)
        os.chdir(path)
        if os.path.isfile(fileName):
            with open(fileName, 'a') as logFile:
                for x in range(len(lines[0])):
                    logFile.write(lines[0][x])
        else:
            with open(fileName, 'w') as logFile:
                for x in range(len(lines[0])):
                    logFile.write(lines[0][x])
    os.chdir(currentPath)
    return True
