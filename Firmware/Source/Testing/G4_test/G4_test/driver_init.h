/*
 * Code generated from Atmel Start.
 *
 * This file will be overwritten when reconfiguring your Atmel Start project.
 * Please copy examples or other code you want to keep to a separate file
 * to avoid losing it when reconfiguring.
 */
#ifndef DRIVER_INIT_INCLUDED
#define DRIVER_INIT_INCLUDED

#include "atmel_start_pins.h"

#ifdef __cplusplus
extern "C" {
#endif

#include <hal_atomic.h>
#include <hal_delay.h>
#include <hal_gpio.h>
#include <hal_init.h>
#include <hal_io.h>
#include <hal_sleep.h>

#include <hal_flash.h>

#include <hal_qspi_dma.h>

#include <hal_usart_async.h>
#include <hal_usart_async.h>

#include <hal_usart_sync.h>
#include <hal_usart_async.h>

#include <hal_i2c_m_async.h>
#include <hal_usart_async.h>

#include <hal_delay.h>

#include "hal_usb_device.h"

extern struct flash_descriptor FLASH_0;

extern struct qspi_dma_descriptor    SYS_QSPI;
extern struct usart_async_descriptor GRID_EAST;
extern struct usart_async_descriptor GRID_NORTH;

extern struct usart_sync_descriptor  GRID_AUX;
extern struct usart_async_descriptor GRID_WEST;

extern struct i2c_m_async_desc       SYS_I2C;
extern struct usart_async_descriptor GRID_SOUTH;

void FLASH_0_init(void);
void FLASH_0_CLOCK_init(void);

void SYS_QSPI_PORT_init(void);
void SYS_QSPI_CLOCK_init(void);
void SYS_QSPI_init(void);

void GRID_EAST_PORT_init(void);
void GRID_EAST_CLOCK_init(void);
void GRID_EAST_init(void);

void GRID_NORTH_PORT_init(void);
void GRID_NORTH_CLOCK_init(void);
void GRID_NORTH_init(void);

void GRID_AUX_PORT_init(void);
void GRID_AUX_CLOCK_init(void);
void GRID_AUX_init(void);

void GRID_WEST_PORT_init(void);
void GRID_WEST_CLOCK_init(void);
void GRID_WEST_init(void);

void SYS_I2C_PORT_init(void);
void SYS_I2C_CLOCK_init(void);
void SYS_I2C_init(void);

void GRID_SOUTH_PORT_init(void);
void GRID_SOUTH_CLOCK_init(void);
void GRID_SOUTH_init(void);

void delay_driver_init(void);

void USB_0_CLOCK_init(void);
void USB_0_init(void);

/**
 * \brief Perform system initialization, initialize pins and clocks for
 * peripherals
 */
void system_init(void);

#ifdef __cplusplus
}
#endif
#endif // DRIVER_INIT_INCLUDED
