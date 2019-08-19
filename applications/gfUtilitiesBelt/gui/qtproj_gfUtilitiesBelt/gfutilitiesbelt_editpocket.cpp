#include "gfutilitiesbelt_editpocket.h"
#include "ui_gfutilitiesbelt_editpocket.h"

gfUtilitiesBelt_editPocket::gfUtilitiesBelt_editPocket(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::gfUtilitiesBelt_editPocket)
{
    ui->setupUi(this);
}

gfUtilitiesBelt_editPocket::~gfUtilitiesBelt_editPocket()
{
    delete ui;
}
