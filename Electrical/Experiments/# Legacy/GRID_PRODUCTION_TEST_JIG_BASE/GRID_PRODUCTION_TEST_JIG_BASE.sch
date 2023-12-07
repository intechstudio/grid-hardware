EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
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
L Connector_Generic:Conn_01x08 M1
U 1 1 604C3D73
P 4200 3100
F 0 "M1" H 4280 3092 50  0000 L CNN
F 1 "Conn_01x08" H 4280 3001 50  0000 L CNN
F 2 "suku_basics:grid_outline" H 4200 3100 50  0001 C CNN
F 3 "~" H 4200 3100 50  0001 C CNN
	1    4200 3100
	1    0    0    -1  
$EndComp
$Comp
L Connector:TestPoint_Alt TP1
U 1 1 604C479E
P 2700 1200
F 0 "TP1" V 2895 1272 50  0000 C CNN
F 1 "+3V3_UC" V 2804 1272 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 2900 1200 50  0001 C CNN
F 3 "~" H 2900 1200 50  0001 C CNN
	1    2700 1200
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP2
U 1 1 604C5B02
P 2700 1500
F 0 "TP2" V 2895 1572 50  0000 C CNN
F 1 "GND" V 2804 1572 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 2900 1500 50  0001 C CNN
F 3 "~" H 2900 1500 50  0001 C CNN
	1    2700 1500
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP3
U 1 1 604C5D68
P 2700 1800
F 0 "TP3" V 2895 1872 50  0000 C CNN
F 1 "GND" V 2804 1872 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 2900 1800 50  0001 C CNN
F 3 "~" H 2900 1800 50  0001 C CNN
	1    2700 1800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP4
U 1 1 604C5EDE
P 2700 2100
F 0 "TP4" V 2895 2172 50  0000 C CNN
F 1 "N.C." V 2804 2172 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 2900 2100 50  0001 C CNN
F 3 "~" H 2900 2100 50  0001 C CNN
	1    2700 2100
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP5
U 1 1 604C62EA
P 2700 2400
F 0 "TP5" V 2895 2472 50  0000 C CNN
F 1 "GND" V 2804 2472 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 2900 2400 50  0001 C CNN
F 3 "~" H 2900 2400 50  0001 C CNN
	1    2700 2400
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP10
U 1 1 604C6564
P 3800 2400
F 0 "TP10" V 3846 2588 50  0000 L CNN
F 1 "RESET" V 3755 2588 50  0000 L CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 4000 2400 50  0001 C CNN
F 3 "~" H 4000 2400 50  0001 C CNN
	1    3800 2400
	0    1    -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP9
U 1 1 604C6945
P 3800 2100
F 0 "TP9" V 3846 2288 50  0000 L CNN
F 1 "N.C." V 3755 2288 50  0000 L CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 4000 2100 50  0001 C CNN
F 3 "~" H 4000 2100 50  0001 C CNN
	1    3800 2100
	0    1    -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP8
U 1 1 604C7092
P 3800 1800
F 0 "TP8" V 3846 1988 50  0000 L CNN
F 1 "SYS_SWO" V 3755 1988 50  0000 L CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 4000 1800 50  0001 C CNN
F 3 "~" H 4000 1800 50  0001 C CNN
	1    3800 1800
	0    1    -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP7
U 1 1 604C74C3
P 3800 1500
F 0 "TP7" V 3846 1688 50  0000 L CNN
F 1 "SYS_SWCLK" V 3755 1688 50  0000 L CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 4000 1500 50  0001 C CNN
F 3 "~" H 4000 1500 50  0001 C CNN
	1    3800 1500
	0    1    -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP6
U 1 1 604C7756
P 3800 1200
F 0 "TP6" V 3846 1388 50  0000 L CNN
F 1 "SYS_SWDIO" V 3755 1388 50  0000 L CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 4000 1200 50  0001 C CNN
F 3 "~" H 4000 1200 50  0001 C CNN
	1    3800 1200
	0    1    -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP11
U 1 1 604CD45E
P 6100 1100
F 0 "TP11" V 6295 1172 50  0000 C CNN
F 1 "GND" V 6204 1172 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 6300 1100 50  0001 C CNN
F 3 "~" H 6300 1100 50  0001 C CNN
	1    6100 1100
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP12
U 1 1 604CD876
P 6100 1400
F 0 "TP12" V 6295 1472 50  0000 C CNN
F 1 "VB" V 6204 1472 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 6300 1400 50  0001 C CNN
F 3 "~" H 6300 1400 50  0001 C CNN
	1    6100 1400
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP13
U 1 1 604CDE42
P 6100 1700
F 0 "TP13" V 6295 1772 50  0000 C CNN
F 1 "D-" V 6204 1772 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 6300 1700 50  0001 C CNN
F 3 "~" H 6300 1700 50  0001 C CNN
	1    6100 1700
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP14
U 1 1 604CE1A9
P 6100 2000
F 0 "TP14" V 6295 2072 50  0000 C CNN
F 1 "D+" V 6204 2072 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 6300 2000 50  0001 C CNN
F 3 "~" H 6300 2000 50  0001 C CNN
	1    6100 2000
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP15
U 1 1 604CE66D
P 7400 2200
F 0 "TP15" V 7595 2272 50  0000 C CNN
F 1 "UC" V 7504 2272 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 7600 2200 50  0001 C CNN
F 3 "~" H 7600 2200 50  0001 C CNN
	1    7400 2200
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP16
U 1 1 604CE946
P 7400 2500
F 0 "TP16" V 7595 2572 50  0000 C CNN
F 1 "UI" V 7504 2572 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 7600 2500 50  0001 C CNN
F 3 "~" H 7600 2500 50  0001 C CNN
	1    7400 2500
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP17
U 1 1 604CEB39
P 7400 2800
F 0 "TP17" V 7595 2872 50  0000 C CNN
F 1 "UI_5V" V 7504 2872 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 7600 2800 50  0001 C CNN
F 3 "~" H 7600 2800 50  0001 C CNN
	1    7400 2800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP18
U 1 1 604D31B5
P 8700 1600
F 0 "TP18" V 8895 1672 50  0000 C CNN
F 1 "GND" V 8804 1672 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 8900 1600 50  0001 C CNN
F 3 "~" H 8900 1600 50  0001 C CNN
	1    8700 1600
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP19
U 1 1 604D31BB
P 8700 1900
F 0 "TP19" V 8895 1972 50  0000 C CNN
F 1 "TX" V 8804 1972 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 8900 1900 50  0001 C CNN
F 3 "~" H 8900 1900 50  0001 C CNN
	1    8700 1900
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP20
U 1 1 604D31C1
P 8700 2200
F 0 "TP20" V 8895 2272 50  0000 C CNN
F 1 "RX" V 8804 2272 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 8900 2200 50  0001 C CNN
F 3 "~" H 8900 2200 50  0001 C CNN
	1    8700 2200
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP21
U 1 1 604D9A67
P 1600 2800
F 0 "TP21" V 1795 2872 50  0000 C CNN
F 1 "W_SYNC_1" V 1704 2872 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 2800 50  0001 C CNN
F 3 "~" H 1800 2800 50  0001 C CNN
	1    1600 2800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP22
U 1 1 604D9A6D
P 1600 3100
F 0 "TP22" V 1795 3172 50  0000 C CNN
F 1 "W_TX" V 1704 3172 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 3100 50  0001 C CNN
F 3 "~" H 1800 3100 50  0001 C CNN
	1    1600 3100
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP23
U 1 1 604DA335
P 1600 3400
F 0 "TP23" V 1795 3472 50  0000 C CNN
F 1 "W_RX" V 1704 3472 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 3400 50  0001 C CNN
F 3 "~" H 1800 3400 50  0001 C CNN
	1    1600 3400
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP24
U 1 1 604DA33B
P 1600 3700
F 0 "TP24" V 1795 3772 50  0000 C CNN
F 1 "W_SYNC_2" V 1704 3772 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 3700 50  0001 C CNN
F 3 "~" H 1800 3700 50  0001 C CNN
	1    1600 3700
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP25
U 1 1 604E7ED1
P 1600 4500
F 0 "TP25" V 1795 4572 50  0000 C CNN
F 1 "S_SYNC_1" V 1704 4572 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 4500 50  0001 C CNN
F 3 "~" H 1800 4500 50  0001 C CNN
	1    1600 4500
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP26
U 1 1 604E7ED7
P 1600 4800
F 0 "TP26" V 1795 4872 50  0000 C CNN
F 1 "S_TX" V 1704 4872 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 4800 50  0001 C CNN
F 3 "~" H 1800 4800 50  0001 C CNN
	1    1600 4800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP27
U 1 1 604E7EDD
P 1600 5100
F 0 "TP27" V 1795 5172 50  0000 C CNN
F 1 "S_RX" V 1704 5172 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 5100 50  0001 C CNN
F 3 "~" H 1800 5100 50  0001 C CNN
	1    1600 5100
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP28
U 1 1 604E7EE3
P 1600 5400
F 0 "TP28" V 1795 5472 50  0000 C CNN
F 1 "S_SYNC_2" V 1704 5472 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 5400 50  0001 C CNN
F 3 "~" H 1800 5400 50  0001 C CNN
	1    1600 5400
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP29
U 1 1 604E8F77
P 1600 5900
F 0 "TP29" V 1795 5972 50  0000 C CNN
F 1 "E_SYNC_1" V 1704 5972 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 5900 50  0001 C CNN
F 3 "~" H 1800 5900 50  0001 C CNN
	1    1600 5900
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP30
U 1 1 604E8F7D
P 1600 6200
F 0 "TP30" V 1795 6272 50  0000 C CNN
F 1 "E_TX" V 1704 6272 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 6200 50  0001 C CNN
F 3 "~" H 1800 6200 50  0001 C CNN
	1    1600 6200
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP31
U 1 1 604E8F83
P 1600 6500
F 0 "TP31" V 1795 6572 50  0000 C CNN
F 1 "E_RX" V 1704 6572 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 6500 50  0001 C CNN
F 3 "~" H 1800 6500 50  0001 C CNN
	1    1600 6500
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP32
U 1 1 604E8F89
P 1600 6800
F 0 "TP32" V 1795 6872 50  0000 C CNN
F 1 "E_SYNC_2" V 1704 6872 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 6800 50  0001 C CNN
F 3 "~" H 1800 6800 50  0001 C CNN
	1    1600 6800
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP33
U 1 1 604EA0E1
P 1600 7300
F 0 "TP33" V 1795 7372 50  0000 C CNN
F 1 "N_SYNC_1" V 1704 7372 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 7300 50  0001 C CNN
F 3 "~" H 1800 7300 50  0001 C CNN
	1    1600 7300
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP34
U 1 1 604EA0E7
P 1600 7600
F 0 "TP34" V 1795 7672 50  0000 C CNN
F 1 "N_TX" V 1704 7672 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 7600 50  0001 C CNN
F 3 "~" H 1800 7600 50  0001 C CNN
	1    1600 7600
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP35
U 1 1 604EA0ED
P 1600 7900
F 0 "TP35" V 1795 7972 50  0000 C CNN
F 1 "N_RX" V 1704 7972 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 7900 50  0001 C CNN
F 3 "~" H 1800 7900 50  0001 C CNN
	1    1600 7900
	0    -1   -1   0   
$EndComp
$Comp
L Connector:TestPoint_Alt TP36
U 1 1 604EA0F3
P 1600 8200
F 0 "TP36" V 1795 8272 50  0000 C CNN
F 1 "N_SYNC_2" V 1704 8272 50  0000 C CNN
F 2 "suku_basics:testpoint_pogo_0.75mm" H 1800 8200 50  0001 C CNN
F 3 "~" H 1800 8200 50  0001 C CNN
	1    1600 8200
	0    -1   -1   0   
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J1
U 1 1 60546406
P 5400 4700
F 0 "J1" H 5480 4692 50  0000 L CNN
F 1 "Conn_01x04" H 5480 4601 50  0000 L CNN
F 2 "agro-footprint:mobo_oled_1.3" H 5400 4700 50  0001 C CNN
F 3 "~" H 5400 4700 50  0001 C CNN
	1    5400 4700
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:UI_Pushbutton_Omron UI1
U 1 1 60547ADB
P 7000 4400
F 0 "UI1" H 7000 4881 50  0000 C CNN
F 1 "UI_Pushbutton_Omron" H 7000 4790 50  0000 C CNN
F 2 "suku_basics:UI_BUTTON_OMRON" H 6850 4560 50  0001 C CNN
F 3 "~" H 7000 4860 50  0001 C CNN
	1    7000 4400
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:UI_Pushbutton_Omron UI2
U 1 1 605484BA
P 7000 5300
F 0 "UI2" H 7000 5781 50  0000 C CNN
F 1 "UI_Pushbutton_Omron" H 7000 5690 50  0000 C CNN
F 2 "suku_basics:UI_BUTTON_OMRON" H 6850 5460 50  0001 C CNN
F 3 "~" H 7000 5760 50  0001 C CNN
	1    7000 5300
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:UI_Pushbutton_Omron UI3
U 1 1 60548E40
P 8100 4400
F 0 "UI3" H 8100 4881 50  0000 C CNN
F 1 "UI_Pushbutton_Omron" H 8100 4790 50  0000 C CNN
F 2 "suku_basics:UI_BUTTON_OMRON" H 7950 4560 50  0001 C CNN
F 3 "~" H 8100 4860 50  0001 C CNN
	1    8100 4400
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:UI_Pushbutton_Omron UI4
U 1 1 6054942C
P 8100 5300
F 0 "UI4" H 8100 5781 50  0000 C CNN
F 1 "UI_Pushbutton_Omron" H 8100 5690 50  0000 C CNN
F 2 "suku_basics:UI_BUTTON_OMRON" H 7950 5460 50  0001 C CNN
F 3 "~" H 8100 5760 50  0001 C CNN
	1    8100 5300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H1
U 1 1 605577C9
P 4700 6400
F 0 "H1" H 4800 6446 50  0000 L CNN
F 1 "MountingHole" H 4800 6355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 4700 6400 50  0001 C CNN
F 3 "~" H 4700 6400 50  0001 C CNN
	1    4700 6400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H2
U 1 1 605578AC
P 4700 6700
F 0 "H2" H 4800 6746 50  0000 L CNN
F 1 "MountingHole" H 4800 6655 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 4700 6700 50  0001 C CNN
F 3 "~" H 4700 6700 50  0001 C CNN
	1    4700 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H3
U 1 1 60557A47
P 4700 7000
F 0 "H3" H 4800 7046 50  0000 L CNN
F 1 "MountingHole" H 4800 6955 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 4700 7000 50  0001 C CNN
F 3 "~" H 4700 7000 50  0001 C CNN
	1    4700 7000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H4
U 1 1 60557B55
P 4700 7300
F 0 "H4" H 4800 7346 50  0000 L CNN
F 1 "MountingHole" H 4800 7255 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 4700 7300 50  0001 C CNN
F 3 "~" H 4700 7300 50  0001 C CNN
	1    4700 7300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H5
U 1 1 60558711
P 5700 6400
F 0 "H5" H 5800 6446 50  0000 L CNN
F 1 "MountingHole" H 5800 6355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 5700 6400 50  0001 C CNN
F 3 "~" H 5700 6400 50  0001 C CNN
	1    5700 6400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H6
U 1 1 60558717
P 5700 6700
F 0 "H6" H 5800 6746 50  0000 L CNN
F 1 "MountingHole" H 5800 6655 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 5700 6700 50  0001 C CNN
F 3 "~" H 5700 6700 50  0001 C CNN
	1    5700 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H7
U 1 1 6055871D
P 5700 7000
F 0 "H7" H 5800 7046 50  0000 L CNN
F 1 "MountingHole" H 5800 6955 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 5700 7000 50  0001 C CNN
F 3 "~" H 5700 7000 50  0001 C CNN
	1    5700 7000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H8
U 1 1 60558723
P 5700 7300
F 0 "H8" H 5800 7346 50  0000 L CNN
F 1 "MountingHole" H 5800 7255 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 5700 7300 50  0001 C CNN
F 3 "~" H 5700 7300 50  0001 C CNN
	1    5700 7300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H9
U 1 1 6056A3E8
P 3800 6400
F 0 "H9" H 3900 6446 50  0000 L CNN
F 1 "MountingHole" H 3900 6355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3800 6400 50  0001 C CNN
F 3 "~" H 3800 6400 50  0001 C CNN
	1    3800 6400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H10
U 1 1 6056A3EE
P 3800 6700
F 0 "H10" H 3900 6746 50  0000 L CNN
F 1 "MountingHole" H 3900 6655 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3800 6700 50  0001 C CNN
F 3 "~" H 3800 6700 50  0001 C CNN
	1    3800 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H11
U 1 1 6056A3F4
P 3800 7000
F 0 "H11" H 3900 7046 50  0000 L CNN
F 1 "MountingHole" H 3900 6955 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3800 7000 50  0001 C CNN
F 3 "~" H 3800 7000 50  0001 C CNN
	1    3800 7000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H12
U 1 1 6056A3FA
P 3800 7300
F 0 "H12" H 3900 7346 50  0000 L CNN
F 1 "MountingHole" H 3900 7255 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3800 7300 50  0001 C CNN
F 3 "~" H 3800 7300 50  0001 C CNN
	1    3800 7300
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H13
U 1 1 60572AC1
P 3000 6400
F 0 "H13" H 3100 6446 50  0000 L CNN
F 1 "MountingHole" H 3100 6355 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3000 6400 50  0001 C CNN
F 3 "~" H 3000 6400 50  0001 C CNN
	1    3000 6400
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H14
U 1 1 60572AC7
P 3000 6700
F 0 "H14" H 3100 6746 50  0000 L CNN
F 1 "MountingHole" H 3100 6655 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3000 6700 50  0001 C CNN
F 3 "~" H 3000 6700 50  0001 C CNN
	1    3000 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H15
U 1 1 60572ACD
P 3000 7000
F 0 "H15" H 3100 7046 50  0000 L CNN
F 1 "MountingHole" H 3100 6955 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3000 7000 50  0001 C CNN
F 3 "~" H 3000 7000 50  0001 C CNN
	1    3000 7000
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole H16
U 1 1 60572AD3
P 3000 7300
F 0 "H16" H 3100 7346 50  0000 L CNN
F 1 "MountingHole" H 3100 7255 50  0000 L CNN
F 2 "MountingHole:MountingHole_2.2mm_M2" H 3000 7300 50  0001 C CNN
F 3 "~" H 3000 7300 50  0001 C CNN
	1    3000 7300
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_ARM_JTAG_SWD_10 J2
U 1 1 60516A24
P 5600 -1000
F 0 "J2" H 5157 -954 50  0000 R CNN
F 1 "Conn_ARM_JTAG_SWD_10" H 5157 -1045 50  0000 R CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_2x05_P1.27mm_Horizontal" H 5600 -1000 50  0001 C CNN
F 3 "http://infocenter.arm.com/help/topic/com.arm.doc.ddi0314h/DDI0314H_coresight_components_trm.pdf" V 5250 -2250 50  0001 C CNN
	1    5600 -1000
	1    0    0    -1  
$EndComp
$EndSCHEMATC
