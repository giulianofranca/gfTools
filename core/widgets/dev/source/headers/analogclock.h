#ifndef ANALOGCLOCK_H
#define ANALOGCLOCK_H

#include <QtGui/QMouseEvent>
#include <QtGui/QPainter>
#include <QtCore/QTime>
#include <QtCore/QTimer>
#include <QtCore/QtGlobal>

#include <QtWidgets/QWidget>
#include <QtUiPlugin/QDesignerExportWidget>


class QDESIGNER_WIDGET_EXPORT AnalogClock : public QWidget{
    Q_OBJECT

public:
    explicit AnalogClock(QWidget *parent=nullptr);

protected:
    void paintEvent(QPaintEvent *event) override;
};



#endif // ANALOGCLOCK_H