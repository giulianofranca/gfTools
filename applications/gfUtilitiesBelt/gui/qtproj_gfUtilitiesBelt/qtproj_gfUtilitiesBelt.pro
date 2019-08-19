#-------------------------------------------------
#
# Project created by QtCreator 2019-04-03T15:25:07
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = qtproj_gfUtilitiesBelt
TEMPLATE = app


SOURCES += main.cpp\
        gfutilitiesbelt_main.cpp \
    gfutilitiesbelt_addpocket.cpp \
    gfutilitiesbelt_editpocket.cpp \
    gfutilitiesbelt_createtool.cpp

HEADERS  += gfutilitiesbelt_main.h \
    gfutilitiesbelt_addpocket.h \
    gfutilitiesbelt_editpocket.h \
    gfutilitiesbelt_createtool.h

FORMS    += gfutilitiesbelt_main.ui \
    gfutilitiesbelt_addpocket.ui \
    gfutilitiesbelt_editpocket.ui \
    gfutilitiesbelt_createtool.ui

RESOURCES += \
    gfutilitiesbelt_main.qrc
