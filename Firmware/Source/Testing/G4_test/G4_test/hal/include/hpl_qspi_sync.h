/**
 * \file
 *
 * \brief Quad SPI Sync related functionality declaration.
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

#ifndef _HPL_QSPI_SYNC_H_INCLUDED
#define _HPL_QSPI_SYNC_H_INCLUDED

#include <hpl_qspi.h>

/**
 * \addtogroup hpl_qspi HPL QSPI
 *
 *@{
 */

#ifdef __cplusplus
extern "C" {
#endif

/** Quad SPI polling driver instance. */
struct _qspi_sync_dev {
	/** Pointer to private data or hardware base */
	void *prvt;
};

/**
 *  \brief Initialize QSPI for access without interrupts
 *  It will load default hardware configuration and software struct.
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \param[in] hw Pointer to the hardware base.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_sync_init(struct _qspi_sync_dev *dev, void *const hw);

/**
 *  \brief Deinitialize QSPI
 *  Disable, reset the hardware and the software struct.
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_sync_deinit(struct _qspi_sync_dev *dev);

/**
 *  \brief Enable QSPI for access without interrupts
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_sync_enable(struct _qspi_sync_dev *dev);

/**
 *  \brief Disable QSPI for access without interrupts
 *  \param[in, out] dev Pointer to the QSPI device instance.
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_sync_disable(struct _qspi_sync_dev *dev);

/**
 * \brief Execute command in Serial Memory Mode.
 *
 * \param[in] dev The pointer to QSPI device instance
 * \param[in] cmd The pointer to the command information
 *  \return Operation status.
 *  \retval ERR_NONE Operation done successfully.
 */
int32_t _qspi_sync_serial_run_command(struct _qspi_sync_dev *dev, const struct _qspi_command *cmd);

#ifdef __cplusplus
}
#endif

/**@}*/
#endif /* ifndef _HPL_QSPI_SYNC_H_INCLUDED */
