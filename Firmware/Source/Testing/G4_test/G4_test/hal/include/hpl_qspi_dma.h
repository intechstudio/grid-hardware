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

#ifndef _HPL_QSPI_DMA_H_INCLUDED
#define _HPL_QSPI_DMA_H_INCLUDED

#include <hpl_qspi.h>
#include "hpl_irq.h"
#include "hpl_dma.h"

/**
 * \addtogroup hpl_qspi_dma HPL QSPI
 *
 *@{
 */

#ifdef __cplusplus
extern "C" {
#endif

/** The callback types */
enum _qspi_dma_cb_type {
	/** Callback type for DMA transfer done */
	QSPI_DMA_CB_XFER_DONE,
	/** Callback type for DMA errors */
	QSPI_DMA_CB_ERROR,
};

/**
 * \brief QSPI DMA callback type
 */
typedef void (*_qspi_dma_cb_t)(struct _dma_resource *resource);

/**
 *  \brief The callbacks offered by QSPI driver
 */
struct _qspi_dma_callbacks {
	_qspi_dma_cb_t xfer_done;
	_qspi_dma_cb_t error;
};

/**
 * QSPI dma driver instance.
 */
struct _qspi_dma_dev {
	/** Pointer to private data or hardware base */
	void *prvt;
	/**
	 *  Pointer to the callback functions so that initialize the driver to
	 *  handle interrupts.
	 */
	struct _qspi_dma_callbacks cb;
	/** DMA resource */
	struct _dma_resource *resource;
};

/**
 *  \brief Initialize QSPI for access without interrupts
 *  It will load default hardware configuration and software struct.
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \param[in] hw Pointer to the hardware base.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_dma_init(struct _qspi_dma_dev *dev, void *const hw);

/**
 *  \brief Deinitialize QSPI
 *  Disable, reset the hardware and the software struct.
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_dma_deinit(struct _qspi_dma_dev *dev);

/**
 *  \brief Enable QSPI for access without interrupts
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_dma_enable(struct _qspi_dma_dev *dev);

/**
 *  \brief Disable QSPI for access without interrupts
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_dma_disable(struct _qspi_dma_dev *dev);

/**
 * \brief Execute command in Serial Memory Mode.
 *
 * \param[in] dev The pointer to QSPI device instance
 * \param[in] cmd The pointer to the command information
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_dma_serial_run_command(struct _qspi_dma_dev *dev, const struct _qspi_command *cmd);

/**
 *  \brief Register the QSPI device callback
 *  \param[in] dev Pointer to the SPI device instance.
 *  \param[in] type The callback type.
 *  \param[in] cb The callback function to register. NULL to disable callback.
 *  \return Always 0.
 */
void _qspi_dma_register_callback(struct _qspi_dma_dev *dev, const enum _qspi_dma_cb_type type, _qspi_dma_cb_t cb);

#ifdef __cplusplus
}
#endif

/**@}*/
#endif /* ifndef _HPL_QSPI_DMA_H_INCLUDED */
