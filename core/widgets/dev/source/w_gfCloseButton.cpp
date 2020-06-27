#include "headers/w_gfCloseButton.h"

#include "headers/moc_w_gfCloseButton.cpp"


/////////////////////////////////////////////////////////////////////
// Export Widget

GFCloseButton::GFCloseButton(QWidget *parent) : QPushButton(parent){
    setLineWidth(2);
    setPadding(8);
    setDormantColor(QColor(0, 0, 0));
    setHoverColor(QColor(255, 255, 255));
    setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    setAttribute(Qt::WA_Hover);
    kActiveColor = kDormantColor;
    kButtonArea = QRegion(0, 0, width(), height(), QRegion::Ellipse);
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
    painter.setBrush(QBrush(Qt::gray));
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
    kActiveColor = kHoverColor;
    update();
    emit mouseHoverEntered();
}


void GFCloseButton::hoverLeaveEvent(QHoverEvent *event){
    this->setCursor(QCursor(Qt::ArrowCursor));
    kActiveColor = kDormantColor;
    update();
    emit mouseHoverLeaved();
}


void GFCloseButton::clickEvent(QMouseEvent *event){
    if (kButtonArea.contains(event->pos())){
        if (event->button() == Qt::RightButton){
            kActiveColor = QColor(Qt::red);
            update();
            emit mouseRightClicked();
        }
        else if (event->button() == Qt::LeftButton){
            kActiveColor = QColor(Qt::green);
            update();
            emit mouseClicked();
        }
    }
}


void GFCloseButton::doubleClickEvent(QMouseEvent *event){
    if (kButtonArea.contains(event->pos())){
        if (event->button() == Qt::LeftButton){
            kActiveColor = QColor(Qt::blue);
            update();
            emit mouseDoubleClicked();
        }
    }
}


int GFCloseButton::lineWidth() const{
    return kLineWidth;
}


void GFCloseButton::setLineWidth(int width){
    if (width != kLineWidth){
        kLineWidth = width;
        update();
    }
}


int GFCloseButton::padding() const{
    return kPadding;
}


void GFCloseButton::setPadding(int padding){
    if (padding != kPadding){
        kPadding = padding;
        update();
    }
}


QColor GFCloseButton::dormantColor() const{
    return kDormantColor;
}


void GFCloseButton::setDormantColor(QColor color){
    if (color != kDormantColor){
        kDormantColor = color;
        update();
    }
}


QColor GFCloseButton::hoverColor() const{
    return kHoverColor;
}


void GFCloseButton::setHoverColor(QColor color){
    if (color != kHoverColor){
        kHoverColor = color;
        update();
    }
}


bool GFCloseButton::animated() const{
    return kAnimated;
}


void GFCloseButton::setAnimated(bool animated){
    if (animated != kAnimated){
        kAnimated = animated;
        update();
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