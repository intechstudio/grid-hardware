EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 11
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L suku_basics:74HC165 U?
U 1 1 5DC5FDC3
P 4100 3400
AR Path="/5DC5FDC3" Ref="U?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDC3" Ref="U3"  Part="1" 
F 0 "U3" H 3700 4300 50  0000 C CNN
F 1 "74HC165" H 3800 4200 50  0000 C CNN
F 2 "suku_basics:SOIC-16_74HC165" H 4100 3400 50  0001 C CNN
F 3 "" H 4100 3400 50  0001 C CNN
	1    4100 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 3900 3400 3900
Wire Wire Line
	3600 4000 3500 4000
Wire Wire Line
	3600 4100 3400 4100
Wire Wire Line
	3500 4000 3500 4400
Wire Wire Line
	3500 4400 4100 4400
Wire Wire Line
	4100 4400 4100 4300
Wire Wire Line
	4600 2800 4800 2800
Wire Wire Line
	3600 2800 3500 2800
Wire Wire Line
	3500 2800 3500 4000
Connection ~ 3500 4000
$Comp
L power:GND #PWR?
U 1 1 5DC5FDD6
P 4100 4500
AR Path="/5DC5FDD6" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDD6" Ref="#PWR0155"  Part="1" 
F 0 "#PWR0155" H 4100 4250 50  0001 C CNN
F 1 "GND" H 4105 4327 50  0000 C CNN
F 2 "" H 4100 4500 50  0001 C CNN
F 3 "" H 4100 4500 50  0001 C CNN
	1    4100 4500
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:CAP C?
U 1 1 5DC5FDDC
P 4800 3700
AR Path="/5DC5FDDC" Ref="C?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDDC" Ref="C33"  Part="1" 
F 0 "C33" H 4892 3746 50  0000 L CNN
F 1 "100n" H 4892 3655 50  0000 L CNN
F 2 "suku_basics:CAP_0805" H 4800 3700 50  0001 C CNN
F 3 "~" H 4800 3700 50  0001 C CNN
	1    4800 3700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5DC5FDE2
P 4800 4000
AR Path="/5DC5FDE2" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDE2" Ref="#PWR0154"  Part="1" 
F 0 "#PWR0154" H 4800 3750 50  0001 C CNN
F 1 "GND" H 4805 3827 50  0000 C CNN
F 2 "" H 4800 4000 50  0001 C CNN
F 3 "" H 4800 4000 50  0001 C CNN
	1    4800 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 2500 4100 2600
Wire Wire Line
	4800 3800 4800 3900
Wire Wire Line
	4800 3400 4800 3500
$Comp
L suku_basics:+3V3_UC #PWR?
U 1 1 5DC5FDEB
P 4800 3400
AR Path="/5DC5FDEB" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDEB" Ref="#PWR0153"  Part="1" 
F 0 "#PWR0153" H 4800 3250 50  0001 C CNN
F 1 "+3V3_UC" H 4815 3573 50  0000 C CNN
F 2 "" H 4800 3400 50  0001 C CNN
F 3 "" H 4800 3400 50  0001 C CNN
	1    4800 3400
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:+3V3_UC #PWR?
U 1 1 5DC5FDF1
P 4100 2500
AR Path="/5DC5FDF1" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/5DC5FDF1" Ref="#PWR0151"  Part="1" 
F 0 "#PWR0151" H 4100 2350 50  0001 C CNN
F 1 "+3V3_UC" H 4115 2673 50  0000 C CNN
F 2 "" H 4100 2500 50  0001 C CNN
F 3 "" H 4100 2500 50  0001 C CNN
	1    4100 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 4500 4100 4400
Connection ~ 4100 4400
Wire Wire Line
	4800 3500 5100 3500
Connection ~ 4800 3500
Wire Wire Line
	4800 3500 4800 3600
Wire Wire Line
	4800 3900 5100 3900
Connection ~ 4800 3900
Wire Wire Line
	4800 3900 4800 4000
Text Label 5100 3500 0    50   ~ 0
HWCFG_HIGH
Text Label 5100 3900 0    50   ~ 0
HWCFG_LOW
Wire Wire Line
	3600 3500 3100 3500
Wire Wire Line
	3600 3400 3100 3400
Wire Wire Line
	3600 3200 3100 3200
Wire Wire Line
	3600 3100 3100 3100
Wire Wire Line
	3600 3000 3100 3000
Text Label 3100 3400 2    50   ~ 0
HWCFG_LOW
Text Label 3100 3500 2    50   ~ 0
HWCFG_LOW
Text Label 3100 3200 2    50   ~ 0
HWCFG_LOW
Text Label 3100 2900 2    50   ~ 0
HWCFG_LOW
Text Notes 6100 5100 0    50   ~ 0
Board Identification\n\nGrid firmware can identify the hardware and the board \nrevision thorugh a 3 wire serial interface using one \nor more shift register as read only memory. The content\nof the memory is defined by pulling the inputs high or\nlow through pcb traces or solderable configuration jumpers.\n\n4b'Model + 4b'Revision + nb'Reserved (Multiple shift registers)\n\nD0: MODEL (LSB)\nD1: MODEL\nD2: MODEL\nD3: MODEL (MSB)\nD4: REVISION (LSB)\nD5: REVISION\nD6: REVISION\nD7: REVISION (MSB)\n\n\n\nModel Codes (D3-D0):\n\nPo16 0000\nBo16 0001\nPBF4 0010\nEN16 0011\n...\n\nRevision Codes (D7-D4):\n\nRevA 0000\nRevB 0001\nRevC 0010\nRevD 0011\n...\n
Text HLabel 4800 2800 2    50   Output ~ 0
HWCFG_DATA
Text HLabel 3400 3900 0    50   Input ~ 0
HWCFG_CLOCK
Text HLabel 3400 4100 0    50   Input ~ 0
HWCFG_SHIFT
NoConn ~ 4600 2900
Wire Wire Line
	3100 2900 3600 2900
Text Label 3100 3100 2    50   ~ 0
HWCFG_HIGH
$Comp
L suku_basics:RES R?
U 1 1 60507332
P 1500 4500
AR Path="/5D757C78/60507332" Ref="R?"  Part="1" 
AR Path="/5DC2DC06/60507332" Ref="R112"  Part="1" 
F 0 "R112" H 1559 4546 50  0000 L CNN
F 1 "10k" H 1559 4455 50  0000 L CNN
F 2 "suku_basics:RES_0805" H 1500 4500 50  0001 C CNN
F 3 "~" H 1500 4500 50  0001 C CNN
	1    1500 4500
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 60507338
P 1500 5100
AR Path="/60507338" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/60507338" Ref="#PWR0348"  Part="1" 
F 0 "#PWR0348" H 1500 4850 50  0001 C CNN
F 1 "GND" H 1505 4927 50  0000 C CNN
F 2 "" H 1500 5100 50  0001 C CNN
F 3 "" H 1500 5100 50  0001 C CNN
	1    1500 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 5100 1500 5000
$Comp
L suku_basics:JP_SolderJumper_2_Open JP2
U 1 1 60507340
P 1500 4900
F 0 "JP2" V 1454 4968 50  0000 L CNN
F 1 "(NF)" V 1545 4968 50  0000 L CNN
F 2 "Jumper:SolderJumper-2_P1.3mm_Open_TrianglePad1.0x1.5mm" H 1500 4900 50  0001 C CNN
F 3 "~" H 1500 4900 50  0001 C CNN
	1    1500 4900
	0    1    1    0   
$EndComp
$Comp
L suku_basics:+3V3_UC #PWR?
U 1 1 60507348
P 1500 4300
AR Path="/60507348" Ref="#PWR?"  Part="1" 
AR Path="/5DC2DC06/60507348" Ref="#PWR0349"  Part="1" 
F 0 "#PWR0349" H 1500 4150 50  0001 C CNN
F 1 "+3V3_UC" H 1515 4473 50  0000 C CNN
F 2 "" H 1500 4300 50  0001 C CNN
F 3 "" H 1500 4300 50  0001 C CNN
	1    1500 4300
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 4300 1500 4400
Wire Wire Line
	1500 4600 1500 4700
Wire Wire Line
	1500 4700 2200 4700
Wire Wire Line
	2200 4700 2200 3600
Connection ~ 1500 4700
Wire Wire Line
	1500 4700 1500 4800
Wire Wire Line
	2200 3600 3600 3600
Text Notes 1600 5100 0    50   ~ 0
OPEN IF FUSB IC IS FITTED
Text Label 3100 3000 2    50   ~ 0
HWCFG_LOW
Text Label 3100 3300 2    50   ~ 0
HWCFG_LOW
Wire Wire Line
	3100 3300 3600 3300
$EndSCHEMATC
