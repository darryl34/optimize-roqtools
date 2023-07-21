* Start of model for 1822-2408
* URL: http://cds.soco.agilent.com/perl/PPR.pl?hppn=1822-2408
* RCS: $Id: 1822-2408.inc,v 1.1 2006/11/25 09:04:18 cdsbuild Exp cdsbuild $
* Description: IC Interface Clock Distribution 1.2GHz PLL 5-output 48-CSP  
* Manufacturer_info:
*  - AD9511BCPZ : ANALOG DEVICES
*  - AD9511BCPZ-REEL7 : ANALOG DEVICES
* Extractor: waisleon
* Version: 0.01
* Date Extracted: Sat Nov 25 01:04:18 2006
* Map File: /usr/esappsMA/hpdl/libraries/hpdl/pcb_parts/master_maps/17493.pfr.map
* Level: RoqDC
.subckt '1822-2408' 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
+ 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41
+ 42 43 44 45 46 47 48 %PMH1
* Model for 1822-2408 goes here
* Power Draw Section
* Model draws Typ supply current of 0.17A from VS (PD=550mW)
MCL 3 19 19 19 ML2WN4A L=2u W=14.6u
.model ML2WN4A UCBMOS NMOS VTO=-0.7 KP=81.63m RD=5.0m RS=5.0m
*
* Output Stages
* ECL Output Interfaces
XO0 42 41 3 19 outp_ecl_1822_2408
XO1 27 26 3 19 outp_ecl_1822_2408
XO2 21 20 3 19 outp_ecl_1822_2408
*
* LVDS Output Interfaces
XO3 3 35 34 19 outs_lvds_1822_2408
XO4 3 31 30 19 outs_lvds_1822_2408
*
* Adding protection diodes on Input pins
* with assumed current limit of 10mA
DCPRSETU 47 3 DMOD_0p3_10m
DCPRSETD 19 47 DMOD_0p3_10m
RCPRSET 19 47 100k
*
DRSETU 45 3 DMOD_0p3_10m
DRSETD 19 45 DMOD_0p3_10m
RRSET 19 45 100k
*
DNOT_CSU 17 3 DMOD_0p3_10m
DNOT_CSD 19 17 DMOD_0p3_10m
RNOT_CS 19 17 100k
*
DSCLKU 14 3 DMOD_0p3_10m
DSCLKD 19 14 DMOD_0p3_10m
RSCLK 19 14 100k
*
DSTATUSU 13 3 DMOD_0p3_10m
DSTATUSD 19 13 DMOD_0p3_10m
RSTATUS 19 13 100k
*
DFUNCTIONU 12 3 DMOD_0p3_10m
DFUNCTIOND 19 12 DMOD_0p3_10m
RFUNCTION 19 12 100k
*
DNOT_CLK1U 11 3 DMOD_0p3_10m
DNOT_CLK1D 19 11 DMOD_0p3_10m
RNOT_CLK1 19 11 100k
*
DCLK1U 10 3 DMOD_0p3_10m
DCLK1D 19 10 DMOD_0p3_10m
RCLK1 19 10 100k
*
DNOT_CLK2U 8 3 DMOD_0p3_10m
DNOT_CLK2D 19 8 DMOD_0p3_10m
RNOT_CLK2 19 8 100k
*
DCLK2U 7 3 DMOD_0p3_10m
DCLK2D 19 7 DMOD_0p3_10m
RCLK2 19 7 100k
*
DNOT_REFINU 2 3 DMOD_0p3_10m
DNOT_REFIND 19 2 DMOD_0p3_10m
RNOT_REFIN 19 2 100k
*
DREFINU 1 3 DMOD_0p3_10m
DREFIND 19 1 DMOD_0p3_10m
RREFIN 19 1 100k
*
.model DMOD_0p3_10m D N=1 IS=1.26019e-07 RS=1
*
* Shorting all VS pins
RVS001 3 6 1
RVS002 3 9 1
RVS003 3 18 1
RVS004 3 22 1
RVS005 3 23 1
RVS006 3 25 1
RVS007 3 28 1
RVS008 3 29 1
RVS009 3 32 1
RVS010 3 33 1
RVS011 3 36 1
RVS012 3 39 1
RVS013 3 40 1
RVS014 3 44 1
RVS015 3 48 1
RVS016 6 9 1
RVS017 6 18 1
RVS018 6 22 1
RVS019 6 23 1
RVS020 6 25 1
RVS021 6 28 1
RVS022 6 29 1
RVS023 6 32 1
RVS024 6 33 1
RVS025 6 36 1
RVS026 6 39 1
RVS027 6 40 1
RVS028 6 44 1
RVS029 6 48 1
RVS030 9 18 1
RVS031 9 22 1
RVS032 9 23 1
RVS033 9 25 1
RVS034 9 28 1
RVS035 9 29 1
RVS036 9 32 1
RVS037 9 33 1
RVS038 9 36 1
RVS039 9 39 1
RVS040 9 40 1
RVS041 9 44 1
RVS042 9 48 1
RVS043 18 22 1
RVS044 18 23 1
RVS045 18 25 1
RVS046 18 28 1
RVS047 18 29 1
RVS048 18 32 1
RVS049 18 33 1
RVS050 18 36 1
RVS051 18 39 1
RVS052 18 40 1
RVS053 18 44 1
RVS054 18 48 1
RVS055 22 23 1
RVS056 22 25 1
RVS057 22 28 1
RVS058 22 29 1
RVS059 22 32 1
RVS060 22 33 1
RVS061 22 36 1
RVS062 22 39 1
RVS063 22 40 1
RVS064 22 44 1
RVS065 22 48 1
RVS066 23 25 1
RVS067 23 28 1
RVS068 23 29 1
RVS069 23 32 1
RVS070 23 33 1
RVS071 23 36 1
RVS072 23 39 1
RVS073 23 40 1
RVS074 23 44 1
RVS075 23 48 1
RVS076 25 28 1
RVS077 25 29 1
RVS078 25 32 1
RVS079 25 33 1
RVS080 25 36 1
RVS081 25 39 1
RVS082 25 40 1
RVS083 25 44 1
RVS084 25 48 1
RVS085 28 29 1
RVS086 28 32 1
RVS087 28 33 1
RVS088 28 36 1
RVS089 28 39 1
RVS090 28 40 1
RVS091 28 44 1
RVS092 28 48 1
RVS093 29 32 1
RVS094 29 33 1
RVS095 29 36 1
RVS096 29 39 1
RVS097 29 40 1
RVS098 29 44 1
RVS099 29 48 1
RVS100 32 33 1
RVS101 32 36 1
RVS102 32 39 1
RVS103 32 40 1
RVS104 32 44 1
RVS105 32 48 1
RVS106 33 36 1
RVS107 33 39 1
RVS108 33 40 1
RVS109 33 44 1
RVS110 33 48 1
RVS111 36 39 1
RVS112 36 40 1
RVS113 36 44 1
RVS114 36 48 1
RVS115 39 40 1
RVS116 39 44 1
RVS117 39 48 1
RVS118 40 44 1
RVS119 40 48 1
RVS120 44 48 1
*
* Shorting all GND pins
RGND01 19 24 1
RGND02 19 37 1
RGND03 19 38 1
RGND04 19 43 1
RGND05 19 46 1
RGND06 19 %PMH1 1
RGND07 24 37 1
RGND08 24 38 1
RGND09 24 43 1
RGND10 24 46 1
RGND11 24 %PMH1 1
RGND12 37 38 1
RGND13 37 43 1
RGND14 37 46 1
RGND15 37 %PMH1 1
RGND16 38 43 1
RGND17 38 46 1
RGND18 38 %PMH1 1
RGND19 43 46 1
RGND20 43 %PMH1 1
RGND21 46 %PMH1 1
*
* Pin_number pin_name symbol
* 1 REFIN A
* 2 NOT_REFIN A
* 3 VS_1 A
* 4 VCP A
* 5 CP A
* 6 VS_2 A
* 7 CLK2 A
* 8 NOT_CLK2 A
* 9 VS_3 A
* 10 CLK1 A
* 11 NOT_CLK1 A
* 12 FUNCTION A
* 13 STATUS A
* 14 SCLK A
* 15 SDIO A
* 16 SDO A
* 17 NOT_CS A
* 18 VS_4 A
* 19 GND_1 A
* 20 NOT_OUT2 A
* 21 OUT2 A
* 22 VS_5 A
* 23 VS_6 A
* 24 GND_2 A
* 25 VS_7 A
* 26 NOT_OUT1 A
* 27 OUT1 A
* 28 VS_8 A
* 29 VS_9 A
* 30 NOT_OUT4 A
* 31 OUT4 A
* 32 VS_10 A
* 33 VS_11 A
* 34 NOT_OUT3 A
* 35 OUT3 A
* 36 VS_12 A
* 37 GND_3 A
* 38 GND_4 A
* 39 VS_13 A
* 40 VS_14 A
* 41 NOT_OUT0 A
* 42 OUT0 A
* 43 GND_5 A
* 44 VS_15 A
* 45 RSET A
* 46 GND_6 A
* 47 CPRSET A
* 48 VS_16 A
* %PMH1 GND_7 A
.ends
.subckt outp_ecl_1822_2408 %q %qb %vcc %vee
****************
*Output stage*
****************
QO  %vcc %b1 %q  QMOD_OUT
QOB %vcc %b2 %qb QMOD_OUT
* Biased the bases,
* estimated RB1 and RB2 values
RB1 %vcc %b1 110.2
RB2 %vcc %b2 425
* MB1 and MB2 are 3mA and 3mA current sinks
MB1 %b1 %vee %vee %vee ML2WN4A L=2u W=30u
MB2 %b2 %vee %vee %vee ML2WN4A L=2u W=30u
***************************
*Models*
***************************
.model QMOD_OUT  NPN  BF=100 
+      RC=1 RE=4 RB=1 IS=222f
.model ML2WN4A UCBMOS NMOS VTO=-0.7
+      KP=816.3u RD=500m RS=500m
.ends
.subckt outs_lvds_1822_2408 %vdd %out %outn %gnd
MPD1 %vdd %mnpa %mnpa %mnpa ML2WN2A L=2u W=0.00025878545818674965
C1 %vdd %mnpa 10p
MP7 %outnx %m5d %mnpa %mnpa PMOD_OUT L=1u W=350u
MP8 %outx %m6d %mnpa %mnpa PMOD_OUT L=1u W=350u
MN7 %outnx %m5d %mnda %mnda NMOD_OUT L=1u W=100u
MN8 %outx %m6d %mnda %mnda NMOD_OUT L=1u W=100u
MND1 %mnda %gnd %gnd %gnd ML2WN2A L=2u W=0.0006914264151186789
C2 %mnda %gnd 10p
MCMFB %mnda %cmfbn1 %gnd %gnd NMOD_OUT L=1u W=100u
Ccmfb %cmfbn1 %gnd 10p
Rcmfb %cmfb %cmfbn1 1K
*
RMEASP %outx %out 1
RMEASN %outnx %outn 1
RC1 %out %cmfb 100K 
RC2 %cmfb %outn 100K
*
* Default Model state : out is high,
* outn is low. Swap RPU/RPD on m5d and 
* m6d nodes to reverse the state.
*
RPU %vdd %m5d 100K
RPD %m6d %gnd 100K
* 
CDIFF %out %outn 5p
* 
* All Models
.model PMOD_OUT UCBMOS PMOS VTO=-0.7 KP=0.00039323511935629825 RD=249.77477688807704 RS=183.33445743330222 
.model NMOD_OUT UCBMOS NMOS VTO=0.7 KP=550u RD=113.7 RS=113.7
.model ML2WN2A UCBMOS NMOS VTO=-0.7 KP=1650u RD=500m RS=500m 
.ends
* RATINGS SECTION
* abs_max_ratings:
*   vvs_max: 3.6
*   vvs_rev_max: 0.3
*   vvcp_max: 5.8
*   vvcp_rev_max: 0.3
*   vvcp_vs_max: 5.8
*   vvcp_vs_rev_max: 0.3
*   vclk1_diff_max: 1.2
*   vclk2_diff_max: 1.2
*   idcprsetu_max: 10m
*   idcprsetd_max: 10m
*   idrsetu_max: 10m
*   idrsetd_max: 10m
*   idnot_csu_max: 10m
*   idnot_csd_max: 10m
*   idsclku_max: 10m
*   idsclkd_max: 10m
*   idstatusu_max: 10m
*   idstatusd_max: 10m
*   idfunctionu_max: 10m
*   idfunctiond_max: 10m
*   idnot_clk1u_max: 10m
*   idnot_clk1d_max: 10m
*   idclk1u_max: 10m
*   idclk1d_max: 10m
*   idnot_clk2u_max: 10m
*   idnot_clk2d_max: 10m
*   idclk2u_max: 10m
*   idclk2d_max: 10m
*   idnot_refinu_max: 10m
*   idnot_refind_max: 10m
*   idrefinu_max: 10m
*   idrefind_max: 10m
* measure_stress:
*   vvs_max: '(v(3)-v(19))'
*   vvs_rev_max: '(v(19)-v(3))'
*   vvcp_max: '(v(4)-v(19))'
*   vvcp_rev_max: '(v(19)-v(4))'
*   vvcp_vs_max: '(v(4)-v(3))'
*   vvcp_vs_rev_max: '(v(3)-v(4))'
*   vclk1_diff_max: 'abs(v(10)-v(11))'
*   vclk2_diff_max: 'abs(v(7)-v(8))'
*   idcprsetu_max: 'abs(i(dcprsetu))'
*   idcprsetd_max: 'abs(i(dcprsetd))'
*   idrsetu_max: 'abs(i(drsetu))'
*   idrsetd_max: 'abs(i(drsetd))'
*   idnot_csu_max: 'abs(i(dnot_csu))'
*   idnot_csd_max: 'abs(i(dnot_csd))'
*   idsclku_max: 'abs(i(dsclku))'
*   idsclkd_max: 'abs(i(dsclkd))'
*   idstatusu_max: 'abs(i(dstatusu))'
*   idstatusd_max: 'abs(i(dstatusd))'
*   idfunctionu_max: 'abs(i(dfunctionu))'
*   idfunctiond_max: 'abs(i(dfunctiond))'
*   idnot_clk1u_max: 'abs(i(dnot_clk1u))'
*   idnot_clk1d_max: 'abs(i(dnot_clk1d))'
*   idclk1u_max: 'abs(i(dclk1u))'
*   idclk1d_max: 'abs(i(dclk1d))'
*   idnot_clk2u_max: 'abs(i(dnot_clk2u))'
*   idnot_clk2d_max: 'abs(i(dnot_clk2d))'
*   idclk2u_max: 'abs(i(dclk2u))'
*   idclk2d_max: 'abs(i(dclk2d))'
*   idnot_refinu_max: 'abs(i(dnot_refinu))'
*   idnot_refind_max: 'abs(i(dnot_refind))'
*   idrefinu_max: 'abs(i(drefinu))'
*   idrefind_max: 'abs(i(drefind))'
* END RATINGS
* Notes:
* - It is a non-functional model with ECL and LVDS output interfaces.
* - Datasheet does not provide the supply current directly.
*   Current drawn is calculated based on the Typ PD = 550mW at VS = 3.3V
*   from Table 11 under Specifications.
*   Using the formula:
*           P = V*I
*           I = 550m/3.3 = 0.17A
*
*   Conditions: Power-up default state; does not include power dissipated
*               in output load resistors. No clock.
*
* - The model meets the Typ output levels of VOH and VOL per Datasheet specs
*   from Table 3.
* - Internal bias currents are set by RSET and CPRSET resistors externally.
* End of model for 1822-2408
*
