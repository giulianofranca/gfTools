#ifndef GFTOOLTITLEBAR_H
#define GFTOOLTITLEBAR_H

#include <QtCore/QtPlugin>
#include <QtUiPlugin/QDesignerExportWidget>
#include <QtUiPlugin/QDesignerCustomWidgetInterface>

#include <QtWidgets/QWidget>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QSpacerItem>
#include <QtWidgets/QPushButton>


/////////////////////////////////////////////////////////////////////
// Additional intern widgets

class ToolButton : public QPushButton{
public:
    // ToolButton(const QIcon &icon, QWidget *parent=nullptr);
    explicit ToolButton(const QString &text, QWidget *parent=nullptr);

    QSize minimumSizeHint() const override;
    QSize sizeHint() const override;

// protected:
//     void paintEvent(QPaintEvent *event) override;
};




// class TitleButton : public QPushButton{
// public:
//     TitleButton(const QString &text, QWidget *parent=nullptr);
//     TitleButton(const QIcon &icon, QWidget *parent=nullptr);
//     TitleButton(const QString &text, const QIcon &icon, QWidget *parent=nullptr);

// protected:
//     void paintEvent(QPaintEvent *event) override;
// };




// class TitleArea : public QWidget{
// public:
//     TitleArea(QWidget *root=nullptr, QWidget *parent=nullptr);
// };




/////////////////////////////////////////////////////////////////////
// Export Widget

class QDESIGNER_WIDGET_EXPORT ToolTitleBar : public QWidget{
    Q_OBJECT

public:
    explicit ToolTitleBar(QWidget *parent=nullptr);

    QSize                               minimumSizeHint() const override;
    QSize                               sizeHint() const override;

    // Custom methods
    // void                             addTitleButton(QWidget *button);
    void                                setTitleMargins(int left, int top, int right, int bottom);
    void                                getTitleMargins(int *left=nullptr, int *top=nullptr, 
                                                        int *right=nullptr, int *bottom=nullptr);
    void                                setTitleSpacing(int space);
    int                                 getTitleSpacing() const;
    // void                             setRootWidget(QWidget *root);


protected:
    // void                             paintEvent(QPaintEvent *event) override;

    void                                createTitleLayout();
    void                                createSpacer();
    void                                addCloseButton();

private:
    // QWidget                          *root;
    ToolButton                          *closeButton;
    // ToolButton                       *minimizeButton;
    // ToolButton                       *maximizeButton;
    QHBoxLayout                         *titleLayout;
    QSpacerItem                         *spacer;
};




/////////////////////////////////////////////////////////////////////
// Interfaces

class ToolTitleBarInterface : public QObject, public QDesignerCustomWidgetInterface{
    Q_OBJECT
    Q_INTERFACES(QDesignerCustomWidgetInterface)

public:
    ToolTitleBarInterface(QObject *parent=nullptr);

    bool isContainer() const override;
    bool isInitialized() const override;
    QIcon icon() const override;
    QString domXml() const override;
    QString group() const override;
    QString includeFile() const override;
    QString name() const override;
    QString toolTip() const override;
    QString whatsThis() const override;
    QWidget *createWidget(QWidget *parent) override;
    void initialize(QDesignerFormEditorInterface *core) override;

private:
    bool initialized = false;
};



#endif // GFTOOLTITLEBAR_H