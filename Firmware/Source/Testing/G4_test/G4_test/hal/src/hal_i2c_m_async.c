/**
 * \file
 *
 * \brief I/O I2C related functionality implementation.
 *
 * Copyright (c) 2014-2018 Microchip Technology Inc. and its subsidiaries.
 *
 * \asf_license_start
 *
 * \page License
 *
 * Subject to your compliance with these terms, you may use Microchip
 * software and any derivatives exclusively with Microchip products.
 * It is your responsibility to comply with third party license terms applicable
 * to your use of third party software (including open source software) that
 * may accompany Microchip software.
 *
 * THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES,
 * WHETHER EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE,
 * INCLUDING ANY IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY,
 * AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT WILL MICROCHIP BE
 * LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, INCIDENTAL OR CONSEQUENTIAL
 * LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND WHATSOEVER RELATED TO THE
 * SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP HAS BEEN ADVISED OF THE
 * POSSIBILITY OR THE DAMAGES ARE FORESEEABLE.  TO THE FULLEST EXTENT
 * ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL CLAIMS IN ANY WAY
 * RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT OF FEES, IF ANY,
 * THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS SOFTWARE.
 *
 * \asf_license_stop
 *
 */
#include <hal_i2c_m_async.h>
#include <utils.h>
#include <utils_assert.h>

/**
 * \brief Driver version
 */
#define DRIVER_VERSION 0x00000001u

/**
 * \brief Callback function for tx complete
 */
static void i2c_tx_complete(struct _i2c_m_async_device *const i2c_dev)
{
	struct i2c_m_async_desc *i2c = CONTAINER_OF(i2c_dev, struct i2c_m_async_desc, device);

	if (!(i2c_dev->service.msg.flags & I2C_M_BUSY)) {
		if (i2c->i2c_cb.tx_complete) {
			i2c->i2c_cb.tx_complete(i2c);
		}
	}
}

/**
 * \brief Callback function for rx complete
 */
static void i2c_rx_complete(struct _i2c_m_async_device *const i2c_dev)
{
	struct i2c_m_async_desc *i2c = CONTAINER_OF(i2c_dev, struct i2c_m_async_desc, device);

	if (!(i2c_dev->service.msg.flags & I2C_M_BUSY)) {
		if (i2c->i2c_cb.rx_complete) {
			i2c->i2c_cb.rx_complete(i2c);
		}
	}
}

static void i2c_error(struct _i2c_m_async_device *const i2c_dev, int32_t error)
{
	struct i2c_m_async_desc *i2c = CONTAINER_OF(i2c_dev, struct i2c_m_async_desc, device);

	if (!(i2c_dev->service.msg.flags & I2C_M_BUSY)) {
		if (i2c->i2c_cb.error) {
			i2c->i2c_cb.error(i2c, error);
		}
	}
}

/**
 * \brief Async version of I2C I/O read
 */
static int32_t i2c_m_async_read(struct io_descriptor *const io, uint8_t *buf, const uint16_t n)
{
	struct i2c_m_async_desc *i2c = CONTAINER_OF(io, struct i2c_m_async_desc, io);
	struct _i2c_m_msg        msg;
	int32_t                  ret;

	msg.addr   = i2c->slave_addr;
	msg.len    = n;
	msg.flags  = I2C_M_STOP | I2C_M_RD;
	msg.buffer = buf;

	/* start transfer then return */
	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		return ret;
	}

	return (int32_t)n;
}

/**
 * \brief Async version of I2C I/O write
 */
static int32_t i2c_m_async_write(struct io_descriptor *const io, const uint8_t *buf, const uint16_t n)
{
	struct i2c_m_async_desc *i2c = CONTAINER_OF(io, struct i2c_m_async_desc, io);
	struct _i2c_m_msg        msg;
	int32_t                  ret;

	msg.addr   = i2c->slave_addr;
	msg.len    = n;
	msg.flags  = I2C_M_STOP;
	msg.buffer = (uint8_t *)buf;

	/* start transfer then return */
	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		return ret;
	}

	return (int32_t)n;
}

/**
 * \brief Async version of i2c initialize
 */
int32_t i2c_m_async_init(struct i2c_m_async_desc *const i2c, void *const hw)
{
	int32_t init_status;
	ASSERT(i2c);

	init_status = _i2c_m_async_init(&i2c->device, hw);
	if (init_status) {
		return init_status;
	}
	/* Init I/O */
	i2c->io.read  = i2c_m_async_read;
	i2c->io.write = i2c_m_async_write;

	/* Init callbacks */
	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_TX_COMPLETE, (FUNC_PTR)i2c_tx_complete);
	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_RX_COMPLETE, (FUNC_PTR)i2c_rx_complete);
	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_ERROR, (FUNC_PTR)i2c_error);

	return ERR_NONE;
}

/**
 * \brief Deinitialize
 */
int32_t i2c_m_async_deinit(struct i2c_m_async_desc *const i2c)
{
	int32_t status;
	ASSERT(i2c);

	status = _i2c_m_async_deinit(&i2c->device);
	if (status) {
		return status;
	}

	i2c->io.read  = NULL;
	i2c->io.write = NULL;

	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_TX_COMPLETE, NULL);
	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_RX_COMPLETE, NULL);
	_i2c_m_async_register_callback(&i2c->device, I2C_M_ASYNC_DEVICE_ERROR, NULL);

	return ERR_NONE;
}

/**
 * \brief Async version of i2c enable
 */
int32_t i2c_m_async_enable(struct i2c_m_async_desc *const i2c)
{
	int32_t rc;

	ASSERT(i2c);

	rc = _i2c_m_async_enable(&i2c->device);
	if (rc == ERR_NONE) {
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_TX_COMPLETE, true);
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_RX_COMPLETE, true);
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_ERROR, true);
	}
	return rc;
}

/**
 * \brief Async version of i2c disable
 */
int32_t i2c_m_async_disable(struct i2c_m_async_desc *const i2c)
{
	int32_t rc;

	ASSERT(i2c);

	rc = _i2c_m_async_disable(&i2c->device);
	if (rc == ERR_NONE) {
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_TX_COMPLETE, false);
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_RX_COMPLETE, false);
		_i2c_m_async_set_irq_state(&i2c->device, I2C_M_ASYNC_DEVICE_ERROR, false);
	}
	return rc;
}

/**
 * \brief Async version of i2c set slave address
 */
int32_t i2c_m_async_set_slaveaddr(struct i2c_m_async_desc *const i2c, int16_t addr, int32_t addr_len)
{
	return i2c->slave_addr = (addr & 0x3ff) | (addr_len & I2C_M_TEN);
}

/**
 * \brief I2c register callback
 */
int32_t i2c_m_async_register_callback(struct i2c_m_async_desc *const i2c, enum i2c_m_async_callback_type type,
                                      FUNC_PTR func)
{
	switch (type) {
	case I2C_M_ASYNC_ERROR:
		i2c->i2c_cb.error = (i2c_error_cb_t)func;
		break;
	case I2C_M_ASYNC_TX_COMPLETE:
		i2c->i2c_cb.tx_complete = (i2c_complete_cb_t)func;
		break;
	case I2C_M_ASYNC_RX_COMPLETE:
		i2c->i2c_cb.rx_complete = (i2c_complete_cb_t)func;
		break;
	default:
		/* error */
		return ERR_INVALID_ARG;
	}
	return I2C_OK;
}

/**
 * \brief Async version of i2c set baudrate
 */
int32_t i2c_m_async_set_baudrate(struct i2c_m_async_desc *const i2c, uint32_t clkrate, uint32_t baudrate)
{
	return _i2c_m_async_set_baudrate(&i2c->device, clkrate, baudrate);
}

/**
 * \brief Async version of i2c write command
 */
int32_t i2c_m_async_cmd_write(struct i2c_m_async_desc *const i2c, uint8_t reg, uint8_t value)
{
	struct _i2c_m_msg msg;
	int32_t           ret;

	msg.addr   = i2c->slave_addr;
	msg.len    = 1;
	msg.flags  = 0;
	msg.buffer = &reg;

	i2c->device.cb.tx_complete = NULL;

	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		/* re-register to enable notify user callback */
		i2c->device.cb.tx_complete = i2c_tx_complete;
		return ret;
	}

	/* we polling busy flag wait for send finish here */
	while (i2c->device.service.msg.flags & I2C_M_BUSY) {
		;
	}

	i2c->device.cb.tx_complete = i2c_tx_complete;

	msg.flags  = I2C_M_STOP;
	msg.buffer = &value;

	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		return ret;
	}

	return I2C_OK;
}

/**
 * \brief Async version of i2c read command
 */
int32_t i2c_m_async_cmd_read(struct i2c_m_async_desc *const i2c, uint8_t reg, uint8_t *value)
{
	struct _i2c_m_msg msg;
	int32_t           ret;

	msg.addr   = i2c->slave_addr;
	msg.len    = 1;
	msg.flags  = 0;
	msg.buffer = &reg;

	i2c->device.cb.tx_complete = NULL;

	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		/* re-register to enable notify user callback */
		i2c->device.cb.tx_complete = i2c_tx_complete;
		return ret;
	}

	/* we polling busy flag wait for send finish here */
	while (i2c->device.service.msg.flags & I2C_M_BUSY) {
		;
	}

	/* re-register to enable notify user callback */
	i2c->device.cb.tx_complete = i2c_tx_complete;

	msg.flags  = I2C_M_STOP | I2C_M_RD;
	msg.buffer = value;

	ret = _i2c_m_async_transfer(&i2c->device, &msg);

	if (ret != 0) {
		/* error occurred */
		return ret;
	}

	return I2C_OK;
}

int32_t i2c_m_async_transfer(struct i2c_m_async_desc *const i2c, struct _i2c_m_msg *msg)
{
	return _i2c_m_async_transfer(&i2c->device, msg);
}

/**
 * \brief Send stop condition
 */
int32_t i2c_m_async_send_stop(struct i2c_m_async_desc *const i2c)
{
	return _i2c_m_async_send_stop(&i2c->device);
}

/**
 * \brief Get bytes left in message buffer
 */
int32_t i2c_m_async_get_status(struct i2c_m_async_desc *const i2c, struct i2c_m_async_status *stat)
{
	ASSERT(i2c && stat);
	/* Get a copy of status to avoid critical issue */
	volatile uint16_t *tmp_stat = &(i2c->device.service.msg.flags);
	volatile int32_t * tmp_left = &(i2c->device.service.msg.len);

	if (*tmp_stat == I2C_M_BUSY) {
		stat->flags = *tmp_stat;
		stat->left  = *tmp_left;
		return ERR_BUSY;
	}

	return ERR_NONE;
}

/**
 * \brief Retrieve I/O descriptor
 */
int32_t i2c_m_async_get_io_descriptor(struct i2c_m_async_desc *const i2c, struct io_descriptor **io)
{
	*io = &i2c->io;
	return ERR_NONE;
}

/**
 * \brief Retrieve the current driver version
 */
uint32_t i2c_m_get_version(void)
{
	return DRIVER_VERSION;
}
