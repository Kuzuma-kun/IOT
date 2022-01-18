/*
 * command_parser.h
 *
 *  Created on: Jan 10, 2022
 *      Author: ngocc
 */

#ifndef INC_COMMAND_PARSER_H_
#define INC_COMMAND_PARSER_H_

#include "main.h"
#define COMMAND_SIZE 50

void command_parser(uint8_t temp);

uint8_t is_command_done();
void reset_command();
char* get_command();

#endif /* INC_COMMAND_PARSER_H_ */
