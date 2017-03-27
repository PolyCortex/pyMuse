#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "timer.h"
#include <QToolButton>
#include <chrono>
#include <thread>
#include <algorithm>
#include <iostream>
#include <QApplication>

#include <winsock2.h>
#include <stdlib.h>
#include <stdio.h>
#include <string>

#pragma comment(lib, "ws2_32.lib")
#pragma comment (lib, "Mswsock.lib")
#pragma comment (lib, "AdvApi32.lib")

#define SERVER "127.0.0.1" //ip adress of udp server
#define PORT 8888
#define BUFLEN 65507
struct sockaddr_in server, si_other;
SOCKET s;
int slen;
char buf[BUFLEN];
WSADATA wsa;

#define TestSize 1000
bool stop = false;
unsigned long startTime = 0;
std::pair<QPushButton*,QPushButton*> p300Array[TestSize];
int arr[TestSize];
std::string udpArr[TestSize];
bool arrcomplet = false;
int BSLEEPTIME = 80;
int ASLEEPTIME = 100;
std::string mode;


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowTitle("Remote Home");
    this->setMinimumSize(927, 581);
    this->setMaximumSize(927, 581);

    ui->pushButton_2->setEnabled(false);
    ui->volume_widget->hide();
    ui->channel_widget->hide();

    ui->frequency_Bspin->setValue(BSLEEPTIME);
    ui->frequency_Aspin->setValue(ASLEEPTIME);
    ui->freemode_radioButton->setChecked(true);
    mode = "F";


    slen = sizeof(si_other);

    if (WSAStartup(MAKEWORD(2,2), &wsa) != 0)
    {
        printf("Failed. Error Code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }

    if ( (s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == SOCKET_ERROR)
    {
        printf("socket clien failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }

    memset((char *) &si_other, 0, sizeof(si_other));
    si_other.sin_family = AF_INET;
    si_other.sin_port = htons(PORT);
    si_other.sin_addr.S_un.S_addr = inet_addr(SERVER);
}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::randomArray()
{
    if (!arrcomplet)
    {
        srand((unsigned)time(NULL));

        for (int i = 0; i < TestSize; i++)
        {
            arr[i] = 1 + rand() % 4;
            if (arr[i] == 1)
                udpArr[i] = "L1";
            else if (arr[i] == 2)
                udpArr[i] = "L2";
            else if (arr[i] == 3)
                udpArr[i] = "C1";
            else if (arr[i] == 4)
                udpArr[i] = "C2";
        }

        arrcomplet = true;
    }
    if (!(ui->home_widget->isHidden()))
        for (int j = 0; j < TestSize - 1;j++)
        {
            if (arr[j] == 1)
                p300Array[j] = std::make_pair(ui->volume,ui->power);
            else if (arr[j] == 2)
                p300Array[j] = std::make_pair(ui->channel,ui->home);
            else if (arr[j] == 3)
                p300Array[j] = std::make_pair(ui->volume,ui->channel);
            else if (arr[j] == 4)
                p300Array[j] = std::make_pair(ui->power,ui->home);
        }
    else if (!(ui->volume_widget->isHidden()))
        for (int j = 0; j < TestSize - 1;j++)
        {
            if (arr[j] == 1)
                p300Array[j] = std::make_pair(ui->plus_volume,ui->mute_volume);
            else if (arr[j] == 2)
                p300Array[j] = std::make_pair(ui->minus_volume,ui->home);
            else if (arr[j] == 3)
                p300Array[j] = std::make_pair(ui->plus_volume,ui->minus_volume);
            else if (arr[j] == 4)
                p300Array[j] = std::make_pair(ui->mute_volume,ui->home);
        }
    else if (!(ui->channel_widget->isHidden()))
        for (int j = 0; j < TestSize - 1;j++)
        {
            if (arr[j] == 1)
                p300Array[j] = std::make_pair(ui->plus_channel,ui->favorite_channel);
            else if (arr[j] == 2)
                p300Array[j] = std::make_pair(ui->minus_channel,ui->home);
            else if (arr[j] == 3)
                p300Array[j] = std::make_pair(ui->plus_channel,ui->minus_channel);
            else if (arr[j] == 4)
                p300Array[j] = std::make_pair(ui->favorite_channel,ui->home);
        }

}

void MainWindow::start() {
    startTime = clock();
}
unsigned long MainWindow::elapsedTime() {
    return ((unsigned long) clock() - startTime) / (CLOCKS_PER_SEC/1000);
}

void MainWindow::p300Effect()
{
    using namespace std::this_thread; // sleep_for, sleep_until
    using namespace std::chrono; // nanoseconds, system_clock, seconds

    int longueurOnde = BSLEEPTIME + ASLEEPTIME;                      // Temps d'une iteration
    std::string initialUdpSignal;
    initialUdpSignal = std::to_string(longueurOnde);
    initialUdpSignal += (" " + mode);                                  // Mode du P300

    for (int i = 0; i < TestSize; i++)                               // Concatenation des lignes et colonnes
    {
        initialUdpSignal += (" " + udpArr[i]);
    }

    initialUdpSignal += " DONE";
    const char* initialUdpSignal_char = initialUdpSignal.c_str();
    if (sendto(s, initialUdpSignal_char, int(strlen(initialUdpSignal_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }

/*
    std::string messageDebut = "DONE";
    const char* messageDebut_char = messageDebut.c_str();
    if (sendto(s, messageDebut_char, int(strlen(messageDebut_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }
*/
/*
    std::string finArrayS = std::to_string(startTime);
    const char* finArrayS_char = finArrayS.c_str();
    if (sendto(s, finArrayS_char, int(strlen(finArrayS_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }
    std::string finArrayB = std::to_string(BSLEEPTIME);
    const char* finArrayB_char = finArrayB.c_str();
    if (sendto(s, finArrayB_char, int(strlen(finArrayB_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }
    std::string finArrayA = std::to_string(ASLEEPTIME);
    const char* finArrayA_char = finArrayA.c_str();
    if (sendto(s, finArrayA_char, int(strlen(finArrayA_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }
*/
    for (int i = 0; i < TestSize - 1 && stop == false  ;i++)
    {
        start();
        // TOSEND: time a chaque je sais pas trop combien de temps et mon index (modulo nombre itteration).
        if (i%5 == 0) //a tous les 5, on envoie un message
        {
            std::string messageIteratif = std::to_string(startTime) + " " + std::to_string(i);
            const char* messageIteratif_char = messageIteratif.c_str();
            if (sendto(s, messageIteratif_char, int(strlen(messageIteratif_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
            {
                printf("sendto() failed with error code : %d", WSAGetLastError());
                exit(EXIT_FAILURE);
            }
        }


        p300Array[i].first->toggled(true);
        p300Array[i].second->toggled(true);
        qApp->processEvents();
        sleep_for(milliseconds(BSLEEPTIME));
        p300Array[i].first->toggled(false);
        p300Array[i].second->toggled(false);
        sleep_for(milliseconds(ASLEEPTIME));
    }
    std::string messageENDED = "ENDED";
    const char* messageENDED_char = messageENDED.c_str();
    if (sendto(s, messageENDED_char, int(strlen(messageENDED_char)), 0, (struct sockaddr *) &si_other, slen) == SOCKET_ERROR)
    {
        printf("sendto() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
    }
    stop = false;
}


void MainWindow::ButtonToggleFunction(QPushButton *button,bool checked, QString whitePic, QString blackPic)
{
    QIcon *ico;

    if (checked)
    {

        QPixmap pixW(whitePic);
        ico = new QIcon(pixW);
        button->setIcon(*ico);
        button->setIconSize(pixW.size());
    }
    else
    {
        QPixmap pixB(blackPic);
        ico = new QIcon(pixB);
        button->setIcon(*ico);
        button->setIconSize(pixB.size());
    }

    //button->setCheckable(true);
}


void MainWindow::on_volume_toggled(bool checked)
{
    ButtonToggleFunction(ui->volume, checked,":/Buttons/VolumeButtonWhite.png", ":/Buttons/VolumeButtonBlack.png");
}


void MainWindow::on_volume_clicked()
{
    ui->home_widget->hide();
    ui->channel_widget->hide();
    ui->volume_widget->show();
}


void MainWindow::on_home_clicked()
{
    ui->volume_widget->hide();
    ui->channel_widget->hide();
    ui->home_widget->show();
}


void MainWindow::on_channel_clicked()
{
    ui->home_widget->hide();
    ui->volume_widget->hide();
    ui->channel_widget->show();
}

void MainWindow::on_minus_volume_toggled(bool checked)
{
    ButtonToggleFunction(ui->minus_volume, checked,":/Buttons/MinusButtonWhite.png", ":/Buttons/MinusButtonBlack.png");
}

void MainWindow::on_mute_volume_toggled(bool checked)
{
    ButtonToggleFunction(ui->mute_volume, checked,":/Buttons/MuteButtonWhite.png", ":/Buttons/MuteButtonBlack.png");
}

void MainWindow::on_plus_volume_toggled(bool checked)
{
    ButtonToggleFunction(ui->plus_volume, checked,":/Buttons/PlusButtonWhite.png", ":/Buttons/PlusButtonBlack.png");
}

void MainWindow::on_favorite_channel_toggled(bool checked)
{
    ButtonToggleFunction(ui->favorite_channel, checked,":/Buttons/FavoriteButtonWhite.png", ":/Buttons/FavoriteButtonBlack.png");
}

void MainWindow::on_minus_channel_toggled(bool checked)
{
    ButtonToggleFunction(ui->minus_channel, checked,":/Buttons/MinusButtonWhite.png", ":/Buttons/MinusButtonBlack.png");
}

void MainWindow::on_plus_channel_toggled(bool checked)
{
    ButtonToggleFunction(ui->plus_channel, checked,":/Buttons/PlusButtonWhite.png", ":/Buttons/PlusButtonBlack.png");
}
void MainWindow::on_channel_toggled(bool checked)
{
    ButtonToggleFunction(ui->channel, checked,":/Buttons/ChannelButtonWhite.png", ":/Buttons/ChannelButtonBlack.png");
}

void MainWindow::on_home_toggled(bool checked)
{
    ButtonToggleFunction(ui->home, checked,":/Buttons/HomeButtonWhite.png", ":/Buttons/HomeButtonBlack.png");
}

void MainWindow::on_power_toggled(bool checked)
{
    ButtonToggleFunction(ui->power, checked,":/Buttons/PowerButtonWhite.png", ":/Buttons/PowerButtonBlack.png");
}

void MainWindow::on_pushButton_pressed()
{
    ui->pushButton->setEnabled(false);
    ui->pushButton_2->setEnabled(true);
    ui->frequency_Aspin->setEnabled(false);
    ui->frequency_Bspin->setEnabled(false);
    randomArray();
    p300Effect();
    ui->pushButton->setEnabled(true);
    ui->pushButton_2->setEnabled(false);
    ui->frequency_Aspin->setEnabled(true);
    ui->frequency_Bspin->setEnabled(true);
}

void MainWindow::on_pushButton_2_pressed()
{
    stop = true;
}

void MainWindow::on_frequency_Bspin_valueChanged()
{
    BSLEEPTIME = ui->frequency_Bspin->value();
}

void MainWindow::on_frequency_Aspin_valueChanged()
{
    ASLEEPTIME = ui->frequency_Aspin->value();
}




void MainWindow::on_freemode_radioButton_clicked()
{
    mode = "F";
}

void MainWindow::on_acquisition_radioButton_clicked()
{
    mode = "T";
}

void MainWindow::on_p300remote_radioButton_clicked()
{
    mode = "U";
}
