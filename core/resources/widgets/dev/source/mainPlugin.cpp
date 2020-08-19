#include "headers/mainPlugin.h"
#include "headers/analogclockplugin.h"
#include "headers/w_gfToolTitleBar.h"
#include "headers/w_gfCloseButton.h"

#include "headers/moc_mainPlugin.cpp"


GFWidgets::GFWidgets(QObject *parent) : QObject(parent){
    widgets.append(new AnalogClockPlugin(this));
    widgets.append(new ToolTitleBarInterface(this));
    widgets.append(new GFCloseButtonInterface(this));
}

QList<QDesignerCustomWidgetInterface*> GFWidgets::customWidgets() const{
    return widgets;
}