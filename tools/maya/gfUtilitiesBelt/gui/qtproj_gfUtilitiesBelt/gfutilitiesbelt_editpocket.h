#ifndef GFUTILITIESBELT_EDITPOCKET_H
#define GFUTILITIESBELT_EDITPOCKET_H

#include <QDialog>

namespace Ui {
class gfUtilitiesBelt_editPocket;
}

class gfUtilitiesBelt_editPocket : public QDialog
{
    Q_OBJECT

public:
    explicit gfUtilitiesBelt_editPocket(QWidget *parent = 0);
    ~gfUtilitiesBelt_editPocket();

private:
    Ui::gfUtilitiesBelt_editPocket *ui;
};

#endif // GFUTILITIESBELT_EDITPOCKET_H
