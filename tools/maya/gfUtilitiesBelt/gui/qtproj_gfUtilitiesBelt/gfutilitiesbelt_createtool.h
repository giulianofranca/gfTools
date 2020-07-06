#ifndef GFUTILITIESBELT_CREATETOOL_H
#define GFUTILITIESBELT_CREATETOOL_H

#include <QDialog>

namespace Ui {
class gfUtilitiesBelt_createTool;
}

class gfUtilitiesBelt_createTool : public QDialog
{
    Q_OBJECT

public:
    explicit gfUtilitiesBelt_createTool(QWidget *parent = 0);
    ~gfUtilitiesBelt_createTool();

private:
    Ui::gfUtilitiesBelt_createTool *ui;
};

#endif // GFUTILITIESBELT_CREATETOOL_H
