/*
 * timer.c
 *
 *  Created on: Jan 10, 2022
 *      Author: ngocc
 */

#include "timer.h"

#define NUM_OF_TIMER 3
#define TIME_PERIOD 10

static int timer_counter[NUM_OF_TIMER];
static int timer_flag[NUM_OF_TIMER];

void start_timer(int index) {
	timer_flag[index] = 1;
}

void run_timer(int index) {
	if (timer_counter[index] > 0) {
		timer_counter[index]--;
		if (timer_counter[index] <= 0) {
			timer_flag[index] = 1;
		}
	}
}

void init_timer(int index, int duration, int time_period_ms) {
	timer_counter[index] = duration/time_period_ms;
	timer_flag[index] = 0;
 }

void stop_timer(int index) {
	timer_flag[index] = 0;
	timer_counter[index] = 0;
}

int get_timer_flag(int index) {
	if (index >= NUM_OF_TIMER) return 0xffffffff;
	return timer_flag[index];
}
