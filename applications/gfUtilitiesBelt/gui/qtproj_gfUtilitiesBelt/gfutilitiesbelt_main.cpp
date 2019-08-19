#include "gfutilitiesbelt_main.h"
#include "ui_gfutilitiesbelt_main.h"

gfutilitiesbelt_main::gfutilitiesbelt_main(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::gfutilitiesbelt_main)
{
    ui->setupUi(this);
}

gfutilitiesbelt_main::~gfutilitiesbelt_main()
{
    delete ui;
}
