/* Auto-generated config file hpl_qspi_config.h */
#ifndef HPL_QSPI_CONFIG_H
#define HPL_QSPI_CONFIG_H

// <<< Use Configuration Wizard in Context Menu >>>

#include <peripheral_clk_config.h>

// <h> Basic settings

#ifndef CONF_CONF_QSPI_ENABLE
#define CONF_CONF_QSPI_ENABLE 1
#endif

// <o> Baud rate <1-150000000>
// <i> The SPI data transfer rate. Note: (fqspi_clock / baudrate) < 255
// <id> qspi_baud_rate
#ifndef CONF_QSPI_BAUD
#define CONF_QSPI_BAUD 375000
#endif

// <o> Clock Polarity
// <0x0=>The inactive state value of SPCK is logic level zero.
// <0x1=>The inactive state value of SPCK is logic level one.
// <i> Determines the inactive state value of the serial clock (SPCK).
// <id> qspi_cpol
#ifndef CONF_QSPI_CPOL
#define CONF_QSPI_CPOL 0x0
#endif

// <o> Clock Phase
// <0x0=>Data is changed on the leading edge of SPCK and captured on the following edge of SPCK.
// <0x1=>Data is captured on the leading edge of SPCK and changed on the following edge of SPCK.
// <i> Determines which edge of SPCK causes data to change and which edge causes data to be captured.
// <id> qspi_cpha
#ifndef CONF_QSPI_CPHA
#define CONF_QSPI_CPHA 0x0
#endif

//<o> QSPI DMA TX Channel <0-32>
//<i> This defines DMA channel to be used
//<id> qspi_dma_tx_channel
#ifndef CONF_QSPI_DMA_TX_CHANNEL
#define CONF_QSPI_DMA_TX_CHANNEL 0
#endif

//<o> QSPI DMA RX  Channel <0-32>
//<i> This defines DMA channel to be used
//<id> qspi_dma_rx_channel
#ifndef CONF_QSPI_DMA_RX_CHANNEL
#define CONF_QSPI_DMA_RX_CHANNEL 1
#endif

// </h>

// <e> Advanced Configuration
// <id> qspi_advanced
#ifndef CONF_QSPI_ADVANCED
#define CONF_QSPI_ADVANCED 0
#endif

// <o> Delay Before QSCK (ns) <0-255000>
// <i> This field defines the delay from QCS falling edge (activation) to the first valid QSCK transition (in ns).
// <id> qspi_dlybs
#ifndef CONF_QSPI_DLY_BS
#define CONF_QSPI_DLY_BS 0
#endif

// <o> Minimum Inactive QCS Delay (ns) <0-8160000>
// <i> This field defines the minimum delay between the deactivation and the activation of QCS (in ns).
// <id> qspi_dlycs
#ifndef CONF_QSPI_DLY_CS
#define CONF_QSPI_DLY_CS 0
#endif

// </e>

/* Calculate baud register value from requested baudrate value */
#ifndef CONF_QSPI_BAUD_RATE
#define CONF_QSPI_BAUD_RATE ((CONF_CPU_FREQUENCY / CONF_QSPI_BAUD) - 1)
#if CONF_QSPI_BAUD > CONF_CPU_FREQUENCY || CONF_QSPI_BAUD_RATE > 255
#warning Invalid baudrate, please check.
#endif
#endif

/* Calculates the value of the CSR DLYCS field given the desired delay (in ns) */
#ifndef CONF_QSPI_DLYCS
#define CONF_QSPI_DLYCS (((CONF_CPU_FREQUENCY / 1000000) * CONF_QSPI_DLY_CS) / 1000)
#endif

/* Calculates the value of the CSR DLYBS field given the desired delay (in ns) */
#ifndef CONF_QSPI_DLYBS
#define CONF_QSPI_DLYBS (((CONF_CPU_FREQUENCY / 1000000) * CONF_QSPI_DLY_BS) / 1000)
#endif

// <<< end of configuration section >>>

#endif // HPL_QSPI_CONFIG_H
