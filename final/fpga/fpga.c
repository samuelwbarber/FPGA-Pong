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

void display_score(int number){
	int out = 0;
	if (number == 0){
		out = 0b1000000;
	}if (number == 1){
		out = 0b1111001;
	}if (number == 2){
		out = 0b0100100;
	}if (number == 3){
		out = 0b0110000;
	}if (number == 4){
		out = 0b0011001;
	}if (number == 5){
		out = 0b0010010;
	}if (number == 6){
		out = 0b0000010;
	}if (number == 7){
		out = 0b1111000;
	}if (number == 8){
		out = 0b0000000;
	}if (number == 9){
		out = 0b0011000;
	}
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_0_BASE, out);
}

// converts accelerometer data into led lights
void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

// function to handle diff button modes
void buttons(){

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

    // reset score to 0
//    display_score(HEX_0_BASE, 0);

    timer_init(sys_timer_isr);
    while (1) {
        if (fp) {
        	char text[2 * CHARLIM];
    		int buffer_index = 0;
//    		int score = alt_getchar() - '0';
//    		display_score(score);

        	for (int i = 0; i < 50; i++){
        		alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
				int filtered = apply_filter_float(x_read);
				convert_read(filtered, & level, & led);

				scaled = (abs(filtered)*SCALE)/260;
//
				char scaled_c = '0' + scaled;

				if (x_read < 0){
					text[buffer_index++] = '-';
				}

				text[buffer_index++] = scaled_c;

//				char digits[3];
//				int num_digits = 0;
//				do {
//					digits[num_digits++] = scaled % 10 + '0';
//					scaled /= 10;
//				} while (scaled != 0);
//
//				// Add digits to text in correct order
//				for (int j = num_digits -1; j >= 0; j--) {
//					text[buffer_index++] = digits[j];
//				}

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

