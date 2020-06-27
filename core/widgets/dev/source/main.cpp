// https://doc.qt.io/qtcreator/adding-plugins.html
#include <QtWidgets\QApplication>

#include "headers\mainwindow.h"


int main(int argc, char* argv[]){
    QApplication app(argc, argv);
    MainWindow mainWindow;
    mainWindow.show();
    return app.exec();  // Nothing will run after app explicitly closes
}