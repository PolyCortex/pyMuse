#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <ctime>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:

    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void ButtonToggleFunction(QPushButton *button, bool checked, QString whitePicPath, QString blackPic);
    void p300Effect();
    void start();
    unsigned long elapsedTime();
    void randomArray();

private slots:

    void on_volume_toggled(bool checked);
    void on_channel_toggled(bool checked);
    void on_home_toggled(bool checked);
    void on_power_toggled(bool checked);
    void on_volume_clicked();
    void on_home_clicked();
    void on_channel_clicked();

    void on_minus_volume_toggled(bool checked);

    void on_mute_volume_toggled(bool checked);

    void on_plus_volume_toggled(bool checked);

    void on_favorite_channel_toggled(bool checked);

    void on_minus_channel_toggled(bool checked);

    void on_plus_channel_toggled(bool checked);

    void on_pushButton_pressed();

    void on_pushButton_2_pressed();

    void on_frequency_Bspin_valueChanged();

    void on_frequency_Aspin_valueChanged();


    void on_freemode_radioButton_clicked();

    void on_acquisition_radioButton_clicked();

    void on_p300remote_radioButton_clicked();

private:
    Ui::MainWindow *ui;  
};

#endif // MAINWINDOW_H
