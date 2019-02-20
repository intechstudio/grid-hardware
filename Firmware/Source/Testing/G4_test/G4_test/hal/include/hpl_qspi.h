/**
 * \file
 *
 * \brief Quad SPI related functionality declaration.
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

#ifndef _HPL_QSPI_H_INCLUDED
#define _HPL_QSPI_H_INCLUDED

#include "compiler.h"

/**
 * \addtogroup hpl_qspi HPL QSPI
 *
 *@{
 */

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \brief Qspi access modes
 */
enum qspi_access {
	/* Read access */
	QSPI_READ_ACCESS = 0,
	/* Read memory access */
	QSPI_READMEM_ACCESS,
	/* Write access */
	QSPI_WRITE_ACCESS,
	/* Write memory access */
	QSPI_WRITEMEM_ACCESS
};

/**
 * \brief QSPI command instruction/address/data width
 */
enum qspi_cmd_width {
	/** Instruction: Single-bit, Address: Single-bit, Data: Single-bit */
	QSPI_INST1_ADDR1_DATA1,
	/** Instruction: Single-bit, Address: Single-bit, Data: Dual-bit */
	QSPI_INST1_ADDR1_DATA2,
	/** Instruction: Single-bit, Address: Single-bit, Data: Quad-bit */
	QSPI_INST1_ADDR1_DATA4,
	/** Instruction: Single-bit, Address: Dual-bit, Data: Dual-bit */
	QSPI_INST1_ADDR2_DATA2,
	/** Instruction: Single-bit, Address: Quad-bit, Data: Quad-bit */
	QSPI_INST1_ADDR4_DATA4,
	/** Instruction: Dual-bit, Address: Dual-bit, Data: Dual-bit */
	QSPI_INST2_ADDR2_DATA2,
	/** Instruction: Quad-bit, Address: Quad-bit, Data: Quad-bit */
	QSPI_INST4_ADDR4_DATA4
};

/**
 * \brief QSPI command option code length in bits
 */
enum qspi_cmd_opt_len {
	/** The option code is 1 bit long */
	QSPI_OPT_1BIT,
	/** The option code is 2 bits long */
	QSPI_OPT_2BIT,
	/** The option code is 4 bits long */
	QSPI_OPT_4BIT,
	/** The option code is 8 bits long */
	QSPI_OPT_8BIT
};

/**
 * \brief Qspi command structure
 */
struct _qspi_command {
	union {
		struct {
			/* Width of QSPI Addr , inst data */
			uint32_t width : 3;
			/* Reserved */
			uint32_t reserved0 : 1;
			/* Enable Instruction */
			uint32_t inst_en : 1;
			/* Enable Address */
			uint32_t addr_en : 1;
			/* Enable Option */
			uint32_t opt_en : 1;
			/* Enable Data */
			uint32_t data_en : 1;
			/* Option Length */
			uint32_t opt_len : 2;
			/* Address Length */
			uint32_t addr_len : 1;
			/* Option Length */
			uint32_t reserved1 : 1;
			/* Transfer type */
			uint32_t tfr_type : 2;
			/* Continuous read mode */
			uint32_t continues_read : 1;
			/* Enable Double Data Rate */
			uint32_t ddr_enable : 1;
			/* Dummy Cycles Length */
			uint32_t dummy_cycles : 5;
			/* Reserved */
			uint32_t reserved3 : 11;
		} bits;
		uint32_t word;
	} inst_frame;

	uint8_t  instruction;
	uint8_t  option;
	uint32_t address;

	size_t      buf_len;
	const void *tx_buf;
	void *      rx_buf;
};

#ifdef __cplusplus
}
#endif

/**@}*/
#endif /* ifndef _HPL_QSPI_H_INCLUDED */
