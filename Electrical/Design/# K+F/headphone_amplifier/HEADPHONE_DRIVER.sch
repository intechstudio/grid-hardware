EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 6
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
L suku_basics:R_POT_Dual_Separate RV?
U 1 1 5FF0C082
P 3200 1700
AR Path="/5FF0C082" Ref="RV?"  Part="1" 
AR Path="/5FF09E25/5FF0C082" Ref="RV?"  Part="1" 
AR Path="/5FF89B41/5FF0C082" Ref="RV?"  Part="1" 
AR Path="/5FF89E02/5FF0C082" Ref="RV?"  Part="1" 
AR Path="/5FF89F0F/5FF0C082" Ref="RV?"  Part="1" 
F 0 "RV?" H 3000 1600 50  0000 R CNN
F 1 "20k" H 3000 1700 50  0000 R CNN
F 2 "" H 3200 1700 50  0001 C CNN
F 3 "~" H 3200 1700 50  0001 C CNN
	1    3200 1700
	0    -1   1    0   
$EndComp
$Comp
L suku_basics:R_POT_Dual_Separate RV?
U 2 1 5FF0C088
P 3200 3500
AR Path="/5FF0C088" Ref="RV?"  Part="2" 
AR Path="/5FF09E25/5FF0C088" Ref="RV?"  Part="2" 
AR Path="/5FF89B41/5FF0C088" Ref="RV?"  Part="2" 
AR Path="/5FF89E02/5FF0C088" Ref="RV?"  Part="2" 
AR Path="/5FF89F0F/5FF0C088" Ref="RV?"  Part="2" 
F 0 "RV?" H 3000 3400 50  0000 R CNN
F 1 "20k" H 3000 3500 50  0000 R CNN
F 2 "" H 3200 3500 50  0001 C CNN
F 3 "~" H 3200 3500 50  0001 C CNN
	2    3200 3500
	0    -1   1    0   
$EndComp
$Comp
L Amplifier_Operational:NJM4556A U?
U 1 1 5FF0C08E
P 3600 2500
AR Path="/5FF0C08E" Ref="U?"  Part="1" 
AR Path="/5FF09E25/5FF0C08E" Ref="U?"  Part="1" 
AR Path="/5FF89B41/5FF0C08E" Ref="U?"  Part="1" 
AR Path="/5FF89E02/5FF0C08E" Ref="U?"  Part="1" 
AR Path="/5FF89F0F/5FF0C08E" Ref="U?"  Part="1" 
F 0 "U?" H 3600 2867 50  0000 C CNN
F 1 "NJM4556A" H 3600 2776 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 3600 2500 50  0001 C CNN
F 3 "http://www.njr.com/semicon/PDF/NJM4556A_E.pdf" H 3600 2500 50  0001 C CNN
	1    3600 2500
	1    0    0    1   
$EndComp
$Comp
L Amplifier_Operational:NJM4556A U?
U 2 1 5FF0CF5F
P 3600 4300
AR Path="/5FF0CF5F" Ref="U?"  Part="1" 
AR Path="/5FF09E25/5FF0CF5F" Ref="U?"  Part="2" 
AR Path="/5FF89B41/5FF0CF5F" Ref="U?"  Part="2" 
AR Path="/5FF89E02/5FF0CF5F" Ref="U?"  Part="2" 
AR Path="/5FF89F0F/5FF0CF5F" Ref="U?"  Part="2" 
F 0 "U?" H 3600 4667 50  0000 C CNN
F 1 "NJM4556A" H 3600 4576 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 3600 4300 50  0001 C CNN
F 3 "http://www.njr.com/semicon/PDF/NJM4556A_E.pdf" H 3600 4300 50  0001 C CNN
	2    3600 4300
	1    0    0    1   
$EndComp
$Comp
L Amplifier_Operational:NJM4556A U?
U 3 1 5FF0DF7D
P 4700 6000
AR Path="/5FF0DF7D" Ref="U?"  Part="1" 
AR Path="/5FF09E25/5FF0DF7D" Ref="U?"  Part="3" 
AR Path="/5FF89B41/5FF0DF7D" Ref="U?"  Part="3" 
AR Path="/5FF89E02/5FF0DF7D" Ref="U?"  Part="3" 
AR Path="/5FF89F0F/5FF0DF7D" Ref="U?"  Part="3" 
F 0 "U?" H 4658 6046 50  0000 L CNN
F 1 "NJM4556A" H 4658 5955 50  0000 L CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 4700 6000 50  0001 C CNN
F 3 "http://www.njr.com/semicon/PDF/NJM4556A_E.pdf" H 4700 6000 50  0001 C CNN
	3    4700 6000
	1    0    0    -1  
$EndComp
Text HLabel 2400 1700 0    50   Input ~ 0
IN_LEFT
Text HLabel 2400 3500 0    50   Input ~ 0
IN_RIGHT
Wire Wire Line
	2400 1700 2600 1700
$Comp
L suku_basics:RES R?
U 1 1 5FF11F72
P 2700 1700
AR Path="/5FF09E25/5FF11F72" Ref="R?"  Part="1" 
AR Path="/5FF89B41/5FF11F72" Ref="R?"  Part="1" 
AR Path="/5FF89E02/5FF11F72" Ref="R?"  Part="1" 
AR Path="/5FF89F0F/5FF11F72" Ref="R?"  Part="1" 
F 0 "R?" V 2504 1700 50  0000 C CNN
F 1 "10k" V 2595 1700 50  0000 C CNN
F 2 "suku_basics:RES_0805" H 2700 1700 50  0001 C CNN
F 3 "~" H 2700 1700 50  0001 C CNN
	1    2700 1700
	0    1    1    0   
$EndComp
$Comp
L suku_basics:RES R?
U 1 1 5FF12C84
P 2700 3500
AR Path="/5FF09E25/5FF12C84" Ref="R?"  Part="1" 
AR Path="/5FF89B41/5FF12C84" Ref="R?"  Part="1" 
AR Path="/5FF89E02/5FF12C84" Ref="R?"  Part="1" 
AR Path="/5FF89F0F/5FF12C84" Ref="R?"  Part="1" 
F 0 "R?" V 2504 3500 50  0000 C CNN
F 1 "10k" V 2595 3500 50  0000 C CNN
F 2 "suku_basics:RES_0805" H 2700 3500 50  0001 C CNN
F 3 "~" H 2700 3500 50  0001 C CNN
	1    2700 3500
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 1700 4000 2000
Wire Wire Line
	4000 2500 3900 2500
Wire Wire Line
	4000 3500 4000 3800
Wire Wire Line
	4000 4300 3900 4300
$Comp
L power:GND #PWR?
U 1 1 5FF20328
P 3200 2700
AR Path="/5FF09E25/5FF20328" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF20328" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF20328" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF20328" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3200 2450 50  0001 C CNN
F 1 "GND" H 3205 2527 50  0000 C CNN
F 2 "" H 3200 2700 50  0001 C CNN
F 3 "" H 3200 2700 50  0001 C CNN
	1    3200 2700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 2700 3200 2600
Wire Wire Line
	3200 2600 3300 2600
$Comp
L power:GND #PWR?
U 1 1 5FF20C9B
P 3200 4500
AR Path="/5FF09E25/5FF20C9B" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF20C9B" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF20C9B" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF20C9B" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 3200 4250 50  0001 C CNN
F 1 "GND" H 3205 4327 50  0000 C CNN
F 2 "" H 3200 4500 50  0001 C CNN
F 3 "" H 3200 4500 50  0001 C CNN
	1    3200 4500
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 4500 3200 4400
Wire Wire Line
	3200 4400 3300 4400
Connection ~ 4000 2500
Connection ~ 4000 4300
$Comp
L Connector:AudioJack2_Ground J?
U 1 1 5FF241B9
P 6000 3100
AR Path="/5FF09E25/5FF241B9" Ref="J?"  Part="1" 
AR Path="/5FF89B41/5FF241B9" Ref="J?"  Part="1" 
AR Path="/5FF89E02/5FF241B9" Ref="J?"  Part="1" 
AR Path="/5FF89F0F/5FF241B9" Ref="J?"  Part="1" 
F 0 "J?" H 5820 3118 50  0000 R CNN
F 1 "AudioJack2_Ground" H 5820 3027 50  0000 R CNN
F 2 "" H 6000 3100 50  0001 C CNN
F 3 "~" H 6000 3100 50  0001 C CNN
	1    6000 3100
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5800 3100 5600 3100
Wire Wire Line
	5600 3100 5600 2500
Wire Wire Line
	4000 2500 4300 2500
Wire Wire Line
	5800 3000 5500 3000
Wire Wire Line
	5500 3000 5500 4300
Wire Wire Line
	4000 4300 4300 4300
$Comp
L suku_basics:CAP_POL C?
U 1 1 5FF276C7
P 6000 3600
AR Path="/5FF09E25/5FF276C7" Ref="C?"  Part="1" 
AR Path="/5FF89B41/5FF276C7" Ref="C?"  Part="1" 
AR Path="/5FF89E02/5FF276C7" Ref="C?"  Part="1" 
AR Path="/5FF89F0F/5FF276C7" Ref="C?"  Part="1" 
F 0 "C?" H 6091 3646 50  0000 L CNN
F 1 "220u" H 6091 3555 50  0000 L CNN
F 2 "" H 6000 3600 50  0001 C CNN
F 3 "~" H 6000 3600 50  0001 C CNN
	1    6000 3600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 3500 6000 3300
$Comp
L power:GND #PWR?
U 1 1 5FF284F5
P 6000 3800
AR Path="/5FF09E25/5FF284F5" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF284F5" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF284F5" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF284F5" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 6000 3550 50  0001 C CNN
F 1 "GND" H 6005 3627 50  0000 C CNN
F 2 "" H 6000 3800 50  0001 C CNN
F 3 "" H 6000 3800 50  0001 C CNN
	1    6000 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 3800 6000 3700
$Comp
L suku_basics:RES R?
U 1 1 5FF28E3F
P 4400 4300
AR Path="/5FF09E25/5FF28E3F" Ref="R?"  Part="1" 
AR Path="/5FF89B41/5FF28E3F" Ref="R?"  Part="1" 
AR Path="/5FF89E02/5FF28E3F" Ref="R?"  Part="1" 
AR Path="/5FF89F0F/5FF28E3F" Ref="R?"  Part="1" 
F 0 "R?" V 4596 4300 50  0000 C CNN
F 1 "47R" V 4505 4300 50  0000 C CNN
F 2 "suku_basics:RES_0805" H 4400 4300 50  0001 C CNN
F 3 "~" H 4400 4300 50  0001 C CNN
	1    4400 4300
	0    1    -1   0   
$EndComp
Wire Wire Line
	4500 4300 5500 4300
$Comp
L suku_basics:RES R?
U 1 1 5FF293C3
P 4400 2500
AR Path="/5FF09E25/5FF293C3" Ref="R?"  Part="1" 
AR Path="/5FF89B41/5FF293C3" Ref="R?"  Part="1" 
AR Path="/5FF89E02/5FF293C3" Ref="R?"  Part="1" 
AR Path="/5FF89F0F/5FF293C3" Ref="R?"  Part="1" 
F 0 "R?" V 4596 2500 50  0000 C CNN
F 1 "47R" V 4505 2500 50  0000 C CNN
F 2 "suku_basics:RES_0805" H 4400 2500 50  0001 C CNN
F 3 "~" H 4400 2500 50  0001 C CNN
	1    4400 2500
	0    1    -1   0   
$EndComp
Wire Wire Line
	4500 2500 5600 2500
$Comp
L power:GND #PWR?
U 1 1 5FF2BA88
P 4600 6400
AR Path="/5FF09E25/5FF2BA88" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF2BA88" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF2BA88" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF2BA88" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4600 6150 50  0001 C CNN
F 1 "GND" H 4605 6227 50  0000 C CNN
F 2 "" H 4600 6400 50  0001 C CNN
F 3 "" H 4600 6400 50  0001 C CNN
	1    4600 6400
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 5FF2D086
P 4600 5600
AR Path="/5FF09E25/5FF2D086" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF2D086" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF2D086" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF2D086" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 4600 5450 50  0001 C CNN
F 1 "+12V" H 4615 5773 50  0000 C CNN
F 2 "" H 4600 5600 50  0001 C CNN
F 3 "" H 4600 5600 50  0001 C CNN
	1    4600 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4600 5700 4600 5600
Wire Wire Line
	4600 6400 4600 6300
$Comp
L suku_basics:CAP C?
U 1 1 5FF2EB0F
P 5500 6000
AR Path="/5FF09E25/5FF2EB0F" Ref="C?"  Part="1" 
AR Path="/5FF89B41/5FF2EB0F" Ref="C?"  Part="1" 
AR Path="/5FF89E02/5FF2EB0F" Ref="C?"  Part="1" 
AR Path="/5FF89F0F/5FF2EB0F" Ref="C?"  Part="1" 
F 0 "C?" H 5592 6046 50  0000 L CNN
F 1 "100n" H 5592 5955 50  0000 L CNN
F 2 "suku_basics:CAP_0805" H 5500 6000 50  0001 C CNN
F 3 "~" H 5500 6000 50  0001 C CNN
	1    5500 6000
	1    0    0    -1  
$EndComp
$Comp
L suku_basics:CAP C?
U 1 1 5FF2EFA7
P 6000 6000
AR Path="/5FF09E25/5FF2EFA7" Ref="C?"  Part="1" 
AR Path="/5FF89B41/5FF2EFA7" Ref="C?"  Part="1" 
AR Path="/5FF89E02/5FF2EFA7" Ref="C?"  Part="1" 
AR Path="/5FF89F0F/5FF2EFA7" Ref="C?"  Part="1" 
F 0 "C?" H 6092 6046 50  0000 L CNN
F 1 "1u" H 6092 5955 50  0000 L CNN
F 2 "suku_basics:CAP_0805" H 6000 6000 50  0001 C CNN
F 3 "~" H 6000 6000 50  0001 C CNN
	1    6000 6000
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 5FF2F5C4
P 5500 5600
AR Path="/5FF09E25/5FF2F5C4" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF2F5C4" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF2F5C4" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF2F5C4" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 5500 5450 50  0001 C CNN
F 1 "+12V" H 5515 5773 50  0000 C CNN
F 2 "" H 5500 5600 50  0001 C CNN
F 3 "" H 5500 5600 50  0001 C CNN
	1    5500 5600
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR?
U 1 1 5FF2FA7D
P 6000 5600
AR Path="/5FF09E25/5FF2FA7D" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF2FA7D" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF2FA7D" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF2FA7D" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 6000 5450 50  0001 C CNN
F 1 "+12V" H 6015 5773 50  0000 C CNN
F 2 "" H 6000 5600 50  0001 C CNN
F 3 "" H 6000 5600 50  0001 C CNN
	1    6000 5600
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 5600 6000 5900
Wire Wire Line
	5500 5600 5500 5900
$Comp
L power:GND #PWR?
U 1 1 5FF30DDA
P 5500 6400
AR Path="/5FF09E25/5FF30DDA" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF30DDA" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF30DDA" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF30DDA" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 5500 6150 50  0001 C CNN
F 1 "GND" H 5505 6227 50  0000 C CNN
F 2 "" H 5500 6400 50  0001 C CNN
F 3 "" H 5500 6400 50  0001 C CNN
	1    5500 6400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 5FF3102C
P 6000 6400
AR Path="/5FF09E25/5FF3102C" Ref="#PWR?"  Part="1" 
AR Path="/5FF89B41/5FF3102C" Ref="#PWR?"  Part="1" 
AR Path="/5FF89E02/5FF3102C" Ref="#PWR?"  Part="1" 
AR Path="/5FF89F0F/5FF3102C" Ref="#PWR?"  Part="1" 
F 0 "#PWR?" H 6000 6150 50  0001 C CNN
F 1 "GND" H 6005 6227 50  0000 C CNN
F 2 "" H 6000 6400 50  0001 C CNN
F 3 "" H 6000 6400 50  0001 C CNN
	1    6000 6400
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 6400 6000 6100
Wire Wire Line
	5500 6400 5500 6100
Wire Wire Line
	2800 1700 3000 1700
Wire Wire Line
	3400 1700 4000 1700
Wire Wire Line
	3200 1900 3200 2000
Wire Wire Line
	3200 2400 3300 2400
Wire Wire Line
	3400 3500 4000 3500
Wire Wire Line
	3200 3700 3200 3800
Wire Wire Line
	3200 4200 3300 4200
Wire Wire Line
	2800 3500 3000 3500
Wire Wire Line
	2400 3500 2600 3500
$Comp
L suku_basics:CAP C?
U 1 1 5FF48331
P 3600 2000
AR Path="/5FF09E25/5FF48331" Ref="C?"  Part="1" 
AR Path="/5FF89B41/5FF48331" Ref="C?"  Part="1" 
AR Path="/5FF89E02/5FF48331" Ref="C?"  Part="1" 
AR Path="/5FF89F0F/5FF48331" Ref="C?"  Part="1" 
F 0 "C?" V 3371 2000 50  0000 C CNN
F 1 "20p" V 3462 2000 50  0000 C CNN
F 2 "suku_basics:CAP_0805" H 3600 2000 50  0001 C CNN
F 3 "~" H 3600 2000 50  0001 C CNN
	1    3600 2000
	0    1    1    0   
$EndComp
$Comp
L suku_basics:CAP C?
U 1 1 5FF48A9E
P 3600 3800
AR Path="/5FF09E25/5FF48A9E" Ref="C?"  Part="1" 
AR Path="/5FF89B41/5FF48A9E" Ref="C?"  Part="1" 
AR Path="/5FF89E02/5FF48A9E" Ref="C?"  Part="1" 
AR Path="/5FF89F0F/5FF48A9E" Ref="C?"  Part="1" 
F 0 "C?" V 3371 3800 50  0000 C CNN
F 1 "20p" V 3462 3800 50  0000 C CNN
F 2 "suku_basics:CAP_0805" H 3600 3800 50  0001 C CNN
F 3 "~" H 3600 3800 50  0001 C CNN
	1    3600 3800
	0    1    1    0   
$EndComp
Wire Wire Line
	3500 3800 3200 3800
Connection ~ 3200 3800
Wire Wire Line
	3200 3800 3200 4200
Connection ~ 4000 3800
Wire Wire Line
	4000 3800 4000 4300
Wire Wire Line
	3700 3800 4000 3800
Wire Wire Line
	3700 2000 4000 2000
Connection ~ 4000 2000
Wire Wire Line
	4000 2000 4000 2500
Wire Wire Line
	3500 2000 3200 2000
Connection ~ 3200 2000
Wire Wire Line
	3200 2000 3200 2400
$EndSCHEMATC
