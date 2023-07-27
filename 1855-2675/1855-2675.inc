* Start of model for 1855-2675
* URL: http://cds.srs.is.keysight.com/perl/PPR.pl?hppn=1855-2675
* RCS: $Id: 1855-2675.inc,v 1.1 2015/01/31 09:00:11 cdsbuild Exp cdsbuild $
* Description: Transistor-MOSFET N-channel enhancement-Mode 60V 0.0158 Ohm 71W Silicon 3-D2PAK  
* Manufacturer_info:
*  - IRFS3806TRLPBF : INFINEON TECHNOLOGIES
* Extractor: waisleon
* Version: 0.02
* Date Extracted: Sat Jan 31 02:00:11 2015
* Level: RoqDC
.subckt '1855-2675' 1 3 4
* Model for 1855-2675 goes here
M1 4 1 3 3 MN2675 W=10u L=1u
D1 3 4 DBDY2675
.model MN2675 UCBMOS NMOS VTO=5.724105129725181 KP=0.3346346227727194 LAMBDA=77.897189849304
+ RS=0.005779794258866416 RD=0.004086986099118235 CGSO=108.3u CGDO=6.7u
.model DBDY2675 D N=1.215 IS=0.244n RS=0.0042 BV=60 IBV=250u
* Pin_number pin_name symbol
* 1 G 1
* 3 S 1
* 4 D 1
.ends
* RATINGS SECTION
* abs_max_ratings:
*   vds_max: 60
*   vgs_max: 20
*   idc_max: 35.6
*   id_max: 170
*   pd_max: 1.21
* measure_stress:
*   vds_max: 'abs(v(4)-v(3))'
*   vgs_max: 'abs(v(1)-v(3))'
*   idc_max: 'abs(i(m1.d))'
*   id_max: 'abs(i(m1.d))'
*   pd_max: 'abs(v(1)*i(m1.g)+v(3)*i(m1.s)+v(4)*i(m1.d))+abs(i(d1)*(v(3)-v(4)))'
* END RATINGS
* Notes:
* - The value of VTO is extended to 4.14V above max VTO of 4.0V
*   specified in datasheet in order to have a good overall matching.
* - id_max is the Pulsed Drain Current.
* - idc_max is the Continuous Drain Current derated at Tc = 70 degC.
*
* - Power Calculation:
* -  pd_max calculated using Junction temp and R-theta-JA as below:
*         Max Junction Temp Tj allowed = 25 + 80% of (175DegC - 25DegC)
*                                      = 145 DegC
*         For this part, worst case R-theta-ja(max) is 62 DegC/W  
*         which assumes that the part is Device mounted on 
*         1 inch square PCB (FR-4 or G-10 Material).
*
*         Max Ambient Temp = 70 DegC
*         Max temp rise allowed = 145-70= 75 DegC
*         Max Power Diss allowed using R-Theta-JA
*         pd_max = (75DegC) / (62DegC/W)
*              = 1.21W
*     Using pd_max=1.21W to limit junction temp rise.
*
* - Capacitance Ciss and Crss are taken at VDS = 50V from Datasheet
*   as per Dynamic characteristics in Datasheet.
* End of model for 1855-2675
*
