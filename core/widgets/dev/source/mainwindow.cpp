// _MSC_VER
// #ifdef _WIN32
//     #ifdef _DEBUG
//         // Debug
//         #pragma include_alias("ui/ui_mainwindow.h", "../build/source/helloSignalSlots_autogen/include_Debug/ui/ui_mainwindow.h")
//         #pragma include_alias("headers/moc_mainwindow.cpp", "../build/source/helloSignalSlots_autogen/include_Debug/headers/moc_mainwindow.cpp")
//     #else
//         // Release
//         #pragma include_alias("ui/ui_mainwindow.h", "../build/source/helloSignalSlots_autogen/include_Release/ui/ui_mainwindow.h")
//         #pragma include_alias("headers/moc_mainwindow.cpp", "../build/source/helloSignalSlots_autogen/include_Release/headers/moc_mainwindow.cpp")
//     #endif
// #else
//     #pragma include_alias("ui/ui_mainwindow.h", "../build/source/helloSignalSlots_autogen/include/ui/ui_mainwindow.h")
//     #pragma include_alias("headers/moc_mainwindow.cpp", "../build/source/helloSignalSlots_autogen/include/headers/moc_mainwindow.cpp")
// #endif
// Build generated Qt Files
#include "ui/ui_mainwindow.h"
#include "headers/moc_mainwindow.cpp"
/////////////////////////////////////////////////////////////

#include "headers/mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    QObject::connect(ui->actionOpen, SIGNAL(triggered()), this, SLOT(onOpenActionTriggered()));
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::onOpenActionTriggered(){
    std::cout << "Button Triggered" << std::endl;
    // Use QStandardPaths to a QFileDialog
    auto selectedFile = QFileDialog::getOpenFileName(this, tr("Open a file"), QApplication::applicationDirPath());
    int Test = 0;
    if(!selectedFile.isNull())
        std::cout << selectedFile.toStdString() << std::endl;
}