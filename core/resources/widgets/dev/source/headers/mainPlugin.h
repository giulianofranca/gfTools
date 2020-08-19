#ifndef GFWIDGETS_H
#define GFWIDGETS_H

#include <QtCore/QtPlugin>
#include <QtUiPlugin/QDesignerCustomWidgetCollectionInterface>




class GFWidgets : public QObject, public QDesignerCustomWidgetCollectionInterface{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QDesignerCustomWidgetCollectionInterface")
    Q_INTERFACES(QDesignerCustomWidgetCollectionInterface)

public:
    GFWidgets(QObject *parent = nullptr);

    QList<QDesignerCustomWidgetInterface*> customWidgets() const override;

private:
    QList<QDesignerCustomWidgetInterface*> widgets;
};



#endif // GFWIDGETS_H