/*
 * command_parser.c
 *
 *  Created on: Jan 10, 2022
 *      Author: ngocc
 */
#include "command_parser.h"


uint8_t command_done = 0;

char command[COMMAND_SIZE];
int command_index = 0;

enum parser_state {WAITING_START, WAITING_END};

enum parser_state parserState = WAITING_START;

void command_parser(uint8_t temp) {
	switch(parserState) {
	case WAITING_START:
		if (temp == '!') {
			parserState = WAITING_END;
			command_index = 0;
		}
		break;
	case WAITING_END:
		if (temp == '#') {
			command[command_index] = '\0';
			parserState = WAITING_START;
			command_done = 1;
		} else if (temp == '!') {
			//trong truong hop nguoi gui khong the gui ki tu ket thuc
			// nen nguoi gui tien hanh gui lai tu dau, khi nay se la ki tu !.
			// nen ta tien hanh xoa toan bo buffer de ghi lai tu dau.
			command_index = 0;
		} else {
			command[command_index++] = temp;
			if (command_index == COMMAND_SIZE) command_index = 0;
		}
		break;
	}
}

uint8_t is_command_done() {
	return command_done;
}

void reset_command() {
	command_done = 0;
}

char* get_command() {
	return command;
}
