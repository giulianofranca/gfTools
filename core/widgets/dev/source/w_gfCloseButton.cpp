#include "headers/w_gfCloseButton.h"

#include "headers/moc_w_gfCloseButton.cpp"


/////////////////////////////////////////////////////////////////////
// Export Widget

GFCloseButton::GFCloseButton(QWidget *parent) : QPushButton(parent){
    setLineWidth(2);
    setPadding(8);
    setBackgroundColor(QColor(100, 100, 100, 0));
    setDormantColor(QColor(103, 103, 103));
    setHoverColor(QColor(187, 187, 187));
    setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    setAttribute(Qt::WA_Hover);
    kButtonArea = QRegion(0, 0, width(), height(), QRegion::Ellipse);
    kActiveColor = kDormantColor;
    kAnimated = true;
    kAngle = 0;

    // Animation setup
    kActiveColorAnim = new QPropertyAnimation(this, "activeColor", this);
    kShapeAnim = new QPropertyAnimation(this, "angle", this);
    kActiveColorAnimCurve = QEasingCurve(QEasingCurve::OutQuart);
    kShapeAnimCurve = QEasingCurve(QEasingCurve::OutQuart);
    kActiveColorAnim->setEasingCurve(kActiveColorAnimCurve);
    kShapeAnim->setEasingCurve(kShapeAnimCurve);
    connect(kActiveColorAnim, SIGNAL(valueChanged(QVariant)), this, SLOT(animFrameChange(QVariant)));
    connect(kShapeAnim, SIGNAL(valueChanged(QVariant)), this, SLOT(animFrameChange(QVariant)));
}


void GFCloseButton::paintEvent(QPaintEvent *event){
    kButtonArea = QRegion(0, 0, width(), height(), QRegion::Ellipse);

    QPoint midPnt = QPoint(width() / 2, height() / 2);
    QSize length = QSize(width() - kPadding, height() - kPadding);
    QSize midLength = QSize(width() / 2, height() / 2);
    QSize ellipseLength = QSize((width() - kPadding) / 2, (height() - kPadding) / 2);

    QLine line1(-midLength.width(), -midLength.height(), 
                midLength.width(), midLength.height());
    QLine line2(-midLength.width(), midLength.height(), 
                midLength.width(), -midLength.height());

    QPainterPath path = QPainterPath(line1.p1());
    path.lineTo(line1.p2());
    path.moveTo(line2.p1());
    path.lineTo(line2.p2());

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, true);
    painter.save();

    // Draw Ellipse Background
    painter.setPen(Qt::NoPen);
    painter.setBrush(QBrush(kBackgroundColor));
    painter.drawEllipse(midPnt, midLength.width(), midLength.height());

    // Draw Close Shape
    painter.restore();
    painter.setClipRegion(QRegion(kPadding / 2, kPadding / 2,
                          length.width(), length.height(), 
                          QRegion::Ellipse));
    QPen pen(kActiveColor);
    pen.setWidth(kLineWidth);
    painter.setPen(pen);
    painter.translate(midPnt);
    painter.rotate(kAngle);
    painter.drawPath(path);
}


bool GFCloseButton::event(QEvent *event){
    switch (event->type())
    {
    case QEvent::HoverMove:
        hoverMoveEvent(static_cast<QHoverEvent*>(event));
        return true;
        break;

    case QEvent::HoverLeave:
        hoverLeaveEvent(static_cast<QHoverEvent*>(event));
        return true;
        break;

    case QEvent::MouseButtonPress:
        clickEvent(static_cast<QMouseEvent*>(event));
        return true;
        break;

    case QEvent::MouseButtonDblClick:
        doubleClickEvent(static_cast<QMouseEvent*>(event));
        return true;
        break;
    
    default:
        break;
    }
    return QWidget::event(event);
}


void GFCloseButton::hoverMoveEvent(QHoverEvent *event){
    if (kButtonArea.contains(event->pos()))
        hoverEnterEvent(event);
    else
        hoverLeaveEvent(event);
}


void GFCloseButton::hoverEnterEvent(QHoverEvent *event){
    this->setCursor(QCursor(Qt::PointingHandCursor));
    if (kAnimated){
        kActiveColorAnim->stop();
        kActiveColorAnim->setDuration(500);
        kActiveColorAnim->setEasingCurve(kActiveColorAnimCurve);
        kActiveColorAnim->setStartValue(kActiveColor);
        kActiveColorAnim->setEndValue(kHoverColor);
        kActiveColorAnim->start();
        kShapeAnim->stop();
        kShapeAnim->setDuration(500);
        kShapeAnim->setEasingCurve(kShapeAnimCurve);
        kShapeAnim->setStartValue(kAngle);
        kShapeAnim->setEndValue(180);
        kShapeAnim->start();
    }
    else{
        kActiveColor = kHoverColor;
        repaint(kButtonArea);
    }
    emit hoverEntered();
}


void GFCloseButton::hoverLeaveEvent(QHoverEvent *event){
    this->setCursor(QCursor(Qt::ArrowCursor));
    if (kAnimated){
        kActiveColorAnim->stop();
        kActiveColorAnim->setDuration(500);
        kActiveColorAnim->setEasingCurve(kActiveColorAnimCurve);
        kActiveColorAnim->setStartValue(kActiveColor);
        kActiveColorAnim->setEndValue(kDormantColor);
        kActiveColorAnim->start();
        kShapeAnim->stop();
        kShapeAnim->setDuration(500);
        kShapeAnim->setEasingCurve(kShapeAnimCurve);
        kShapeAnim->setStartValue(kAngle);
        kShapeAnim->setEndValue(0);
        kShapeAnim->start();
    }
    else{
        kActiveColor = kDormantColor;
        repaint(kButtonArea);
    }
    emit hoverLeaved();
}


void GFCloseButton::clickEvent(QMouseEvent *event){
    if (kButtonArea.contains(event->pos())){
        if (event->button() == Qt::RightButton){
            kActiveColor = QColor(Qt::red);
            repaint(kButtonArea);
            emit rightClicked();
        }
        else if (event->button() == Qt::LeftButton){
            kActiveColor = QColor(Qt::green);
            repaint(kButtonArea);
            emit clicked();
        }
    }
}


void GFCloseButton::doubleClickEvent(QMouseEvent *event){
    if (kButtonArea.contains(event->pos())){
        if (event->button() == Qt::LeftButton){
            kActiveColor = QColor(Qt::blue);
            repaint(kButtonArea);
            emit doubleClicked();
        }
    }
}


void GFCloseButton::animFrameChange(const QVariant &value){
    repaint(kButtonArea);
}


int GFCloseButton::lineWidth() const{
    return kLineWidth;
}


void GFCloseButton::setLineWidth(int width){
    if (width != kLineWidth){
        kLineWidth = width;
        repaint(kButtonArea);
    }
}


int GFCloseButton::padding() const{
    return kPadding;
}


void GFCloseButton::setPadding(int padding){
    if (padding != kPadding){
        kPadding = padding;
        repaint(kButtonArea);
    }
}


QColor GFCloseButton::backgroundColor() const{
    return kBackgroundColor;
}


void GFCloseButton::setBackgroundColor(QColor color){
    if (color != kBackgroundColor){
        kBackgroundColor = color;
        repaint(kButtonArea);
    }
}


QColor GFCloseButton::dormantColor() const{
    return kDormantColor;
}


void GFCloseButton::setDormantColor(QColor color){
    if (color != kDormantColor){
        kDormantColor = color;
        repaint(kButtonArea);
    }
}


QColor GFCloseButton::hoverColor() const{
    return kHoverColor;
}


void GFCloseButton::setHoverColor(QColor color){
    if (color != kHoverColor){
        kHoverColor = color;
        repaint(kButtonArea);
    }
}


bool GFCloseButton::animated() const{
    return kAnimated;
}


void GFCloseButton::setAnimated(bool animated){
    if (animated != kAnimated){
        kAnimated = animated;
        repaint(kButtonArea);
    }
}




/////////////////////////////////////////////////////////////////////
// Interfaces

GFCloseButtonInterface::GFCloseButtonInterface(QObject *parent) : QObject(parent){}


void GFCloseButtonInterface::initialize(QDesignerFormEditorInterface * /*core */){
    if (initialized)
        return;

    initialized = true;
}


bool GFCloseButtonInterface::isInitialized() const{
    return initialized;
}


QWidget *GFCloseButtonInterface::createWidget(QWidget *parent){
    return new GFCloseButton(parent);
}


QString GFCloseButtonInterface::name() const{
    return QStringLiteral("GFCloseButton");
}


QString GFCloseButtonInterface::group() const{
    return QStringLiteral("gfTools Widgets");
}


QIcon GFCloseButtonInterface::icon() const{
    return QIcon();
}


QString GFCloseButtonInterface::toolTip() const{
    return QString();
}


QString GFCloseButtonInterface::whatsThis() const{
    return QString();
}


bool GFCloseButtonInterface::isContainer() const{
    return false;
}


QString GFCloseButtonInterface::domXml() const{
    return "<ui language=\"c++\">\n"
           " <widget class=\"GFCloseButton\" name=\"gfCloseButton\">\n"
           "  <property name=\"geometry\">\n"
           "   <rect>\n"
           "    <x>0</x>\n"
           "    <y>0</y>\n"
           "    <width>16</width>\n"
           "    <height>16</height>\n"
           "   </rect>\n"
           "  </property>\n"
           " </widget>\n"
           "</ui>\n";
}


QString GFCloseButtonInterface::includeFile() const{
    return QStringLiteral("w_gfCloseButton.h");
}