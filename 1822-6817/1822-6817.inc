* Start of model for 1822-6817
* URL: /CgiBin/PPR.pl?hppn=1822-6817
* RCS: $Id: 1822-6817.inc,v 1.1 2022/01/09 00:25:01 cdsbuild Exp cdsbuild $
* Description: IC-Crosspoint Switch CML 3.2Gbps dual 32-QFN
* Manufacturer_info:
*  - NB4N840MMNR4G : ONSEMI
* Extractor: pinarath
* Version: 0.02
* Date Extracted: Sat Jan  8 17:25:01 2022
* Level: RoqDC
.subckt '1822-6817' 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
+ 20 21 22 23 24 25 26 27 28 29 30 31 32 %PMH1
* Model for 1822-6817 goes here
* Power drawn by the RPD to get
* the supply current of 130mA at 3.3V
RPD 10 9 10k
*****SHORTING GND PINS*******
R_gnd_short 9 24 1
*****SHORTING VCC PINS*******
R_vcc_short1 10 13 1
R_vcc_short2 10 23 1
R_vcc_short3 10 20 1
R_vcc_short4 10 17 1
R_vcc_short5 10 16 1
* Input stages
Xi1 26 27 10 9 diff_inp_1822_6817
Xi3 2 3 10 9 diff_inp_1822_6817
Xi2 6 7 10 9 diff_inp_1822_6817
Xi4 30 31 10 9 diff_inp_1822_6817
*
* Output stage
Xo1 22 21 10 9 cml_outp_1822_6817
Xo2 15 14 10 9 cml_outp_1822_6817
Xo3 19 18 10 9 cml_outp_1822_6817
Xo4 12 11 10 9 cml_outp_1822_6817
*
* Connecting Exposed Pad to VEE
RVE 9 %PMH1 1
* Pin_number pin_name symbol
* 1 ENB1 1
* 2 DB1 1
* 3 NOT_DB1 1
* 4 ENB0 1
* 5 SELB0 1
* 6 DB0 1
* 7 NOT_DB0 1
* 8 SELB1 1
* 9 GND_1 1
* 10 VCC_1 1
* 11 NOT_QB0 1
* 12 QB0 1
* 13 VCC_2 1
* 14 NOT_QB1 1
* 15 QB1 1
* 16 VCC_3 1
* 17 VCC_4 1
* 18 NOT_QA1 1
* 19 QA1 1
* 20 VCC_5 1
* 21 NOT_QA0 1
* 22 QA0 1
* 23 VCC_6 1
* 24 GND_2 1
* 25 SELA1 1
* 26 DA0 1
* 27 NOT_DA0 1
* 28 SELA0 1
* 29 ENA0 1
* 30 DA1 1
* 31 NOT_DA1 1
* 32 ENA1 1
* %PMH1 GND_3 1
.ends
.subckt cml_outp_1822_6817 %q %qb %vcc %gnd
**********************
*  CML output stage  *
**********************
RC50a %vcc %q 50
RC50b %vcc %qb 50
QO1 %qb %b1 %e QMOD_OUT
QO2 %q %b2 %e QMOD_OUT
CC1 %q %vcc 500p
CC2 %qb %vcc 500p
*** MCA = current sink Gives accurate sink current ***
***This helps for the output voltage difference matching***
MCA %e %gnd %gnd %gnd ML2WN4A L=2u W=162u
* 
CE %e %gnd 50p
* Add the resistive divider here
R1 %vcc %b1 2K
R2 %b1 %gnd 5K
R3 %vcc %b2 5K
R4 %b2 %gnd 1K
* All Models
.model QMOD_OUT NPN BF=100 RC=10 RE=10 RB=100
.model ML2WN4A MOSFET NMOS VTO=-0.7 KP=816.3u RD=50m RS=50m 
+RD=5m RS=5m
.ends
.subckt diff_inp_1822_6817 %in %inb %vcc %gnd
**********************
*  CML input stage   *
**********************
R_int_term1 %vcc %in 50
R_int_term2 %vcc %inb 50
* RC50a %vcc %q 50
* RC50b %vcc %qb 50
QO1 %q %in %e QMOD_OUT
QO2 %qb %inb %e QMOD_OUT
CC1 %q %vcc 500p
CC2 %qb %vcc 500p
*** MSA = current sink***
*** This helps in the total current matching ***
MSA %e %gnd %gnd %gnd ML2WN2A L=2u W=152u
CE %e %gnd 50p
* Protection diode at IN
DINP %in %vcc DMOD_0p5v_16mA
DINN %gnd %in DMOD_0p5v_16mA
DINBP %inb %vcc DMOD_0p5v_16mA
DINBN %gnd %inb DMOD_0p5v_16mA
*** All Models 
.model QMOD_OUT NPN BF=100 RC=1 RE=1 RB=10
.model DMOD_0p5v_16mA D RS=3.5 N=1 IS=33n
.model ML2WN2A UCBMOS NMOS VTO=-0.7 KP=816.3u RD=50m RS=50m
+RD=5m RS=5m
.ends
* RATINGS SECTION
* abs_max_ratings:
*   vcc_max: 3.8
*   vda0_max: 3.8
*   vda1_max: 3.8
*   vdb0_max: 3.8
*   vdb1_max: 3.8
*   vdda0_max: 3.8
*   vdda1_max: 3.8
*   vddb0_max: 3.8
*   vddb1_max: 3.8
*   i_da0_max: 45m
*   i_da0_bar_max: 45m
*   i_da1_max: 45m
*   i_da1_bar_max: 45m
*   i_db0_max: 45m
*   i_db0_bar_max: 45m
*   i_db1_max: 45m
*   i_db1_bar_max: 45m
*   i_out_qb0max: 25m
*   i_out_qb1max: 25m
*   i_out_qa0max: 25m
*   i_out_qa1max: 25m
*   i_outb_qb0max: 25m
*   i_outb_qb1max: 25m
*   i_outb_qa0max: 25m
*   i_outb_qa1max: 25m
* measure_stress:
*   vcc_max: '(v(10)-v(9))'
*   vda0_max: 'abs(v(26))-abs(v(9))'
*   vda1_max: 'abs(v(30))-abs(v(9))'
*   vdb0_max: 'abs(v(6))-abs(v(9))'
*   vdb1_max: 'abs(v(2))-abs(v(9))'
*   vdda0_max: 'abs(v(26))-abs(v(27))'
*   vdda1_max: 'abs(v(30))-abs(v(31))'
*   vddb0_max: 'abs(v(6))-abs(v(7))'
*   vddb1_max: 'abs(v(2))-abs(v(3))'
*   i_da0_max: 'abs(i(xi1.qo1.b))'
*   i_da0_bar_max: 'abs(i(xi1.qo2.b))'
*   i_da1_max: 'abs(i(xi4.qo1.b))'
*   i_da1_bar_max: 'abs(i(xi4.qo2.b))'
*   i_db0_max: 'abs(i(xi2.qo1.b))'
*   i_db0_bar_max: 'abs(i(xi2.qo2.b))'
*   i_db1_max: 'abs(i(xi3.qo1.b))'
*   i_db1_bar_max: 'abs(i(xi3.qo2.b))'
*   i_out_qb0max: 'abs(i(xo4.qo2.c))'
*   i_out_qb1max: 'abs(i(xo2.qo2.c))'
*   i_out_qa0max: 'abs(i(xo1.qo2.c))'
*   i_out_qa1max: 'abs(i(xo3.qo2.c))'
*   i_outb_qb0max: 'abs(i(xo4.qo1.c))'
*   i_outb_qb1max: 'abs(i(xo2.qo1.c))'
*   i_outb_qa0max: 'abs(i(xo1.qo1.c))'
*   i_outb_qa1max: 'abs(i(xo3.qo1.c))'
* END RATINGS
* Notes:
* It is the interface only for CML based switch.
* The model draws the supply current of 129.8mA at 3.3V ,
* which is close to the actual value given in the datasheet.
* Also here the CML differential output voltage has been 
* matched.
* The input enable and the enable selector pins have not
* been considered in this model.
* The MUX has not been modelled here.
* 
* Notes on Ratings:
* - Protection diodes has been given to the inputs.
* End of model for 1822-6817
*
