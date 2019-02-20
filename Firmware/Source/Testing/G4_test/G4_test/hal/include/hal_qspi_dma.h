/**
 * \file
 *
 * \brief Quad SPI dma related functionality declaration.
 *
 * Copyright (c) 2016-2018 Microchip Technology Inc. and its subsidiaries.
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

#ifndef _HAL_QSPI_DMA_INCLUDED
#define _HAL_QSPI_DMA_INCLUDED

#include <hpl_qspi_dma.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \addtogroup doc_driver_hal_quad_spi_dma
 *
 *@{
 */

/**
 * \brief QSPI descriptor structure
 */
struct qspi_dma_descriptor {
	/** Pointer to QSPI device instance */
	struct _qspi_dma_dev dev;
};

/**
 *  \brief Initialize QSPI low level driver.
 *
 *  \param[in] qspi Pointer to the QSPI device instance
 *  \param[in] hw Pointer to the hardware base
 *
 *  \return Operation status.
 *  \retval ERR_NONE Success
 */
int32_t qspi_dma_init(struct qspi_dma_descriptor *qspi, void *hw);

/**
 *  \brief Deinitialize QSPI low level driver.
 *
 *  \param[in] qspi Pointer to the QSPI device instance
 *
 *  \return Operation status.
 *  \retval ERR_NONE Success
 */
int32_t qspi_dma_deinit(struct qspi_dma_descriptor *qspi);

/**
 *  \brief Enable QSPI for access without interrupts
 *
 *  \param[in] qspi Pointer to the QSPI device instance.
 *
 *  \return Operation status.
 *  \retval ERR_NONE Success
 */
int32_t qspi_dma_enable(struct qspi_dma_descriptor *qspi);

/**
 *  \brief Disable QSPI for access without interrupts
 *
 *  Disable QSPI. Deactivate all CS pins if it works as master.
 *
 *  \param[in] qspi Pointer to the QSPI device instance.
 *
 *  \return Operation status.
 *  \retval ERR_NONE Success
 */
int32_t qspi_dma_disable(struct qspi_dma_descriptor *qspi);

/** \brief Execute command in Serial Memory Mode.
 *
 *  \param[in] qspi Pointer to the HAL QSPI instance
 *  \param[in] cmd Pointer to the command structure
 *
 *  \return Operation status.
 *  \retval ERR_NONE Success
 */
int32_t qspi_dma_serial_run_command(struct qspi_dma_descriptor *qspi, const struct _qspi_command *cmd);

/** \brief Register a function as QSPI transfer completion callback
 *
 *  Register callback function specified by its \c type.
 *  - QSPI_DMA_CB_XFER_DONE: set the function that will be called on QSPI transfer
 *    completion including deactivate the CS.
 *  - QSPI_DMA_CB_ERROR: set the function that will be called on QSPI transfer error.
 *  Register NULL function to not use the callback.
 *
 *  \param[in] qspi Pointer to the HAL QSPI instance
 *  \param[in] type Callback type (\ref _qspi_dma_cb_type)
 *  \param[in] cb Pointer to callback function
 */
void qspi_dma_register_callback(struct qspi_dma_descriptor *qspi, const enum _qspi_dma_cb_type type, _qspi_dma_cb_t cb);

/**
 *  \brief Retrieve the current driver version
 *
 *  \return Current driver version.
 */
uint32_t qspi_dma_get_version(void);

/**@}*/

#ifdef __cplusplus
}
#endif

#endif /* _HAL_QSPI_DMA_INCLUDED */
