/*
 * timer.h
 *
 *  Created on: Jan 10, 2022
 *      Author: ngocc
 */

#ifndef INC_TIMER_H_
#define INC_TIMER_H_

#define NUM_OF_TIMER 3
#define TIME_PERIOD 10


void start_timer(int index);

void run_timer(int index);

void init_timer(int index, int duration, int time_period_ms);

void stop_timer(int index);

int get_timer_flag(int index);

#endif /* INC_TIMER_H_ */
