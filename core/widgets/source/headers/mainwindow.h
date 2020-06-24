#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <iostream>
#include <stdio.h>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QFileDialog>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void onOpenActionTriggered();

private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H
