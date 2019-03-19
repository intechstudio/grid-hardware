/*
 * Code generated from Atmel Start.
 *
 * This file will be overwritten when reconfiguring your Atmel Start project.
 * Please copy examples or other code you want to keep to a separate file or main.c
 * to avoid loosing it when reconfiguring.
 */
#include "atmel_start.h"
#include "usb_start.h"

/* Max LUN number */
#define CONF_USB_MSC_MAX_LUN 0

#if CONF_USBD_HS_SP
static uint8_t multi_desc_bytes[] = {
    /* Device descriptors and Configuration descriptors list. */
    COMPOSITE_HS_DESCES_LS_FS};
static uint8_t multi_desc_bytes_hs[] = {
    /* Device descriptors and Configuration descriptors list. */
    COMPOSITE_HS_DESCES_HS};
#else
static uint8_t multi_desc_bytes[] = {
    /* Device descriptors and Configuration descriptors list. */
    COMPOSITE_DESCES_LS_FS};
#endif

static struct usbd_descriptors multi_desc[] = {{multi_desc_bytes, multi_desc_bytes + sizeof(multi_desc_bytes)}
#if CONF_USBD_HS_SP
                                               ,
                                               {multi_desc_bytes_hs, multi_desc_bytes_hs + sizeof(multi_desc_bytes_hs)}
#endif
};

/** Ctrl endpoint buffer */
static uint8_t ctrl_buffer[64];

#if CONF_USB_COMPOSITE_CDC_ECHO_DEMO
static uint8_t *cdcdf_demo_buf;
static bool     cdcdf_demo_cb_bulk_out(const uint8_t ep, const enum usb_xfer_code rc, const uint32_t count)
{
	cdcdf_acm_write(cdcdf_demo_buf, count); /* Echo data */
	return false;                           /* No error. */
}
static bool cdcdf_demo_cb_bulk_in(const uint8_t ep, const enum usb_xfer_code rc, const uint32_t count)
{
	cdcdf_acm_read((uint8_t *)cdcdf_demo_buf, CONF_USB_COMPOSITE_CDC_ACM_DATA_BULKIN_MAXPKSZ_HS); /* Another read */
	return false;                                                                                 /* No error. */
}
static bool cdcdf_demo_cb_state_c(usb_cdc_control_signal_t state)
{
	if (state.rs232.DTR) {
		/* After connection the R/W callbacks can be registered */
		cdcdf_acm_register_callback(CDCDF_ACM_CB_READ, (FUNC_PTR)cdcdf_demo_cb_bulk_out);
		cdcdf_acm_register_callback(CDCDF_ACM_CB_WRITE, (FUNC_PTR)cdcdf_demo_cb_bulk_in);
		/* Start Rx */
		cdcdf_acm_read((uint8_t *)cdcdf_demo_buf, CONF_USB_COMPOSITE_CDC_ACM_DATA_BULKIN_MAXPKSZ_HS);
	}
	return false; /* No error. */
}
void cdcdf_acm_demo_init(uint8_t *bulk_packet_buffer)
{
	cdcdf_demo_buf = bulk_packet_buffer;
	cdcdf_acm_register_callback(CDCDF_ACM_CB_STATE_C, (FUNC_PTR)cdcdf_demo_cb_state_c);
}
#endif /* CONF_USB_COMPOSITE_CDC_ECHO_DEMO */

#if CONF_USB_COMPOSITE_HID_MOUSE_DEMO || CONF_USB_COMPOSITE_HID_KEYBOARD_DEMO
static uint32_t pin_btn1, pin_btn2, pin_btn3;
static void     hiddf_demo_sof_event(void)
{
	static uint8_t interval;

#if CONF_USB_COMPOSITE_HID_KEYBOARD_DEMO
	static uint8_t                         b_btn_last_state = false;
	static struct hiddf_kb_key_descriptors key_array[]      = {
        {HID_CAPS_LOCK, false, HID_KB_KEY_UP},
    };
	uint8_t b_btn_state;
#endif

	if (interval++ > 10) {
		interval = 0;

#if CONF_USB_COMPOSITE_HID_MOUSE_DEMO
		if (!gpio_get_pin_level(pin_btn1)) {
			hiddf_mouse_move(-5, HID_MOUSE_X_AXIS_MV);
		}
		if (!gpio_get_pin_level(pin_btn3)) {
			hiddf_mouse_move(5, HID_MOUSE_X_AXIS_MV);
		}
#endif

#if CONF_USB_COMPOSITE_HID_KEYBOARD_DEMO
		if (b_btn_last_state != (b_btn_state = !gpio_get_pin_level(pin_btn2))) {
			b_btn_last_state = b_btn_state;
			if (1 == b_btn_last_state) {
				key_array->state = HID_KB_KEY_DOWN;
			} else {
				key_array->state = HID_KB_KEY_UP;
			}
			hiddf_keyboard_keys_state_change(key_array, 1);
		}
#endif
	}
	(void)pin_btn1;
	(void)pin_btn2;
	(void)pin_btn3;
}
static struct usbdc_handler hiddf_demo_sof_event_h = {NULL, (FUNC_PTR)hiddf_demo_sof_event};
void                        hiddf_demo_init(uint32_t btn1, uint32_t btn2, uint32_t btn3)
{
	pin_btn1 = btn1;
	pin_btn2 = btn2;
	pin_btn3 = btn3;
	usbdc_register_handler(USBDC_HDL_SOF, &hiddf_demo_sof_event_h);
}
#endif /* #if CONF_USB_COMPOSITE_HID_MOUSE_DEMO || CONF_USB_COMPOSITE_HID_KEYBOARD_DEMO */

void composite_device_init(void)
{
	/* usb stack init */
	usbdc_init(ctrl_buffer);

	/* usbdc_register_funcion inside */
#if CONF_USB_COMPOSITE_CDC_ACM_EN
	cdcdf_acm_init();
#endif
#if CONF_USB_COMPOSITE_HID_MOUSE_EN
	hiddf_mouse_init();
#endif
#if CONF_USB_COMPOSITE_HID_KEYBOARD_EN
	hiddf_keyboard_init();
#endif
#if CONF_USB_COMPOSITE_MSC_EN
	mscdf_init(CONF_USB_MSC_MAX_LUN);
#endif
}

void composite_device_start(void)
{
	usbdc_start(multi_desc);
	usbdc_attach();
}

void composite_device_example(void)
{

	/* Initialize */
	/* It's done with system init ... */

	/* Before start do function related initializations */
	/* Add your code here ... */

	/* Start device */
	composite_device_start();

	/* Main loop */
	while (1) {
		if (cdcdf_acm_is_enabled()) {
			/* CDC ACM process*/
		}
		if (hiddf_mouse_is_enabled()) {
			/* HID Mouse process */
		}
		if (hiddf_keyboard_is_enabled()) {
			/* HID Keyboard process */
		};
		if (mscdf_is_enabled()) {
			/* MSC process */
		}
	}
}

void usb_init(void)
{

	composite_device_init();
}
