/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.7.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QRadioButton>
#include <QtWidgets/QSpinBox>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QWidget *home_widget;
    QPushButton *volume;
    QPushButton *channel;
    QPushButton *power;
    QWidget *volume_widget;
    QPushButton *plus_volume;
    QPushButton *minus_volume;
    QPushButton *mute_volume;
    QPushButton *home;
    QWidget *channel_widget;
    QPushButton *minus_channel;
    QPushButton *plus_channel;
    QPushButton *favorite_channel;
    QFrame *line;
    QGroupBox *groupBox;
    QPushButton *pushButton;
    QPushButton *pushButton_2;
    QRadioButton *freemode_radioButton;
    QRadioButton *acquisition_radioButton;
    QRadioButton *p300remote_radioButton;
    QSpinBox *frequency_Bspin;
    QSpinBox *frequency_Aspin;
    QLabel *label;
    QLabel *frequency_label;
    QLabel *frequency_Blabel;
    QLabel *frequency_Alabel;
    QButtonGroup *buttonGroup;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(927, 581);
        MainWindow->setStyleSheet(QLatin1String("QSpinBox { border: 3px inset grey; } \n"
"QSpinBox::up-button { subcontrol-position: left; width: 32px; height: 35px;}\n"
"QSpinBox::down-button { subcontrol-position: right; width: 30px; height: 35px;}"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        centralWidget->setStyleSheet(QStringLiteral("background-color: rgb(197, 197, 197);"));
        home_widget = new QWidget(centralWidget);
        home_widget->setObjectName(QStringLiteral("home_widget"));
        home_widget->setGeometry(QRect(0, 0, 581, 571));
        volume = new QPushButton(home_widget);
        volume->setObjectName(QStringLiteral("volume"));
        volume->setGeometry(QRect(20, 10, 267, 267));
        volume->setStyleSheet(QLatin1String("#volume {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/VolumeButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#volume:pressed\n"
"{\n"
"border-image: url(:/Buttons/VolumeButtonWhite.png);\n"
"}"));
        channel = new QPushButton(home_widget);
        channel->setObjectName(QStringLiteral("channel"));
        channel->setGeometry(QRect(20, 290, 267, 267));
        channel->setStyleSheet(QLatin1String("#channel {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/ChannelButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#channel:pressed\n"
"{\n"
"border-image: url(:/Buttons/ChannelButtonWhite.png);\n"
"}"));
        power = new QPushButton(home_widget);
        power->setObjectName(QStringLiteral("power"));
        power->setGeometry(QRect(300, 10, 267, 267));
        power->setStyleSheet(QLatin1String("#power {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/PowerButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#power:pressed\n"
"{\n"
"border-image: url(:/Buttons/PowerButtonWhite.png);\n"
"}"));
        volume_widget = new QWidget(centralWidget);
        volume_widget->setObjectName(QStringLiteral("volume_widget"));
        volume_widget->setGeometry(QRect(0, 0, 581, 571));
        plus_volume = new QPushButton(volume_widget);
        plus_volume->setObjectName(QStringLiteral("plus_volume"));
        plus_volume->setGeometry(QRect(20, 10, 267, 267));
        plus_volume->setStyleSheet(QLatin1String("#plus_volume {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/PlusButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#plus_volume:pressed\n"
"{\n"
"border-image: url(:/Buttons/PlusButtonWhite.png);\n"
"}"));
        minus_volume = new QPushButton(volume_widget);
        minus_volume->setObjectName(QStringLiteral("minus_volume"));
        minus_volume->setGeometry(QRect(20, 290, 267, 267));
        minus_volume->setStyleSheet(QLatin1String("#minus_volume {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/MinusButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#minus_volume:pressed\n"
"{\n"
"border-image: url(:/Buttons/MinusButtonWhite.png);\n"
"}"));
        mute_volume = new QPushButton(volume_widget);
        mute_volume->setObjectName(QStringLiteral("mute_volume"));
        mute_volume->setGeometry(QRect(300, 10, 267, 267));
        mute_volume->setStyleSheet(QLatin1String("#mute_volume {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/MuteButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#mute_volume:pressed\n"
"{\n"
"border-image: url(:/Buttons/MuteButtonWhite.png);\n"
"}"));
        home = new QPushButton(centralWidget);
        home->setObjectName(QStringLiteral("home"));
        home->setGeometry(QRect(300, 290, 267, 267));
        home->setStyleSheet(QLatin1String("#home {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/HomeButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#home:pressed\n"
"{\n"
"border-image: url(:/Buttons/HomeButtonWhite.png);\n"
"}"));
        channel_widget = new QWidget(centralWidget);
        channel_widget->setObjectName(QStringLiteral("channel_widget"));
        channel_widget->setGeometry(QRect(0, 0, 580, 571));
        minus_channel = new QPushButton(channel_widget);
        minus_channel->setObjectName(QStringLiteral("minus_channel"));
        minus_channel->setGeometry(QRect(20, 290, 267, 267));
        minus_channel->setStyleSheet(QLatin1String("#minus_channel {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/MinusButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#minus_channel:pressed\n"
"{\n"
"border-image: url(:/Buttons/MinusButtonWhite.png);\n"
"}"));
        plus_channel = new QPushButton(channel_widget);
        plus_channel->setObjectName(QStringLiteral("plus_channel"));
        plus_channel->setGeometry(QRect(20, 10, 267, 267));
        plus_channel->setStyleSheet(QLatin1String("#plus_channel {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/PlusButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#plus_channel:pressed\n"
"{\n"
"border-image: url(:/Buttons/PlusButtonWhite.png);\n"
"}"));
        favorite_channel = new QPushButton(channel_widget);
        favorite_channel->setObjectName(QStringLiteral("favorite_channel"));
        favorite_channel->setGeometry(QRect(300, 10, 267, 267));
        favorite_channel->setStyleSheet(QLatin1String("#favorite_channel {\n"
"background-color: transparent;\n"
"border-image: url(:/Buttons/FavoriteButtonBlack.png);\n"
"background: none;\n"
"border: none;\n"
"background-repeat: none;\n"
"}\n"
"#favorite_channel:pressed\n"
"{\n"
"border-image: url(:/Buttons/FavoriteButtonWhite.png);\n"
"}"));
        line = new QFrame(centralWidget);
        line->setObjectName(QStringLiteral("line"));
        line->setGeometry(QRect(580, 10, 16, 551));
        line->setFrameShape(QFrame::VLine);
        line->setFrameShadow(QFrame::Sunken);
        groupBox = new QGroupBox(centralWidget);
        groupBox->setObjectName(QStringLiteral("groupBox"));
        groupBox->setGeometry(QRect(610, 30, 291, 521));
        QFont font;
        font.setPointSize(15);
        font.setBold(true);
        font.setWeight(75);
        groupBox->setFont(font);
        groupBox->setStyleSheet(QStringLiteral("background-color: rgb(148, 148, 148);"));
        pushButton = new QPushButton(groupBox);
        pushButton->setObjectName(QStringLiteral("pushButton"));
        pushButton->setGeometry(QRect(20, 360, 131, 31));
        pushButton_2 = new QPushButton(groupBox);
        pushButton_2->setObjectName(QStringLiteral("pushButton_2"));
        pushButton_2->setGeometry(QRect(160, 360, 121, 31));
        freemode_radioButton = new QRadioButton(groupBox);
        buttonGroup = new QButtonGroup(MainWindow);
        buttonGroup->setObjectName(QStringLiteral("buttonGroup"));
        buttonGroup->addButton(freemode_radioButton);
        freemode_radioButton->setObjectName(QStringLiteral("freemode_radioButton"));
        freemode_radioButton->setGeometry(QRect(30, 80, 171, 31));
        acquisition_radioButton = new QRadioButton(groupBox);
        buttonGroup->addButton(acquisition_radioButton);
        acquisition_radioButton->setObjectName(QStringLiteral("acquisition_radioButton"));
        acquisition_radioButton->setGeometry(QRect(30, 120, 181, 31));
        p300remote_radioButton = new QRadioButton(groupBox);
        buttonGroup->addButton(p300remote_radioButton);
        p300remote_radioButton->setObjectName(QStringLiteral("p300remote_radioButton"));
        p300remote_radioButton->setGeometry(QRect(30, 160, 191, 21));
        frequency_Bspin = new QSpinBox(groupBox);
        frequency_Bspin->setObjectName(QStringLiteral("frequency_Bspin"));
        frequency_Bspin->setGeometry(QRect(150, 270, 131, 22));
        frequency_Bspin->setLayoutDirection(Qt::RightToLeft);
        frequency_Bspin->setStyleSheet(QStringLiteral("background-color: rgb(148, 148, 148);"));
        frequency_Bspin->setWrapping(false);
        frequency_Bspin->setButtonSymbols(QAbstractSpinBox::PlusMinus);
        frequency_Bspin->setProperty("showGroupSeparator", QVariant(false));
        frequency_Bspin->setMaximum(1000);
        frequency_Bspin->setSingleStep(5);
        frequency_Aspin = new QSpinBox(groupBox);
        frequency_Aspin->setObjectName(QStringLiteral("frequency_Aspin"));
        frequency_Aspin->setGeometry(QRect(150, 320, 131, 21));
        frequency_Aspin->setLayoutDirection(Qt::RightToLeft);
        frequency_Aspin->setButtonSymbols(QAbstractSpinBox::PlusMinus);
        frequency_Aspin->setMaximum(1000);
        frequency_Aspin->setSingleStep(5);
        label = new QLabel(groupBox);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(24, 30, 181, 41));
        QFont font1;
        font1.setPointSize(16);
        font1.setBold(true);
        font1.setUnderline(true);
        font1.setWeight(75);
        label->setFont(font1);
        frequency_label = new QLabel(groupBox);
        frequency_label->setObjectName(QStringLiteral("frequency_label"));
        frequency_label->setGeometry(QRect(30, 200, 251, 51));
        frequency_label->setFont(font1);
        frequency_Blabel = new QLabel(groupBox);
        frequency_Blabel->setObjectName(QStringLiteral("frequency_Blabel"));
        frequency_Blabel->setGeometry(QRect(30, 260, 111, 31));
        frequency_Alabel = new QLabel(groupBox);
        frequency_Alabel->setObjectName(QStringLiteral("frequency_Alabel"));
        frequency_Alabel->setGeometry(QRect(30, 309, 111, 31));
        pushButton->raise();
        pushButton_2->raise();
        freemode_radioButton->raise();
        acquisition_radioButton->raise();
        p300remote_radioButton->raise();
        label->raise();
        frequency_label->raise();
        frequency_Blabel->raise();
        frequency_Alabel->raise();
        frequency_Bspin->raise();
        frequency_Aspin->raise();
        MainWindow->setCentralWidget(centralWidget);
        channel_widget->raise();
        home_widget->raise();
        volume_widget->raise();
        home->raise();
        line->raise();
        groupBox->raise();

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0));
        volume->setText(QString());
        channel->setText(QString());
        power->setText(QString());
        plus_volume->setText(QString());
        minus_volume->setText(QString());
        mute_volume->setText(QString());
        home->setText(QString());
        minus_channel->setText(QString());
        plus_channel->setText(QString());
        favorite_channel->setText(QString());
        groupBox->setTitle(QApplication::translate("MainWindow", "Control", 0));
        pushButton->setText(QApplication::translate("MainWindow", "start", 0));
        pushButton_2->setText(QApplication::translate("MainWindow", "stop", 0));
        freemode_radioButton->setText(QApplication::translate("MainWindow", "Free", 0));
        acquisition_radioButton->setText(QApplication::translate("MainWindow", "Acquisition", 0));
        p300remote_radioButton->setText(QApplication::translate("MainWindow", "P300 Remote", 0));
        label->setText(QApplication::translate("MainWindow", "Mode :", 0));
        frequency_label->setText(QApplication::translate("MainWindow", "Frequency :", 0));
        frequency_Blabel->setText(QApplication::translate("MainWindow", "Before Time :", 0));
        frequency_Alabel->setText(QApplication::translate("MainWindow", "After Time :", 0));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
