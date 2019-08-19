#include "gfutilitiesbelt_addpocket.h"
#include "ui_gfutilitiesbelt_addpocket.h"

gfUtilitiesBelt_addPocket::gfUtilitiesBelt_addPocket(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::gfUtilitiesBelt_addPocket)
{
    ui->setupUi(this);
}

gfUtilitiesBelt_addPocket::~gfUtilitiesBelt_addPocket()
{
    delete ui;
}
