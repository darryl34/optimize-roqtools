* Start of model for 1855-3098
* URL: /CgiBin/PPR.pl?hppn=1855-3098
* RCS: $Id: 1855-3098.inc,v 1.1 2021/11/02 23:25:02 cdsbuild Exp cdsbuild $
* Description: Transistor-MOSFET N-channel enhancement-mode 80V 3.5m Ohm 104W Silicon 8-SO  
* Manufacturer_info:
*  - SiR680ADP-T1-RE3 : VISHAY
* Extractor: waisleon
* Version: 0.02
* Date Extracted: Tue Nov  2 17:25:02 2021
* Level: RoqDC
.subckt '1855-3098' 1 2 3 4 5
* Model for 1855-3098 goes here
* Shorting all Source pins
RS1 1 2 1
RS2 1 3 1
RS3 2 3 1
*
* Mosfet
M1 5 4 1 1 MN3098 W=10u L=1u
D1 1 5 DBDY
.model MN3098 UCBMOS NMOS VTO=3.9 KP=7.371316463536168 LAMBDA=10.0
+ RS=0.008079720509344518 RD=5.5210403416128046e-05 CGSO=438.9u CGDO=2.600u
.model DBDY D N=1.107 IS=0.427n RS=2m BV=80 IBV=1m
* Pin_number pin_name symbol
* 1 S1 1
* 2 S2 1
* 3 S3 1
* 4 G 1
* 5 D 1
.ends
* RATINGS SECTION
* abs_max_ratings:
*   vds_max: 80
*   vgs_max: 20
*   idc_max: 24.5
*   id_max: 300
*   pd_max: 2.75
* measure_stress:
*   vds_max: 'abs(v(5)-v(1))'
*   vgs_max: 'abs(v(4)-v(1))'
*   idc_max: 'abs(i(m1.d))'
*   id_max: 'abs(i(m1.d))'
*   pd_max: 'abs(v(4)*i(m1.g)+v(1)*i(m1.s)+v(5)*i(m1.d))+abs(i(d1)*(v(1)-v(5)))'
* END RATINGS
* Notes:
*On Model:
* - The value of VTO is extended to 3.74V above max VTO of 3.5V
*   specified in Datasheet in order to have a good matching.
* - The Output characteristics have good match for VGS<6V.
* - The tranfer characteristics tend to have higher error as IDS increases, 
*   not a very good match.
*On Ratings:
* - id_max is the Pulsed Drain Current at t = 100us.
* - idc_max is the Continuous Drain Current derated at TA = 70 degC.
*
* - Power Calculation:
* -  pd_max calculated using Junction temp and R-theta-JA as below:
*         Max Junction Temp Tj allowed = 25 + 80% of (150DegC - 25DegC)
*                                      = 125 DegC
*         For this part, worst case R-theta-ja(max) is 20 DegC/W  
*         under condition t <= 10 s, assume surface 
*         mounted on 1" x 1" FR4 board.
*
*         Max Ambient Temp = 70 DegC
*         Max temp rise allowed = 125-70= 55 DegC
*         Max Power Diss allowed using R-Theta-JA
*         pd_max = (55DegC) / (20DegC/W)
*              = 2.75W
*     Using pd_max=2.75W to limit junction temp rise.
* - Capacitance CISS and CRSS are taken at condition below from Datasheet:
*          VDS = 40V, VGS = 0V, f = 1MHz
* End of model for 1855-3098
*
