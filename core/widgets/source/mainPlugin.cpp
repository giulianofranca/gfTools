#include "headers/mainPlugin.h"
#include "headers/analogclockplugin.h"

#include "headers/moc_mainPlugin.cpp"


GFWidgets::GFWidgets(QObject *parent) : QObject(parent){
    widgets.append(new AnalogClockPlugin(this));
}

QList<QDesignerCustomWidgetInterface*> GFWidgets::customWidgets() const{
    return widgets;
}