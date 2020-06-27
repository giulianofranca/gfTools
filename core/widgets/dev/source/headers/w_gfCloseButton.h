#ifndef GFCLOSEBUTTON_H
#define GFCLOSEBUTTON_H

#include <QtCore/QtGlobal>
#include <QtCore/QPoint>
#include <QtCore/QEvent>
#include <QtGui/QHoverEvent>
#include <QtGui/QMouseEvent>
#include <QtGui/QPainter>

#include <QtWidgets/QPushButton>
#include <QtCore/QtPlugin>
#include <QtUiPlugin/QDesignerExportWidget>
#include <QtUiPlugin/QDesignerCustomWidgetInterface>

//TODO: Implement hoverMove event. If the move pos is in button area emit hoverEntered.


/////////////////////////////////////////////////////////////////////
// Export Widget

class QDESIGNER_WIDGET_EXPORT GFCloseButton : public QPushButton{
    Q_OBJECT
    Q_PROPERTY(int lineWidth READ lineWidth WRITE setLineWidth)
    Q_PROPERTY(int padding READ padding WRITE setPadding)
    Q_PROPERTY(QColor dormantColor READ dormantColor WRITE setDormantColor)
    Q_PROPERTY(QColor hoverColor READ hoverColor WRITE setHoverColor)
    Q_PROPERTY(bool animated READ animated WRITE setAnimated)

public:
    explicit GFCloseButton(QWidget *parent=nullptr);

    int                                 lineWidth() const;
    void                                setLineWidth(int width);
    int                                 padding() const;
    void                                setPadding(int padding);
    QColor                              dormantColor() const;
    void                                setDormantColor(QColor color);
    QColor                              hoverColor() const;
    void                                setHoverColor(QColor color);
    bool                                animated() const;
    void                                setAnimated(bool animated);

protected:
    void                                paintEvent(QPaintEvent *event) override;
    bool                                event(QEvent *event) override;
    void                                hoverMoveEvent(QHoverEvent *event);
    void                                hoverEnterEvent(QHoverEvent *event);
    void                                hoverLeaveEvent(QHoverEvent *event);
    void                                clickEvent(QMouseEvent *event);
    void                                doubleClickEvent(QMouseEvent *event);

signals:
    // Use signals beginning with mouse. (e.g. mouseClicked() instead of clicked())
    void                                mouseHoverEntered();
    void                                mouseHoverLeaved();
    void                                mouseClicked();
    void                                mouseRightClicked();
    void                                mouseDoubleClicked();

private:
    int                                 kLineWidth;
    int                                 kPadding;
    QColor                              kDormantColor;
    QColor                              kHoverColor;
    QColor                              kActiveColor;
    bool                                kAnimated;
    QRegion                             kButtonArea;
};




/////////////////////////////////////////////////////////////////////
// Interfaces

class GFCloseButtonInterface : public QObject, public QDesignerCustomWidgetInterface{
    Q_OBJECT
    Q_INTERFACES(QDesignerCustomWidgetInterface)

public:
    GFCloseButtonInterface(QObject *parent=nullptr);

    bool                                isContainer() const override;
    bool                                isInitialized() const override;
    QIcon                               icon() const override;
    QString                             domXml() const override;
    QString                             group() const override;
    QString                             includeFile() const override;
    QString                             name() const override;
    QString                             toolTip() const override;
    QString                             whatsThis() const override;
    QWidget                             *createWidget(QWidget *parent) override;
    void                                initialize(QDesignerFormEditorInterface *core) override;

private:
    bool                                initialized = false;
};




#endif // GFCLOSEBUTTON_H