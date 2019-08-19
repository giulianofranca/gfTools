import sys
from PySide2 import QtWidgets, QtGui, QtCore


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        self._title = 'PySide2 Window'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()



class WindowDrawRectangle(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowDrawRectangle, self).__init__()

        self._title = 'PySide2 Drawing Rectangle'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(35, 25, 0), 5, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(112, 0, 32), QtCore.Qt.DiagCrossPattern))

        painter.drawRect(100, 15, 400, 200)



class WindowDrawEllipse(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowDrawEllipse, self).__init__()

        self._title = 'PySide2 Drawing Ellipse'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(35, 25, 0), 5, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(112, 0, 32), QtCore.Qt.DiagCrossPattern))

        painter.drawEllipse(100, 15, 400, 200)



class WindowBrushStyles(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowBrushStyles, self).__init__()

        self._title = 'PySide2 Brush Styles'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        # [QPEN STYLES] SolidLine | DashLine | DotLine | DashDotLine | DashDotDotLine
        # [QBRUSH STYLES] SolidPattern | DiagCrossPattern | Dense1-7Pattern | HorPattern | VerPattern | BDiagPattern
        painter.setPen(QtGui.QPen(QtGui.QColor(202, 156, 34), 2.5, QtCore.Qt.DashDotDotLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(194, 230, 55), QtCore.Qt.DiagCrossPattern))
        painter.drawRect(15, 15, 150, 100)

        painter.setPen(QtGui.QPen(QtGui.QColor(22, 78, 234), 2.5, QtCore.Qt.DashLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(10, 150, 212), QtCore.Qt.Dense1Pattern))
        painter.drawRect(185, 15, 150, 100)

        painter.setPen(QtGui.QPen(QtGui.QColor(19, 150, 89), 2.5, QtCore.Qt.DotLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(31, 192, 124), QtCore.Qt.HorPattern))
        painter.drawRect(355, 15, 150, 100)

        painter.setPen(QtGui.QPen(QtGui.QColor(198, 33, 41), 2.5, QtCore.Qt.DashDotLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(169, 10, 24), QtCore.Qt.VerPattern))
        painter.drawRect(15, 135, 150, 100)

        painter.setPen(QtGui.QPen(QtGui.QColor(198, 100, 41), 2.5, QtCore.Qt.SolidLine))
        painter.setBrush(QtGui.QBrush(QtGui.QColor(169, 98, 24), QtCore.Qt.BDiagPattern))
        painter.drawRect(185, 135, 150, 100)



class WindowDrawPolygon(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowDrawPolygon, self).__init__()

        self._title = 'PySide2 Drawing Polygon'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        startPnt = QtCore.QPoint(250, 30)
        endPnt = QtCore.QPoint(350, 30)
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor(202, 156, 34))
        pen.setWidth(8)
        pen.setJoinStyle(QtCore.Qt.MiterJoin) # MiterJoin
        pen.setStyle(QtCore.Qt.SolidLine)
        pen.setCapStyle(QtCore.Qt.FlatCap) # SquareCap
        painter.setPen(pen)

        poly = QtGui.QPolygon(
            [QtCore.QPoint(10, 10),
            QtCore.QPoint(10, 200),
            QtCore.QPoint(200, 10),
            QtCore.QPoint(200, 200)]
        )
        path = QtGui.QPainterPath()
        path.addPolygon(poly)
        painter.drawPolygon(poly)
        painter.fillPath(path, QtGui.QBrush(QtGui.QColor(100, 100, 100), QtCore.Qt.DiagCrossPattern))

        painter.drawLine(startPnt, endPnt)
        startPnt.setY(50)
        endPnt.setY(50)
        pen.setCapStyle(QtCore.Qt.SquareCap)
        painter.setPen(pen)
        painter.drawLine(startPnt, endPnt)
        startPnt.setY(70)
        endPnt.setY(70)
        pen.setCapStyle(QtCore.Qt.RoundCap)
        painter.setPen(pen)
        painter.drawLine(startPnt, endPnt)



class WindowLinearGradient(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowLinearGradient, self).__init__()

        self._title = 'PySide2 Linear Gradient'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 2.5, QtCore.Qt.SolidLine))

        grad1 = QtGui.QLinearGradient(35, 35, 185, 185) # 40, 115, 150, 175
        grad1.setColorAt(0.0, QtGui.QColor(169, 10, 24))
        grad1.setColorAt(0.5, QtGui.QColor(31, 192, 124))
        grad1.setColorAt(1.0, QtGui.QColor(194, 230, 55))

        painter.setBrush(QtGui.QBrush(grad1))

        painter.drawRoundedRect(15, 15, 200, 200, 25, 25)



class WindowRadialGradient(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowRadialGradient, self).__init__()

        self._title = 'PySide2 Radial Gradient'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 2.5, QtCore.Qt.SolidLine))

        grad2 = QtGui.QRadialGradient(QtCore.QPoint(115, 115), 100)
        grad2.setColorAt(0.0, QtGui.QColor(169, 10, 24))
        grad2.setColorAt(0.5, QtGui.QColor(31, 192, 124))
        grad2.setColorAt(1.0, QtGui.QColor(194, 230, 55))

        painter.setBrush(QtGui.QBrush(grad2))
        painter.drawRoundedRect(15, 15, 200, 200, 25, 25)



class WindowConicalGradient(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowConicalGradient, self).__init__()

        self._title = 'PySide2 Conical Gradient'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)
        self.show()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtGui.QPen(QtGui.QColor(100, 100, 100), 2.5, QtCore.Qt.SolidLine))

        grad3 = QtGui.QConicalGradient(QtCore.QPoint(115, 115), 10)
        grad3.setColorAt(0.0, QtGui.QColor(169, 10, 24))
        grad3.setColorAt(0.5, QtGui.QColor(31, 192, 124))
        grad3.setColorAt(1.0, QtGui.QColor(194, 230, 55))

        painter.setBrush(QtGui.QBrush(grad3))
        painter.drawRoundedRect(15, 15, 200, 200, 25, 25)



class WindowGraphicsView(QtWidgets.QMainWindow):

    def __init__(self):
        super(WindowGraphicsView, self).__init__()

        self._title = 'PySide2 Graphics View'
        self._top = 100
        self._left = 100
        self._width = 680
        self._height = 500

        self.InitWindow()

    def InitWindow(self):
        scene = QtWidgets.QGraphicsScene()
        scene.addText('Hello World!')

        redBrush = QtGui.QBrush(QtCore.Qt.red)
        blueBrush = QtGui.QBrush(QtCore.Qt.blue)
        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(7)

        circle = scene.addEllipse(10, 10, 200, 200, blackPen, redBrush)

        view = QtWidgets.QGraphicsView(scene)
        view.setGeometry(0, 0, 680, 500)
        view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        view.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        view.show()
        self.app.exec_()

        self.setWindowTitle(self._title)
        self.setGeometry(self._top, self._left, self._width, self._height)

    # def paintEvent(self, event):
    #     painter = QtGui.QPainter(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     pen = QtGui.QPen(QtGui.QColor(100, 100, 100))
    #     pen.setWidth(2.5)
    #     pen.setJoinStyle(QtCore.Qt.RoundJoin)
    #     pen.setCapStyle(QtCore.Qt.RoundCap)
    #     pen.setStyle(QtCore.Qt.SolidLine)
    #     painter.setPen(pen)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = WindowGraphicsView()
    # sys.exit(app.exec_())
