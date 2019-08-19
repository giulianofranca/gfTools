#ifndef GFUTILITIESBELT_MAIN_H
#define GFUTILITIESBELT_MAIN_H

#include <QMainWindow>

namespace Ui {
class gfutilitiesbelt_main;
}

class gfutilitiesbelt_main : public QMainWindow
{
    Q_OBJECT

public:
    explicit gfutilitiesbelt_main(QWidget *parent = 0);
    ~gfutilitiesbelt_main();

private:
    Ui::gfutilitiesbelt_main *ui;
};

#endif // GFUTILITIESBELT_MAIN_H
