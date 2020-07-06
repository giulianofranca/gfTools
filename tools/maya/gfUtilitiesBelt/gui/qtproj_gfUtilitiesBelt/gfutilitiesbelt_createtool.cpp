#include "gfutilitiesbelt_createtool.h"
#include "ui_gfutilitiesbelt_createtool.h"

gfUtilitiesBelt_createTool::gfUtilitiesBelt_createTool(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::gfUtilitiesBelt_createTool)
{
    ui->setupUi(this);
}

gfUtilitiesBelt_createTool::~gfUtilitiesBelt_createTool()
{
    delete ui;
}
