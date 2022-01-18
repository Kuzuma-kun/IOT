/*
 * uart_comm.c
 *
 *  Created on: Jan 10, 2022
 *      Author: ngocc
 */
#include <string.h>
#include "command_parser.h"
#include "uart_comm.h"
#include "main.h"
#include <stdio.h>

enum uart_state {IDLE, LED, END};
enum uart_state uart_State = IDLE;
char* tok = NULL;

UART_HandleTypeDef huart2;
UART_HandleTypeDef huart1;
static char received_command[50];
static char command[50];
void uart_comm() {
	switch(uart_State) {
	case IDLE:
//		HAL_UART_Transmit(&huart1, (uint8_t*)received_command,
//				sprintf(received_command, "\r\ninput string is: %s \r\n", get_command()), 1000);

		strcpy(command, get_command());
		tok = strtok(command, ":");
		if (strcmp(tok, "LED") == 0) {
			uart_State = LED;
		} else {
			uart_State = END;
		}
	break;
	case LED:
		tok = strtok(NULL, ":");
		if (strcmp(tok, "ON") == 0) {
			HAL_UART_Transmit(&huart1, "I was here!", 12, 1200);
			HAL_GPIO_WritePin(GPIOA, LED_Pin, GPIO_PIN_SET);
		} else {
			HAL_GPIO_WritePin(GPIOA, LED_Pin, GPIO_PIN_RESET);
		}
		uart_State = END;
	break;
	case END:
		reset_command();
		uart_State = IDLE;
	break;

	}
//	if (tok == NULL) {
//		char yo[] = "NULL";
//		HAL_UART_Transmit(&huart1, (uint8_t*)yo, sizeof(yo), 1000);
//	} else {
//		HAL_UART_Transmit(&huart1, (uint8_t*)tok, sizeof(tok), 1000);
//	}
}
