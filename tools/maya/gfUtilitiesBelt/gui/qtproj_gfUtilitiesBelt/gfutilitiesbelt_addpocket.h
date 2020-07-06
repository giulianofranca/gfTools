#ifndef GFUTILITIESBELT_ADDPOCKET_H
#define GFUTILITIESBELT_ADDPOCKET_H

#include <QDialog>

namespace Ui {
class gfUtilitiesBelt_addPocket;
}

class gfUtilitiesBelt_addPocket : public QDialog
{
    Q_OBJECT

public:
    explicit gfUtilitiesBelt_addPocket(QWidget *parent = 0);
    ~gfUtilitiesBelt_addPocket();

private:
    Ui::gfUtilitiesBelt_addPocket *ui;
};

#endif // GFUTILITIESBELT_ADDPOCKET_H
