#include "timer.h"

Timer::Timer()
{
    startTime = 0;
}
Timer::~Timer(){}
void Timer::start() {
    startTime = clock();
}
unsigned long Timer::elapsedTime() {
    return ((unsigned long) clock() - startTime) / (CLOCKS_PER_SEC/1000);
}
