#include <atmel_start.h>

int main(void)
{
	/* Initializes MCU, drivers and middleware */
	atmel_start_init();


	//gpio_set_pin_function(DAC0, GPIO_PIN_FUNCTION_OFF);

	// GPIO on PB14

	
	/* Replace with your application code */
	while (1) {
		
		gpio_set_pin_level(DAC1, true);
		delay_ms(100);
		gpio_set_pin_level(DAC1, false);
		delay_ms(100);
		
	}
}
