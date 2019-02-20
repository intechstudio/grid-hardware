/*
 * Code generated from Atmel Start.
 *
 * This file will be overwritten when reconfiguring your Atmel Start project.
 * Please copy examples or other code you want to keep to a separate file
 * to avoid losing it when reconfiguring.
 */

#include "driver_examples.h"
#include "driver_init.h"
#include "utils.h"

static uint8_t src_data[512];
static uint8_t chk_data[512];
/**
 * Example of using FLASH_0 to read and write Flash main array.
 */
void FLASH_0_example(void)
{
	uint32_t page_size;
	uint16_t i;

	/* Init source data */
	page_size = flash_get_page_size(&FLASH_0);

	for (i = 0; i < page_size; i++) {
		src_data[i] = i;
	}

	/* Write data to flash */
	flash_write(&FLASH_0, 0x3200, src_data, page_size);

	/* Read data from flash */
	flash_read(&FLASH_0, 0x3200, chk_data, page_size);
}

static uint8_t buf[16] = {0x0};

static void xfer_complete_cb_SYS_QSPI(struct _dma_resource *resource)
{
	/* Transfer completed */
}

/**
 * Example of using SYS_QSPI to get N25Q256A status value,
 * and check bit 0 which indicate embedded operation is busy or not.
 */
void SYS_QSPI_example(void)
{
	struct _qspi_command cmd = {
	    .inst_frame.bits.inst_en      = 1,
	    .inst_frame.bits.data_en      = 1,
	    .inst_frame.bits.addr_en      = 1,
	    .inst_frame.bits.dummy_cycles = 8,
	    .inst_frame.bits.tfr_type     = QSPI_READMEM_ACCESS,
	    .instruction                  = 0x0B,
	    .address                      = 0,
	    .buf_len                      = 14,
	    .rx_buf                       = buf,
	};

	qspi_dma_register_callback(&SYS_QSPI, QSPI_DMA_CB_XFER_DONE, xfer_complete_cb_SYS_QSPI);
	qspi_dma_enable(&SYS_QSPI);
	qspi_dma_serial_run_command(&SYS_QSPI, &cmd);
}

/**
 * Example of using GRID_EAST to write "Hello World" using the IO abstraction.
 *
 * Since the driver is asynchronous we need to use statically allocated memory for string
 * because driver initiates transfer and then returns before the transmission is completed.
 *
 * Once transfer has been completed the tx_cb function will be called.
 */

static uint8_t example_GRID_EAST[12] = "Hello World!";

static void tx_cb_GRID_EAST(const struct usart_async_descriptor *const io_descr)
{
	/* Transfer completed */
}

void GRID_EAST_example(void)
{
	struct io_descriptor *io;

	usart_async_register_callback(&GRID_EAST, USART_ASYNC_TXC_CB, tx_cb_GRID_EAST);
	/*usart_async_register_callback(&GRID_EAST, USART_ASYNC_RXC_CB, rx_cb);
	usart_async_register_callback(&GRID_EAST, USART_ASYNC_ERROR_CB, err_cb);*/
	usart_async_get_io_descriptor(&GRID_EAST, &io);
	usart_async_enable(&GRID_EAST);

	io_write(io, example_GRID_EAST, 12);
}

/**
 * Example of using GRID_NORTH to write "Hello World" using the IO abstraction.
 *
 * Since the driver is asynchronous we need to use statically allocated memory for string
 * because driver initiates transfer and then returns before the transmission is completed.
 *
 * Once transfer has been completed the tx_cb function will be called.
 */

static uint8_t example_GRID_NORTH[12] = "Hello World!";

static void tx_cb_GRID_NORTH(const struct usart_async_descriptor *const io_descr)
{
	/* Transfer completed */
}

void GRID_NORTH_example(void)
{
	struct io_descriptor *io;

	usart_async_register_callback(&GRID_NORTH, USART_ASYNC_TXC_CB, tx_cb_GRID_NORTH);
	/*usart_async_register_callback(&GRID_NORTH, USART_ASYNC_RXC_CB, rx_cb);
	usart_async_register_callback(&GRID_NORTH, USART_ASYNC_ERROR_CB, err_cb);*/
	usart_async_get_io_descriptor(&GRID_NORTH, &io);
	usart_async_enable(&GRID_NORTH);

	io_write(io, example_GRID_NORTH, 12);
}

/**
 * Example of using GRID_AUX to write "Hello World" using the IO abstraction.
 */
void GRID_AUX_example(void)
{
	struct io_descriptor *io;
	usart_sync_get_io_descriptor(&GRID_AUX, &io);
	usart_sync_enable(&GRID_AUX);

	io_write(io, (uint8_t *)"Hello World!", 12);
}

/**
 * Example of using GRID_WEST to write "Hello World" using the IO abstraction.
 *
 * Since the driver is asynchronous we need to use statically allocated memory for string
 * because driver initiates transfer and then returns before the transmission is completed.
 *
 * Once transfer has been completed the tx_cb function will be called.
 */

static uint8_t example_GRID_WEST[12] = "Hello World!";

static void tx_cb_GRID_WEST(const struct usart_async_descriptor *const io_descr)
{
	/* Transfer completed */
}

void GRID_WEST_example(void)
{
	struct io_descriptor *io;

	usart_async_register_callback(&GRID_WEST, USART_ASYNC_TXC_CB, tx_cb_GRID_WEST);
	/*usart_async_register_callback(&GRID_WEST, USART_ASYNC_RXC_CB, rx_cb);
	usart_async_register_callback(&GRID_WEST, USART_ASYNC_ERROR_CB, err_cb);*/
	usart_async_get_io_descriptor(&GRID_WEST, &io);
	usart_async_enable(&GRID_WEST);

	io_write(io, example_GRID_WEST, 12);
}

static uint8_t SYS_I2C_example_str[12] = "Hello World!";

void SYS_I2C_tx_complete(struct i2c_m_async_desc *const i2c)
{
}

void SYS_I2C_example(void)
{
	struct io_descriptor *SYS_I2C_io;

	i2c_m_async_get_io_descriptor(&SYS_I2C, &SYS_I2C_io);
	i2c_m_async_enable(&SYS_I2C);
	i2c_m_async_register_callback(&SYS_I2C, I2C_M_ASYNC_TX_COMPLETE, (FUNC_PTR)SYS_I2C_tx_complete);
	i2c_m_async_set_slaveaddr(&SYS_I2C, 0x12, I2C_M_SEVEN);

	io_write(SYS_I2C_io, SYS_I2C_example_str, 12);
}

/**
 * Example of using GRID_SOUTH to write "Hello World" using the IO abstraction.
 *
 * Since the driver is asynchronous we need to use statically allocated memory for string
 * because driver initiates transfer and then returns before the transmission is completed.
 *
 * Once transfer has been completed the tx_cb function will be called.
 */

static uint8_t example_GRID_SOUTH[12] = "Hello World!";

static void tx_cb_GRID_SOUTH(const struct usart_async_descriptor *const io_descr)
{
	/* Transfer completed */
}

void GRID_SOUTH_example(void)
{
	struct io_descriptor *io;

	usart_async_register_callback(&GRID_SOUTH, USART_ASYNC_TXC_CB, tx_cb_GRID_SOUTH);
	/*usart_async_register_callback(&GRID_SOUTH, USART_ASYNC_RXC_CB, rx_cb);
	usart_async_register_callback(&GRID_SOUTH, USART_ASYNC_ERROR_CB, err_cb);*/
	usart_async_get_io_descriptor(&GRID_SOUTH, &io);
	usart_async_enable(&GRID_SOUTH);

	io_write(io, example_GRID_SOUTH, 12);
}

void delay_example(void)
{
	delay_ms(5000);
}
