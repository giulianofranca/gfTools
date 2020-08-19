#include "headers/w_gfToolTitleBar.h"

#include "headers/moc_w_gfToolTitleBar.cpp"


/////////////////////////////////////////////////////////////////////
// Additional intern widgets

// ToolButton::ToolButton(QWidget *parent) : QPushButton(parent){
//     // Constructor
//     setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
// }

ToolButton::ToolButton(const QString &text, QWidget *parent) : 
    QPushButton(parent){
    // Constructor
    setSizePolicy(QSizePolicy::Fixed, QSizePolicy::Fixed);
    setText(text);
}


QSize ToolButton::minimumSizeHint() const{
    QSize size;
    ToolTitleBar *parent = qobject_cast<ToolTitleBar *>(this->parent());
    if (parent){
        int top, bottom;
        
        parent->getTitleMargins(nullptr, &top, nullptr, &bottom);
        int length = parent->height() - (top + bottom);
        size = QSize(length, length);
    }
    else
        size = QSize(5, 5);
    return size;
}


QSize ToolButton::sizeHint() const{
    return minimumSizeHint();
}




/////////////////////////////////////////////////////////////////////
// Export Widget

ToolTitleBar::ToolTitleBar(QWidget *parent) : QWidget(parent){
    // Constructor
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Fixed);
    setLayoutDirection(Qt::LeftToRight);

    createTitleLayout();
    createSpacer();
    addCloseButton();
}


QSize ToolTitleBar::minimumSizeHint() const{
    return QSize(200, 24);
}


QSize ToolTitleBar::sizeHint() const{
    return minimumSizeHint();
}


void ToolTitleBar::setTitleMargins(int left, int top, int right, int bottom){
    titleLayout->setContentsMargins(left, top, right, bottom);
}


void ToolTitleBar::getTitleMargins(int *left, int *top, int *right, int *bottom){
    titleLayout->getContentsMargins(left, top, right, bottom);
}


void ToolTitleBar::setTitleSpacing(int space){
    titleLayout->setSpacing(space);
}


int ToolTitleBar::getTitleSpacing() const{
    return titleLayout->spacing();
}


void ToolTitleBar::createTitleLayout(){
    titleLayout = new QHBoxLayout(this);
    titleLayout->setContentsMargins(8, 4, 8, 4);
    titleLayout->setSpacing(8);
    setLayout(titleLayout);
}


void ToolTitleBar::createSpacer(){
    QMargins titleMargins = titleLayout->contentsMargins();
    int width = this->width() * 0.15;
    int height = this->height() - (titleMargins.top() + titleMargins.bottom());
    spacer = new QSpacerItem(width, height, QSizePolicy::Expanding, QSizePolicy::Minimum);
    titleLayout->insertSpacerItem(0, spacer);
}


void ToolTitleBar::addCloseButton(){
    closeButton = new ToolButton("X", this);
    titleLayout->insertWidget(1, closeButton);
}




/////////////////////////////////////////////////////////////////////
// Interfaces

ToolTitleBarInterface::ToolTitleBarInterface(QObject *parent) : QObject(parent){}

void ToolTitleBarInterface::initialize(QDesignerFormEditorInterface * /*core */){
    if (initialized)
        return;

    initialized = true;
}


bool ToolTitleBarInterface::isInitialized() const{
    return initialized;
}


QWidget *ToolTitleBarInterface::createWidget(QWidget *parent){
    return new ToolTitleBar(parent);
}


QString ToolTitleBarInterface::name() const{
    return QStringLiteral("gfToolTitleBar");
}


QString ToolTitleBarInterface::group() const{
    return QStringLiteral("gfTools Widgets");
}


QIcon ToolTitleBarInterface::icon() const{
    return QIcon();
}


QString ToolTitleBarInterface::toolTip() const{
    return QString();
}


QString ToolTitleBarInterface::whatsThis() const{
    return QString();
}


bool ToolTitleBarInterface::isContainer() const{
    return false;
}


QString ToolTitleBarInterface::domXml() const{
    return "<ui language=\"c++\">\n"
           " <widget class=\"ToolTitleBar\" name=\"gfToolTitleBar\">\n"
           "  <property name=\"geometry\">\n"
           "   <rect>\n"
           "    <x>0</x>\n"
           "    <y>0</y>\n"
           "    <width>200</width>\n"
           "    <height>24</height>\n"
           "   </rect>\n"
           "  </property>\n"
           " </widget>\n"
           "</ui>\n";
}


QString ToolTitleBarInterface::includeFile() const{
    return QStringLiteral("w_gfToolTitleBar.h");
}