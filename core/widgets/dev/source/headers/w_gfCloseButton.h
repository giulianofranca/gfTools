#ifndef GFCLOSEBUTTON_H
#define GFCLOSEBUTTON_H

#include <QtCore/QtGlobal>
#include <QtCore/QPoint>
#include <QtCore/QEvent>
#include <QtCore/QPropertyAnimation>
#include <QtCore/QVariantAnimation>
#include <QtCore/QEasingCurve>
#include <QtGui/QHoverEvent>
#include <QtGui/QMouseEvent>
#include <QtGui/QPainter>

#include <QtWidgets/QPushButton>
#include <QtCore/QtPlugin>
#include <QtUiPlugin/QDesignerExportWidget>
#include <QtUiPlugin/QDesignerCustomWidgetInterface>


/////////////////////////////////////////////////////////////////////
// Export Widget

class QDESIGNER_WIDGET_EXPORT GFCloseButton : public QPushButton{
    Q_OBJECT
    Q_PROPERTY(int lineWidth READ lineWidth WRITE setLineWidth)
    Q_PROPERTY(int padding READ padding WRITE setPadding)
    Q_PROPERTY(QColor backgroundColor READ backgroundColor WRITE setBackgroundColor)
    Q_PROPERTY(QColor dormantColor READ dormantColor WRITE setDormantColor)
    Q_PROPERTY(QColor hoverColor READ hoverColor WRITE setHoverColor)
    Q_PROPERTY(bool animated READ animated WRITE setAnimated)
    Q_PROPERTY(QColor activeColor MEMBER kActiveColor DESIGNABLE false)
    Q_PROPERTY(qreal angle MEMBER kAngle DESIGNABLE false)

public:
    explicit GFCloseButton(QWidget *parent=nullptr);

    // PROPERTY METHODS
    int                                 lineWidth() const;
    void                                setLineWidth(int width);
    int                                 padding() const;
    void                                setPadding(int padding);
    QColor                              backgroundColor() const;
    void                                setBackgroundColor(QColor color);
    QColor                              dormantColor() const;
    void                                setDormantColor(QColor color);
    QColor                              hoverColor() const;
    void                                setHoverColor(QColor color);
    bool                                animated() const;
    void                                setAnimated(bool animated);

protected:
    // EVENTS
    void                                paintEvent(QPaintEvent *event) override;
    bool                                event(QEvent *event) override;
    void                                hoverMoveEvent(QHoverEvent *event);
    void                                hoverEnterEvent(QHoverEvent *event);
    void                                hoverLeaveEvent(QHoverEvent *event);
    void                                clickEvent(QMouseEvent *event);
    void                                doubleClickEvent(QMouseEvent *event);

signals:
    // SIGNALS
    void                                hoverEntered();
    void                                hoverLeaved();
    void                                clicked();
    void                                rightClicked();
    void                                doubleClicked();

private slots:
    // PRIVATE SLOTS
    void                                animFrameChange(const QVariant &value);

private:
    // PROPERTIES
    int                                 kLineWidth;
    int                                 kPadding;
    QColor                              kBackgroundColor;
    QColor                              kDormantColor;
    QColor                              kHoverColor;
    bool                                kAnimated;
    QColor                              kActiveColor;
    qreal                               kAngle;

    // PRIVATE DATA
    QRegion                             kButtonArea;
    QPropertyAnimation                  *kActiveColorAnim;
    QPropertyAnimation                  *kShapeAnim;
    QEasingCurve                        kActiveColorAnimCurve;
    QEasingCurve                        kShapeAnimCurve;
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