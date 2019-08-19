import sys
from PySide2 import QtCore, QtGui, QtWidgets

################################################################################################################################################################
######### IntSliderGrp
################################################################################################################################################################
class WidIntSliderGrp(QtWidgets.QWidget):

    def __init__(self, name, min, max, val):
        super(WidIntSliderGrp, self).__init__()
        self.name = name
        self.widgetName = 'widIntSlider_' + name.replace(" ", "")
        self.min = min
        self.max = max
        self.val = val
        self.setupUi()
        self.configure()

    def configure(self):
        # Validator
        self.valIntSlider = QtGui.QIntValidator(self.min, self.max, self)
        self.txtIntSlider.setValidator(self.valIntSlider)
        # Configs
        self.sldIntSlider.setRange(self.min, self.max)
        self.sldIntSlider.setValue(self.val)
        self.txtIntSlider.setText(str(self.val))
        # Signals
        self.sldIntSlider.sliderMoved.connect(self.sliderChanged)
        self.txtIntSlider.editingFinished.connect(self.textChanged)

    def sliderChanged(self):
        val = self.sldIntSlider.value()
        self.txtIntSlider.setText(str(val))

    def textChanged(self):
        val = int(self.txtIntSlider.text())
        self.sldIntSlider.setValue(val)

    def getValue(self):
        return int(self.txtIntSlider.text())

    def setupUi(self):
        self.setObjectName(self.widgetName)
        self.resize(400, 40)
        self.layWidIntSlider = QtWidgets.QVBoxLayout(self)
        self.layWidIntSlider.setContentsMargins(5, 5, 5, 5)
        self.layWidIntSlider.setSpacing(5)
        self.layWidIntSlider.setObjectName("layWidIntSlider")
        self.frmIntSlider = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmIntSlider.sizePolicy().hasHeightForWidth())
        self.frmIntSlider.setSizePolicy(sizePolicy)
        self.frmIntSlider.setMinimumSize(QtCore.QSize(0, 30))
        self.frmIntSlider.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frmIntSlider.setObjectName("frmIntSlider")
        self.layIntSlider = QtWidgets.QHBoxLayout(self.frmIntSlider)
        self.layIntSlider.setContentsMargins(5, 5, 5, 5)
        self.layIntSlider.setSpacing(10)
        self.layIntSlider.setObjectName("layIntSlider")
        self.lblIntSlider = QtWidgets.QLabel(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblIntSlider.sizePolicy().hasHeightForWidth())
        self.lblIntSlider.setSizePolicy(sizePolicy)
        self.lblIntSlider.setMinimumSize(QtCore.QSize(120, 0))
        self.lblIntSlider.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblIntSlider.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblIntSlider.setObjectName("lblIntSlider")
        self.layIntSlider.addWidget(self.lblIntSlider)
        self.txtIntSlider = QtWidgets.QLineEdit(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtIntSlider.sizePolicy().hasHeightForWidth())
        self.txtIntSlider.setSizePolicy(sizePolicy)
        self.txtIntSlider.setMinimumSize(QtCore.QSize(60, 0))
        self.txtIntSlider.setMaximumSize(QtCore.QSize(60, 16777215))
        self.txtIntSlider.setObjectName("txtIntSlider")
        self.layIntSlider.addWidget(self.txtIntSlider)
        self.sldIntSlider = QtWidgets.QSlider(self.frmIntSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sldIntSlider.sizePolicy().hasHeightForWidth())
        self.sldIntSlider.setSizePolicy(sizePolicy)
        self.sldIntSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.sldIntSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sldIntSlider.setObjectName("sldIntSlider")
        self.layIntSlider.addWidget(self.sldIntSlider)
        self.layWidIntSlider.addWidget(self.frmIntSlider)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(self.widgetName, self.widgetName))
        self.lblIntSlider.setText(_translate(self.widgetName, self.name))

################################################################################################################################################################
######### FloatSliderGrp
################################################################################################################################################################
class WidFloatSliderGrp(QtWidgets.QWidget):

    def __init__(self, name, min, max, val):
        super(WidFloatSliderGrp, self).__init__()
        self.name = name
        self.widgetName = 'widFltSlider_' + name.replace(" ", "")
        self.min = min
        self.max = max
        self.val = val
        self.setupUi()
        self.configure()

    def configure(self):
        # Validator
        self.valFltSlider = QtGui.QDoubleValidator()
        self.valFltSlider.setDecimals(2)
        self.txtFltSlider.setValidator(self.valFltSlider)
        # Configs
        self.txtFltSlider.setText("%0.2f" % float(self.val))
        self.sldFltSlider.setRange(self.min, self.max * 100)
        sliderVal = float(self.txtFltSlider.text())*100
        self.sldFltSlider.setValue(int(sliderVal))
        # Signals
        self.sldFltSlider.sliderMoved.connect(self.sliderChanged)
        self.txtFltSlider.editingFinished.connect(self.textChanged)

    def fit(self, val, oldMin, oldMax, newMin=0.0, newMax=1.0):
        scale = (float(val) - oldMin) / (oldMax - oldMin)
        newRange = scale * (newMax - newMin)
        if newMin < newMax:
            return newMin + newRange
        else:
            return newMin - newRange

    def sliderChanged(self):
        val = self.sldFltSlider.value()
        newVal = self.fit(val, self.sldFltSlider.minimum(), self.sldFltSlider.maximum(),
            float(str(self.min)+'.0'), float(str(self.max)+'.0'))
        self.txtFltSlider.setText("%0.2f" % (newVal))

    def textChanged(self):
        val = float(self.txtFltSlider.text())*100
        self.sldFltSlider.setValue(int(val))

    def getValue(self):
        return float(self.txtFltSlider.text())

    def setupUi(self):
        self.setObjectName(self.widgetName)
        self.resize(400, 40)
        self.layWidFltSlider = QtWidgets.QVBoxLayout(self)
        self.layWidFltSlider.setContentsMargins(5, 5, 5, 5)
        self.layWidFltSlider.setSpacing(5)
        self.layWidFltSlider.setObjectName("layWidFltSlider")
        self.frmFltSlider = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmFltSlider.sizePolicy().hasHeightForWidth())
        self.frmFltSlider.setSizePolicy(sizePolicy)
        self.frmFltSlider.setMinimumSize(QtCore.QSize(0, 30))
        self.frmFltSlider.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frmFltSlider.setObjectName("frmFltSlider")
        self.layFltSlider = QtWidgets.QHBoxLayout(self.frmFltSlider)
        self.layFltSlider.setContentsMargins(5, 5, 5, 5)
        self.layFltSlider.setSpacing(10)
        self.layFltSlider.setObjectName("layFltSlider")
        self.lblFltSlider = QtWidgets.QLabel(self.frmFltSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFltSlider.sizePolicy().hasHeightForWidth())
        self.lblFltSlider.setSizePolicy(sizePolicy)
        self.lblFltSlider.setMinimumSize(QtCore.QSize(120, 0))
        self.lblFltSlider.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblFltSlider.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblFltSlider.setObjectName("lblFltSlider")
        self.layFltSlider.addWidget(self.lblFltSlider)
        self.txtFltSlider = QtWidgets.QLineEdit(self.frmFltSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtFltSlider.sizePolicy().hasHeightForWidth())
        self.txtFltSlider.setSizePolicy(sizePolicy)
        self.txtFltSlider.setMinimumSize(QtCore.QSize(60, 0))
        self.txtFltSlider.setMaximumSize(QtCore.QSize(60, 16777215))
        self.txtFltSlider.setObjectName("txtFltSlider")
        self.layFltSlider.addWidget(self.txtFltSlider)
        self.sldFltSlider = QtWidgets.QSlider(self.frmFltSlider)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sldFltSlider.sizePolicy().hasHeightForWidth())
        self.sldFltSlider.setSizePolicy(sizePolicy)
        self.sldFltSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.sldFltSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sldFltSlider.setObjectName("sldFltSlider")
        self.layFltSlider.addWidget(self.sldFltSlider)
        self.layWidFltSlider.addWidget(self.frmFltSlider)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(self.widgetName, self.widgetName))
        self.lblFltSlider.setText(_translate(self.widgetName, self.name))

################################################################################################################################################################
######### RadioBtnGrp
################################################################################################################################################################
class WidRadioBtnGrp(QtWidgets.QWidget):

    def __init__(self, name, num, text):
        super(WidRadioBtnGrp, self).__init__()
        self.name = name
        self.widgetName = 'widRadBtnGrp_' + name.replace(" ", "")
        self.num = num
        self.text = text
        self.rads = []
        self.setupUi()

    def configure(self):
        pass

    def setupUi(self):
        self.setObjectName(self.widgetName)
        self.resize(404, 40)
        self.layWidRadioBtnGrp = QtWidgets.QVBoxLayout(self)
        self.layWidRadioBtnGrp.setContentsMargins(5, 5, 5, 5)
        self.layWidRadioBtnGrp.setSpacing(5)
        self.layWidRadioBtnGrp.setObjectName("layWidRadioBtnGrp")
        self.frmRadioBtnGrp = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frmRadioBtnGrp.sizePolicy().hasHeightForWidth())
        self.frmRadioBtnGrp.setSizePolicy(sizePolicy)
        self.frmRadioBtnGrp.setMinimumSize(QtCore.QSize(0, 30))
        self.frmRadioBtnGrp.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frmRadioBtnGrp.setObjectName("frmRadioBtnGrp")
        self.layRadioBtnGrp = QtWidgets.QHBoxLayout(self.frmRadioBtnGrp)
        self.layRadioBtnGrp.setContentsMargins(5, 5, 5, 5)
        self.layRadioBtnGrp.setSpacing(10)
        self.layRadioBtnGrp.setObjectName("layRadioBtnGrp")
        self.lblRadioBtnGrp = QtWidgets.QLabel(self.frmRadioBtnGrp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRadioBtnGrp.sizePolicy().hasHeightForWidth())
        self.lblRadioBtnGrp.setSizePolicy(sizePolicy)
        self.lblRadioBtnGrp.setMinimumSize(QtCore.QSize(120, 0))
        self.lblRadioBtnGrp.setMaximumSize(QtCore.QSize(120, 16777215))
        self.lblRadioBtnGrp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRadioBtnGrp.setObjectName("lblRadioBtnGrp")
        self.layRadioBtnGrp.addWidget(self.lblRadioBtnGrp)
        for x in range(self.num):
            self.radRadioBtn = QtWidgets.QRadioButton(self.frmRadioBtnGrp)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.radRadioBtn.sizePolicy().hasHeightForWidth())
            self.radRadioBtn.setSizePolicy(sizePolicy)
            self.radRadioBtn.setObjectName("rad%s_%s" % (self.name.replace(" ", ""), str(x + 1)))
            self.radRadioBtn.setText(self.text[x])
            self.layRadioBtnGrp.addWidget(self.radRadioBtn)
            self.rads.append(self.radRadioBtn)
        self.rads[0].setChecked(True)
        self.layWidRadioBtnGrp.addWidget(self.frmRadioBtnGrp)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate(self.widgetName, self.widgetName))
        self.lblRadioBtnGrp.setText(_translate(self.widgetName, self.name))

################################################################################################################################################################
################################################################################################################################################################
######### Test Call Widget
################################################################################################################################################################
################################################################################################################################################################
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Int Slider Group
    # intSld = WidIntSliderGrp(name='Test Slider', min=0, max=200, val=50)
    # intSld.show()

    # Float Slider Grp
    # fltSld = WidFloatSliderGrp(name='Test Slider', min=0, max=10, val=0)
    # fltSld.show()

    # Radio Button Grp
    radGrp = WidRadioBtnGrp(name='Test Radio', num=3, text=['Xunda', 'Rola', 'Meu Caralho todo', 'Minha pica'])
    radGrp.show()
    for x in range(len(radGrp.rads)):
        print(radGrp.rads[x].objectName())
    sys.exit(app.exec_())
