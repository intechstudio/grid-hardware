/**
 * \file
 *
 * \brief QSPI Driver
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

#include <utils_assert.h>
#include <hpl_qspi_sync.h>
#include <hpl_qspi_dma.h>
#include <hpl_qspi_config.h>

/**
 * \brief Memory copy function.
 *
 * \param dst  Pointer to destination buffer.
 * \param src  Pointer to source buffer.
 * \param count  Bytes to be copied.
 */
static void _qspi_memcpy(uint8_t *dst, uint8_t *src, uint32_t count)
{
	while (count--) {
		*dst++ = *src++;
	}
}

/**
 * \brief Ends ongoing transfer by releasing CS of QSPI peripheral.
 *
 * \param qspi  Pointer to an Qspi instance.
 */
static inline void _qspi_end_transfer(void *hw)
{
	hri_qspi_write_CTRLA_reg(hw, QSPI_CTRLA_ENABLE | QSPI_CTRLA_LASTXFER);
}

int32_t _qspi_sync_init(struct _qspi_sync_dev *dev, void *const hw)
{
	ASSERT(dev && hw);
	dev->prvt = hw;
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_SWRST);

	hri_qspi_write_CTRLB_reg(hw,
	                         QSPI_CTRLB_MODE_MEMORY | QSPI_CTRLB_CSMODE_LASTXFER | QSPI_CTRLB_DATALEN(0)
	                             | QSPI_CTRLB_DLYBCT(0) | QSPI_CTRLB_DLYCS(CONF_QSPI_DLYCS));

	hri_qspi_write_BAUD_reg(hw,
	                        CONF_QSPI_CPOL << QSPI_BAUD_CPOL_Pos | CONF_QSPI_CPHA << QSPI_BAUD_CPHA_Pos
	                            | QSPI_BAUD_BAUD(CONF_QSPI_BAUD_RATE) | QSPI_BAUD_DLYBS(CONF_QSPI_DLYBS));
	return ERR_NONE;
}

int32_t _qspi_sync_deinit(struct _qspi_sync_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_SWRST);
	return ERR_NONE;
}

int32_t _qspi_sync_enable(struct _qspi_sync_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_ENABLE);
	return ERR_NONE;
}

int32_t _qspi_sync_disable(struct _qspi_sync_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, 0);
	return ERR_NONE;
}

/**
 * \brief Set instruction frame param.
 */
static void _qspi_sync_command_set_ifr(struct _qspi_sync_dev *dev, const struct _qspi_command *cmd)
{
	void *hw = dev->prvt;
	if (cmd->inst_frame.bits.addr_en) {
		hri_qspi_write_INSTRADDR_reg(hw, cmd->address);
	}

	if (cmd->inst_frame.bits.inst_en) {
		hri_qspi_write_INSTRCTRL_INSTR_bf(hw, cmd->instruction);
	}

	if (cmd->inst_frame.bits.opt_en) {
		hri_qspi_write_INSTRCTRL_OPTCODE_bf(hw, cmd->option);
	}

	hri_qspi_write_INSTRFRAME_reg(hw, cmd->inst_frame.word);
}

/**
 * \brief Access QSPI mapping memory via AHB.
 */
static void _qspi_sync_run_transfer(struct _qspi_sync_dev *dev, const struct _qspi_command *cmd)
{
	void *   hw       = dev->prvt;
	uint8_t *qspi_mem = (uint8_t *)QSPI_AHB;
	if (cmd->inst_frame.bits.addr_en)
		qspi_mem += cmd->address;

	/* To synchronize system bus accesses */
	hri_qspi_read_INSTRFRAME_reg(hw);

	ASSERT(cmd->tx_buf || cmd->rx_buf);

	if (cmd->tx_buf) {
		_qspi_memcpy((uint8_t *)qspi_mem, (uint8_t *)cmd->tx_buf, cmd->buf_len);
	} else {
		_qspi_memcpy((uint8_t *)cmd->rx_buf, (uint8_t *)qspi_mem, cmd->buf_len);
	}

	__DSB();
	__ISB();
}

int32_t _qspi_sync_serial_run_command(struct _qspi_sync_dev *dev, const struct _qspi_command *cmd)
{
	_qspi_sync_command_set_ifr(dev, cmd);

	if (cmd->inst_frame.bits.data_en) {
		_qspi_sync_run_transfer(dev, cmd);
	}

	_qspi_end_transfer(dev->prvt);

	while (!hri_qspi_get_INTFLAG_INSTREND_bit(dev->prvt))
		;
	hri_qspi_clear_INTFLAG_INSTREND_bit(dev->prvt);
	return ERR_NONE;
}
/**
 *  \brief Callback for RX
 *  \param[in, out] dev Pointer to the DMA resource.
 */
static void _qspi_dma_rx_complete(struct _dma_resource *resource)
{
	struct _qspi_dma_dev *dev = (struct _qspi_dma_dev *)resource->back;

	_qspi_end_transfer(dev->prvt);

	if (dev->cb.xfer_done) {
		dev->cb.xfer_done(resource);
	}
}

/**
 *  \brief Callback for TX
 *  \param[in, out] dev Pointer to the DMA resource.
 */
static void _qspi_dma_tx_complete(struct _dma_resource *resource)
{
	struct _qspi_dma_dev *dev = (struct _qspi_dma_dev *)resource->back;

	_qspi_end_transfer(dev->prvt);

	if (dev->cb.xfer_done) {
		dev->cb.xfer_done(resource);
	}
}

/**
 *  \brief Callback for ERROR
 *  \param[in, out] dev Pointer to the DMA resource.
 */
static void _qspi_dma_error_occured(struct _dma_resource *resource)
{
	struct _qspi_dma_dev *dev = (struct _qspi_dma_dev *)resource->back;

	if (dev->cb.error) {
		dev->cb.error(resource);
	}
}

int32_t _qspi_dma_init(struct _qspi_dma_dev *dev, void *const hw)
{
	ASSERT(dev && hw);
	dev->prvt = hw;
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_SWRST);

	hri_qspi_write_CTRLB_reg(hw,
	                         QSPI_CTRLB_MODE_MEMORY | QSPI_CTRLB_CSMODE_LASTXFER | QSPI_CTRLB_DATALEN(0)
	                             | QSPI_CTRLB_DLYBCT(0) | QSPI_CTRLB_DLYCS(CONF_QSPI_DLYCS));

	hri_qspi_write_BAUD_reg(hw,
	                        CONF_QSPI_CPOL << QSPI_BAUD_CPOL_Pos | CONF_QSPI_CPHA << QSPI_BAUD_CPHA_Pos
	                            | QSPI_BAUD_BAUD(CONF_QSPI_BAUD_RATE) | QSPI_BAUD_DLYBS(CONF_QSPI_DLYBS));

	/* Initialize DMA rx channel */
	_dma_get_channel_resource(&dev->resource, CONF_QSPI_DMA_RX_CHANNEL);
	dev->resource->back                 = dev;
	dev->resource->dma_cb.transfer_done = _qspi_dma_rx_complete;
	dev->resource->dma_cb.error         = _qspi_dma_error_occured;
	/* Initialize DMA tx channel */
	_dma_get_channel_resource(&dev->resource, CONF_QSPI_DMA_TX_CHANNEL);
	dev->resource->back                 = dev;
	dev->resource->dma_cb.transfer_done = _qspi_dma_tx_complete;
	dev->resource->dma_cb.error         = _qspi_dma_error_occured;

	return ERR_NONE;
}

int32_t _qspi_dma_deinit(struct _qspi_dma_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_SWRST);
	return ERR_NONE;
}

int32_t _qspi_dma_enable(struct _qspi_dma_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, QSPI_CTRLA_ENABLE);
	return ERR_NONE;
}

int32_t _qspi_dma_disable(struct _qspi_dma_dev *dev)
{
	hri_qspi_write_CTRLA_reg(dev->prvt, 0);
	return ERR_NONE;
}

/**
 * \brief Set instruction frame param.
 */
static void _qspi_dma_command_set_ifr(struct _qspi_dma_dev *dev, const struct _qspi_command *cmd)
{
	void *hw = dev->prvt;

	if (cmd->inst_frame.bits.addr_en) {
		hri_qspi_write_INSTRADDR_reg(hw, cmd->address);
	}

	if (cmd->inst_frame.bits.inst_en) {
		hri_qspi_write_INSTRCTRL_INSTR_bf(hw, cmd->instruction);
	}

	if (cmd->inst_frame.bits.opt_en) {
		hri_qspi_write_INSTRCTRL_OPTCODE_bf(hw, cmd->option);
	}

	hri_qspi_write_INSTRFRAME_reg(hw, cmd->inst_frame.word);
}

/**
 * \brief Access QSPI mapping memory via AHB.
 */
static void _qspi_dma_run_transfer(struct _qspi_dma_dev *dev, const struct _qspi_command *cmd)
{
	void *   hw       = dev->prvt;
	uint8_t *qspi_mem = (uint8_t *)QSPI_AHB;

	if (cmd->inst_frame.bits.addr_en) {
		qspi_mem += cmd->address;
	}

	/* To synchronize system bus accesses */
	hri_qspi_read_INSTRFRAME_reg(hw);

	ASSERT(cmd->tx_buf || cmd->rx_buf);

	if (cmd->tx_buf) {
		_dma_set_source_address(CONF_QSPI_DMA_TX_CHANNEL, cmd->tx_buf);
		_dma_set_destination_address(CONF_QSPI_DMA_TX_CHANNEL, (uint8_t *)qspi_mem);
		_dma_set_data_amount(CONF_QSPI_DMA_TX_CHANNEL, cmd->buf_len);
		_dma_enable_transaction(CONF_QSPI_DMA_TX_CHANNEL, false);
	} else {
		_dma_set_source_address(CONF_QSPI_DMA_RX_CHANNEL, (uint8_t *)qspi_mem);
		_dma_set_destination_address(CONF_QSPI_DMA_RX_CHANNEL, cmd->rx_buf);
		_dma_set_data_amount(CONF_QSPI_DMA_RX_CHANNEL, cmd->buf_len);
		_dma_enable_transaction(CONF_QSPI_DMA_RX_CHANNEL, false);
		/* first read and then trig DMA */
		*(uint8_t *)(cmd->rx_buf) = qspi_mem[0];
	}

	__DSB();
	__ISB();
}

int32_t _qspi_dma_serial_run_command(struct _qspi_dma_dev *dev, const struct _qspi_command *cmd)
{
	_qspi_dma_command_set_ifr(dev, cmd);

	if (cmd->inst_frame.bits.data_en) {
		_qspi_dma_run_transfer(dev, cmd);
	}

	return ERR_NONE;
}

void _qspi_dma_register_callback(struct _qspi_dma_dev *dev, enum _qspi_dma_cb_type type, _qspi_dma_cb_t cb)
{
	switch (type) {
	case QSPI_DMA_CB_XFER_DONE:
		dev->cb.xfer_done = cb;
		_dma_set_irq_state(CONF_QSPI_DMA_TX_CHANNEL, DMA_TRANSFER_COMPLETE_CB, cb != NULL);
		_dma_set_irq_state(CONF_QSPI_DMA_RX_CHANNEL, DMA_TRANSFER_COMPLETE_CB, cb != NULL);
		break;
	case QSPI_DMA_CB_ERROR:
		dev->cb.error = cb;
		_dma_set_irq_state(CONF_QSPI_DMA_TX_CHANNEL, DMA_TRANSFER_ERROR_CB, cb != NULL);
		_dma_set_irq_state(CONF_QSPI_DMA_RX_CHANNEL, DMA_TRANSFER_ERROR_CB, cb != NULL);
		break;
	default:
		break;
	}
}
