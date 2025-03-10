cd /Users/rcb95/Desktop

import delimited using final_dispensations.csv, clear

save final_dispensations.dta

use final_dispensations.dta

* create dummies for years to/from treatment date.

foreach x in 0 1 {
	gen es_p_`x'=time_to_treat_year==`x' if time_to_treat_year!=.
}


foreach x in 6 5 4 3 2 {
	gen es_m_`x'=time_to_treat_year==-`x' if time_to_treat_year!=.
}

recode es_* (.=0)


gen omitted=0

foreach x in es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1{
	gen `x'Xlowpresc=`x'*lowpresc_normd
}

label var es_m_6Xlowpresc "-6"
label var es_m_5Xlowpresc "-5"
label var es_m_4Xlowpresc "-4"
label var es_m_3Xlowpresc "-3"
label var es_m_2Xlowpresc "-2"
label var omitted "-1"
label var es_p_0Xlowpresc "0"
label var es_p_1Xlowpresc "1"

reghdfe final_count es_m_6Xlowpresc es_m_5Xlowpresc es_m_4Xlowpresc es_m_3Xlowpresc es_m_2Xlowpresc omitted es_p_0Xlowpresc es_p_1Xlowpresc, a(county year) cluster(county)

*reghdfe final_count lowpresc_normd##(es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1), a(county year) cluster(county)


coefplot, drop(_cons) title("Event Study (Dispensations, Yearly)") xtitle("Years from Treatment") vertical label omit
*reghdfe final_count lowpresc_normd##es_*, a(county year) cluster(county)
 

coefplot, drop(_cons) title("Event Study") yline(0) vertical label omit

*********************************
* quarterly data

import delimited using final_dispensations.csv, clear

save final_dispensations.dta

use final_dispensations.dta


gen es_m_lte10=time_to_treat_quarter<=-10 if time_to_treat_quarter!=.

foreach x in 0 1 2 {
	gen es_p_`x'=time_to_treat_quarter==`x' if time_to_treat_quarter!=.
}


foreach x in 9 8 7 6 5 4 3 2 {
	gen es_m_`x'=time_to_treat_quarter==-`x' if time_to_treat_quarter!=.
}

recode es_* (.=0)

*reghdfe final_count lowpresc_normd##(es_m_lte10 es_m_9 es_m_8 es_m_7 es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1 es_p_2), a(county quarter) cluster(county)
*coefplot, drop(_cons) yline(0) vertical 

foreach x in es_m_lte10 es_m_9 es_m_8 es_m_7 es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1 es_p_2{
	gen `x'Xlowpresc=`x'*lowpresc_normd_median
}

gen omitted=0

label var es_m_lte10Xlowpresc "<=-10"
label var es_m_9Xlowpresc "-9"
label var es_m_8Xlowpresc "-8"
label var es_m_7Xlowpresc "-7"
label var es_m_6Xlowpresc "-6"
label var es_m_5Xlowpresc "-5"
label var es_m_4Xlowpresc "-4"
label var es_m_3Xlowpresc "-3"
label var es_m_2Xlowpresc "-2"
label var omitted "-1"
label var es_p_0Xlowpresc "0"
label var es_p_1Xlowpresc "1"
label var es_p_2Xlowpresc "2"

gen log_var=log(final_count)

reghdfe log_var es_m_lte10Xlowpresc es_m_9Xlowpresc es_m_8Xlowpresc es_m_7Xlowpresc es_m_6Xlowpresc es_m_5Xlowpresc es_m_4Xlowpresc es_m_3Xlowpresc es_m_2Xlowpresc omitted es_p_0Xlowpresc es_p_1Xlowpresc es_p_2Xlowpresc, a(county quarter) cluster(county)

coefplot, drop(_cons) title("Event Study (Log(Dispensations), Quarterly)") xtitle("Quarters from Treatment") vertical label omit



********************************
* create dummies for quarters to/from treatment date for all quarters

foreach x in 0 1 2 {
	gen es_p_`x'=time_to_treat_quarter==`x' if time_to_treat_quarter!=.
}


foreach x in 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 {
	gen es_m_`x'=time_to_treat_quarter==-`x' if time_to_treat_quarter!=.
}

recode es_* (.=0)
* *

* event study and plot
gen omitted=0

*encode log_count, generate(log_count2)

reghdfe final_count lowpresc_normd##(es_m_25 es_m_24 es_m_23 es_m_22 es_m_21 es_m_20 es_m_19 es_m_18 es_m_17 es_m_16 es_m_15 es_m_14 es_m_13 es_m_12 es_m_11 es_m_10 es_m_9 es_m_8 es_m_7 es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1 es_p_2), a(county year) cluster(county)

coefplot, drop(_cons) vertical nolab

** plot it
coefplot , keep(es_m_25 es_m_24 es_m_23 es_m_22 es_m_21 es_m_20 es_m_19 es_m_18 es_m_17 es_m_16 es_m_15 es_m_14 es_m_13 es_m_12 es_m_11 es_m_10 es_m_9 es_m_8 es_m_7 es_m_6 es_m_5 es_m_4 es_m_3 es_m_2 es_p_0 es_p_1 es_p_2 omitted es_m_1) vertical yline(0)  label    recast(line) cirecast(rarea) omit levels(95 90)   ciopts( recast(rarea rarea) color(%40 %20)   lpattern(dot dot)) 
reghdfe final_count es_m_6 es_m_5 es_m_4 es_m_3 es_m_2  es_p_0 es_p_1, a(county year) cluster(county)


******** diff in diff

* continuous variable
reghdfe final_count c.lowpresc_basic##treated_quarterly, a(county quarter) cluster(county)

* no norm, mean cutoff
reghdfe final_count lowpresc_basic##treated_quarterly, a(county quarter) cluster(county)

* normed, mean cut off
reghdfe log_var lowpresc_normd##treated_quarterly, a(county quarter) cluster(county)

* normed, median cut off
reghdfe log_var lowpresc_normd_median##treated_quarterly, a(county quarter) cluster(county)

* create table
outreg2 using Dispensations, keep(lowpresc_normd_median##treated_quarterly) dec(3) nocons word replace
