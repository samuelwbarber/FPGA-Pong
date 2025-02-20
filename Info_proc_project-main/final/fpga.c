#include <stdio.h>
#include <string.h>
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>
#include <sys/alt_stdio.h>

#define QUITLETTER 'q' // Letter to kill all processing
#define CHARLIM 256

#define OFFSET -32
#define PWM_PERIOD 16

#define FILTER_TAP_NUM 5
#define FRACTIONAL_BITS 3
#define SCALE 9

alt_8 pwm = 0;
alt_u8 led;
int level;
alt_u8 scaled = 0;

float filter_coefficients[FILTER_TAP_NUM] = {0.2, 0.2, 0.2, 0.2, 0.2};
float filter_state[FILTER_TAP_NUM] = {0};


void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

int display_score(int number){
	int out;
	if (number == 0){
		out = 0b1000000;
	}
	else if (number == 1){
		out = 0b1111001;
	}
	else if (number == 2){
		out = 0b0100100;
	}
	else if (number == 3){
		out = 0b0110000;
	}
	else if (number == 4){
		out = 0b0011001;
	}
	else if (number == 5){
		out = 0b0010010;
	}
	else{
		out = 0b1111111;
	}
	return out;
}

void display(int mode, int score){
	int hex0, hex1, hex2, hex3, hex4, hex5;

	if (mode == 0){ // start - sc [score]
		hex5 = 0b1111111;
		hex4 = 0b1111111;
		hex3 = 0b0010010;
		hex2 = 0b1000110;
		hex1 = 0b1111111;
		hex0 = display_score(score);
	}
	else if (mode == 1){ // win - yay
		hex5 = 0b1111111;
		hex4 = 0b1111111;
		hex3 = 0b1111111;
		hex2 = 0b0010001;
		hex1 = 0b0001000;
		hex0 = 0b0010001;
	}
	else if (mode == 2){ // lose - L
		hex5 = 0b1111111;
		hex4 = 0b1111111;
		hex3 = 0b1111111;
		hex2 = 0b1111111;
		hex1 = 0b1111111;
		hex0 = 0b1000111;
	}
	else if (mode == 3){ // countdown
		hex5 = 0b1111111;
		hex4 = 0b1111111;
		hex3 = 0b1111111;
		hex2 = 0b1111111;
		hex1 = 0b1111111;
		hex0 = display_score(score);
	}
	else{
		hex5 = 0b1111111;
		hex4 = 0b1111111;
		hex3 = 0b1111111;
		hex2 = 0b1111111;
		hex1 = 0b1111111;
		hex0 = 0b1111111;
	}

	IOWR_ALTERA_AVALON_PIO_DATA(HEX_0_BASE, hex0);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_1_BASE, hex1);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_2_BASE, hex2);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_3_BASE, hex3);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_4_BASE, hex4);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_5_BASE, hex5);
}

void flash_leds(){
	IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, 0b1111111111);
//	IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, 0b0000000000);
//	IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, 0b1111111111);
}

// converts accelerometer data into led lights
void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}


// function to filter accelerometer data - from lab 3
float apply_filter_float(int new_data) {
	int filtered_output = 0;
    //Shift state and update with new data

    for (int i = FILTER_TAP_NUM - 1; i > 0; i--) {
        filter_state[i] = filter_state[i - 1];
        filtered_output += filter_coefficients[i] * filter_state[i];
    }

    // Update the first element of  state with new data
    filter_state[0] = new_data;
    filtered_output += filter_coefficients[0] * new_data;

    return filtered_output;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

int main() {

    alt_32 x_read;
    FILE *fp;

    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // cannot be opened
    	printf ("Error: Check if the spi ip name is 'accelerometer_spi' \n");
    	return 1;
    }

    // access stream of data through the jtag_uart
    fp = fopen("/dev/jtag_uart", "w+");

    timer_init(sys_timer_isr);
    int mode = 0;
	display(mode, 0);

    while (1) {
        if (fp) {
        	char text[2 * CHARLIM];
    		int buffer_index = 0;

    		char input = alt_getchar();
			if(input == 'w'){
				display(1, 0);
				flash_leds();
			}
			else if(input == 'l'){
				display(2, 0);
			}
			else if(input == 'd'){
				display(3, 0);
			}
			else if(input == 'c'){
				display(3, 1);
			}
			else if(input == 'b'){
				display(3, 2);
			}
			else if(input == 'a'){
				display(3, 3);
			}
			else{
				display(0, (input - '0'));
			}

        	for (int i = 0; i < 50; i++){
        		alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
				int filtered = apply_filter_float(x_read);
				convert_read(filtered, & level, & led);

				scaled = (abs(filtered)*SCALE)/260;

				char scaled_c = '0' + scaled;

				if (x_read < 0){
					text[buffer_index++] = '-';
				}
				text[buffer_index++] = scaled_c;
				text[buffer_index++] = '\n';

        	}
        	char *printMsg = NULL;
			asprintf(&printMsg, "%s\n", text);
			alt_putstr(printMsg);
			free(printMsg);
			memset(text, 0, 2 * CHARLIM);

			// error handling: if an error occurs, clear file
			if (ferror(fp)) {
				clearerr(fp);
			}
        }

    }

    return 0;
}

