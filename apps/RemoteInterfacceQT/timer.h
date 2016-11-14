#ifndef TIMER_H
#define TIMER_H
#include <ctime>

class Timer : public QObject
{
    Q_OBJECT
private:
    unsigned long startTime;
public:
    Timer(QObject* parent = 0);
    ~Timer();
    void start() {
        startTime = clock();
    }

    unsigned long elapsedTime() {
        return ((unsigned long) clock() - startTime) / 1000;
    }

    bool isTimeout(unsigned long seconds) {
        return seconds >= elapsedTime();
    }
};

#endif // TIMER_H

