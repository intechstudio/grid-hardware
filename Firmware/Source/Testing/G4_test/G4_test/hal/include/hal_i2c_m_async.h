/**
 * \file
 *
 * \brief Async I2C Hardware Abstraction Layer(HAL) declaration.
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

#ifndef _HAL_I2C_M_ASYNC_H_INCLUDED
#define _HAL_I2C_M_ASYNC_H_INCLUDED

#include <hpl_i2c_m_async.h>
#include <hal_io.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \addtogroup doc_driver_hal_i2c_master_async
 *
 * @{
 */

#define I2C_M_MAX_RETRY 1

/**
 * \brief I2C master callback names
 */
enum i2c_m_async_callback_type { I2C_M_ASYNC_ERROR, I2C_M_ASYNC_TX_COMPLETE, I2C_M_ASYNC_RX_COMPLETE };

/**
 * \brief Forward declaration of the descriptor type
 */
struct i2c_m_async_desc;

/**
 * \brief The I2C master callback function type for completion of RX or TX
 */
typedef void (*i2c_complete_cb_t)(struct i2c_m_async_desc *const i2c);

/**
 * \brief The I2C master callback function type for error
 */
typedef void (*i2c_error_cb_t)(struct i2c_m_async_desc *const i2c, int32_t error);

/** \brief I2C status
 *
 *  Status descriptor holds the current status of transfer.
 */
struct i2c_m_async_status {
	/** Status flags */
	uint16_t flags;
	/** The number of characters left in the message buffer*/
	int32_t left;
};

/**
 * \brief I2C master callback pointers structure
 */
struct i2c_m_async_callback {
	i2c_error_cb_t    error;
	i2c_complete_cb_t tx_complete;
	i2c_complete_cb_t rx_complete;
};

/**
 * \brief I2C descriptor structure, embed i2c_device & i2c_interface
 */
struct i2c_m_async_desc {
	struct _i2c_m_async_device  device;
	struct io_descriptor        io;
	struct i2c_m_async_callback i2c_cb;
	uint16_t                    slave_addr;
};

/**
 * \brief Initialize the asynchronous I2C master interface
 *
 * This function initializes the given I2C descriptor to be used as asynchronous
 * I2C master interface descriptor.
 * It checks if the given hardware is not initialized and if the given hardware
 * is permitted to be initialized.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through I2C
 * \param[in] hw The pointer to hardware instance
 *
 * \return Initialization status.
 */
int32_t i2c_m_async_init(struct i2c_m_async_desc *const i2c, void *const hw);

/**
 * \brief Deinitialize asynchronous I2C master interface
 *
 * This function deinitializes the given asynchronous I2C master descriptor.
 * It checks if the given hardware is initialized and if the given hardware is
 * permitted to be deinitialized.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 *
 * \return De-initialization status.
 * \retval -1 The passed parameters were invalid or the interface is already
 *            deinitialized
 * \retval 0 The de-initialization is completed successfully
 */
int32_t i2c_m_async_deinit(struct i2c_m_async_desc *const i2c);

/**
 * \brief Set the slave device address
 *
 * This function sets the next transfer target slave I2C device address.
 * It takes no effect to an already started access.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] addr The slave address to access
 * \param[in] addr_len The slave address length, can be I2C_M_TEN or I2C_M_SEVEN
 *
 * \return Masked slave address. The mask is maximum a 10-bit address, and the 10th
 *         bit set if 10-bit address is used
 */
int32_t i2c_m_async_set_slaveaddr(struct i2c_m_async_desc *const i2c, int16_t addr, int32_t addr_len);

/**
 * \brief Register callback function
 *
 * This function registers one callback function to the I2C master device specified
 * by the given descriptor
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] type Type of a callback to set
 * \param[in] func Callback function pointer
 *
 * \return Callback setting status
 * \retval -1 The passed parameters were invalid
 * \retval 0 The callback set is completed successfully
 */
int32_t i2c_m_async_register_callback(struct i2c_m_async_desc *const i2c, enum i2c_m_async_callback_type type,
                                      FUNC_PTR func);

/**
 * \brief Set baudrate
 *
 * This function sets the I2C master device to a specified baudrate.
 * It only takes effect when the hardware is disabled.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] clkrate Unused parameter, should always be 0
 * \param[in] baudrate The baudrate value set to master
 *
 * \return The status whether successfully set the baudrate
 * \retval -1 The passed parameters were invalid or the device is already enabled
 * \retval 0 The baudrate set is completed successfully
 */
int32_t i2c_m_async_set_baudrate(struct i2c_m_async_desc *const i2c, uint32_t clkrate, uint32_t baudrate);

/**
 * \brief Async version of enable hardware
 *
 * This function enables the I2C master device and then waits for this enabling
 * operation to be done.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 *
 * \return The status whether successfully enabled
 * \retval -1 The passed parameters were invalid or the device enable failed
 * \retval 0 The hardware enabling is completed successfully
 */
int32_t i2c_m_async_enable(struct i2c_m_async_desc *const i2c);

/**
 * \brief Async version of disable hardware
 *
 * This function disables the I2C master device and then waits for this disabling
 * operation to be done.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 *
 * \return The status whether successfully disabled
 * \retval -1 The passed parameters were invalid or the device disable failed
 * \retval 0 The hardware disabling is completed successfully
 */
int32_t i2c_m_async_disable(struct i2c_m_async_desc *const i2c);

/**
 * \brief Async version of the write command to I2C slave
 *
 * This function will write the value to a specified register in the I2C slave device,
 * and then return before the last sub-operation is done.
 *
 * The sequence of this routine is
 * sta->address(write)->ack->reg address->ack->resta->address(write)->ack->reg
 * value->nack->stt
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] reg The internal address/register of the I2C slave device
 * \param[in] value The value write to the I2C slave device
 *
 * \return The status whether successfully write to the device
 * \retval <0 The passed parameters were invalid or write fail
 * \retval 0 Writing to register is completed successfully
 */
int32_t i2c_m_async_cmd_write(struct i2c_m_async_desc *const i2c, uint8_t reg, uint8_t value);

/**
 * \brief Async version of read register value from the I2C slave
 *
 * This function will read a byte value from a specified reg in the I2C slave device
 * and then return before the last sub-operation is done.
 *
 * The sequence of this routine is
 * sta->address(write)->ack->reg address->ack->resta->address(read)->ack->reg
 * value->nack->stt
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] reg The internal address/register of the I2C slave device
 * \param[in] value The value read from the I2C slave device
 *
 * \return The status whether successfully read from the device
 * \retval <0 The passed parameters were invalid or read fail
 * \retval 0 Reading from register is completed successfully
 */
int32_t i2c_m_async_cmd_read(struct i2c_m_async_desc *const i2c, uint8_t reg, uint8_t *value);

/**
 * \brief Async version of transfer message to/from I2C slave
 *
 * This function will transfer a message between the I2C slave and the master.
 * This function will not wait for the transfer to complete.
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] msg  An i2c_m_msg struct
 *
 * \return The status of the operation
 * \retval 0 Operation completed successfully
 * \retval <0 Operation failed
 */
int32_t i2c_m_async_transfer(struct i2c_m_async_desc *const i2c, struct _i2c_m_msg *msg);

/**
 * \brief Generate stop condition on the I2C bus
 *
 * This function will generate a stop condition on the I2C bus
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 *
 * \return Operation status
 * \retval 0 Operation executed successfully
 * \retval <0 Operation failed
 */
int32_t i2c_m_async_send_stop(struct i2c_m_async_desc *const i2c);

/**
 * \brief Returns the status during the transfer
 *
 * \param[in] i2c An i2c descriptor which is used to communicate through I2C
 * \param[out] stat Pointer to the detailed status descriptor, set to NULL
 *
 * \return Status of transfer
 * \retval 0 No error detected
 * \retval <0 Error code
 */
int32_t i2c_m_async_get_status(struct i2c_m_async_desc *const i2c, struct i2c_m_async_status *stat);

/**
 * \brief Return I/O descriptor for this I2C instance
 *
 * This function will return an I/O instance for this I2C driver instance
 *
 * \param[in] i2c An I2C master descriptor, which is used to communicate through
 *                I2C
 * \param[in] io A pointer to an I/O descriptor pointer type
 *
 * \return Error code
 * \retval 0 No error detected
 * \retval <0 Error code
 */
int32_t i2c_m_async_get_io_descriptor(struct i2c_m_async_desc *const i2c, struct io_descriptor **io);

/**
 * \brief Retrieve the current driver version
 *
 * \return Current driver version.
 */
uint32_t i2c_m_get_version(void);

/**@}*/

#ifdef __cplusplus
}
#endif

#endif
