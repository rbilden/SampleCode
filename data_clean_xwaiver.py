import numpy as np
from datetime import datetime
import pandas as pd

# read in datasets for PDMP bupe export and population size
df = pd.read_csv('/Users/rcb95/Desktop/locator_export.csv')
pop_df = pd.read_csv('/Users/rcb95/Desktop/pop_size.csv')
deathrate_df = pd.read_csv('/Users/rcb95/Desktop/deathrate.csv')
prov_pop_df = pd.read_csv('/Users/rcb95/Desktop/provider_pop.csv')

# Total is pop of healthcare providers
# population is all people in a county

counties = ['ADAMS',
'ALLEGHENY',
'ARMSTRONG',
'BEAVER',
'BEDFORD',
'BERKS',
'BLAIR',
'BRADFORD',
'BUCKS',
'BUTLER',
'CAMBRIA',
'CAMERON',
'CARBON',
'CENTRE',
'CHESTER',
'CLARION',
'CLEARFIELD',
'CLINTON',
'COLUMBIA',
'CRAWFORD',
'CUMBERLAND',
'DAUPHIN',
'DELAWARE',
'ELK',
'ERIE',
'FAYETTE',
'FOREST',
'FRANKLIN',
'FULTON',
'GREENE',
'HUNTINGDON',
'INDIANA',
'JEFFERSON',
'JUNIATA',
'LACKAWANNA',
'LANCASTER',
'LAWRENCE',
'LEBANON',
'LEHIGH',
'LUZERNE',
'LYCOMING',
'MCKEAN',
'MERCER',
'MIFFLIN',
'MONROE',
'MONTGOMERY',
'MONTOUR',
'NORTHAMPTON',
'NORTHUMBERLAND',
'PERRY',
'PHILADELPHIA',
'PIKE',
'POTTER',
'SCHUYLKILL',
'SNYDER',
'SOMERSET',
'SULLIVAN',
'SUSQUEHANNA',
'TIOGA',
'UNION',
'VENANGO',
'WARREN',
'WASHINGTON',
'WAYNE',
'WESTMORELAND',
'WYOMING',
'YORK']

# restrict data to selected counties
df = df[df['county'].isin(counties)]

# filter values to PA only
df = df.loc[df['state'] == 'PA' , 'county']

# count number of bupe prescribers by county
df1 = pd.DataFrame(df.value_counts())

df1['County'] = df1.index

# merge two dfs so have number of providers and population size
df1 = pd.merge(df1, pop_df, on='County', how='left')
df1 = pd.merge(df1, deathrate_df[['County', 'rate_per_100k']], on='County', how='left')
df1 = pd.merge(df1, prov_pop_df[['County', 'Total']], on='County', how='left')

# calculate cutoffs for low prescribers(treated) basic and normd 
basic_mean = np.mean(df1['count'])
basic_median = np.median(df1['count'])

###### norm = normed by county pop
# norm number of waivered prescr by population size
df1['normd_presc'] = df1['count']/df1['population']

normd_mean = np.mean(df1['normd_presc'])
normd_median = np.median(df1['normd_presc'])

# NORM break down prescribers by quartiles
quartiles_list = list(df1.normd_presc.quantile([0.2,0.4,0.6, 0.8]))
df1['LowPresc_normd_Q1'] = np.where(df1['normd_presc'] <= quartiles_list[0], 1, 0)
df1['LowPresc_normd_Q2'] = np.where(df1['normd_presc'] <= quartiles_list[1], 1, 0)
df1['LowPresc_normd_Q3'] = np.where(df1['normd_presc'] <= quartiles_list[2], 1, 0)
df1['LowPresc_normd_Q4'] = np.where(df1['normd_presc'] <= quartiles_list[3], 1, 0)

###### health_norm = normed by county pop of healthcare providers
df1['hnormd_presc'] = df1['count']/df1['Total']

hnormd_mean = np.mean(df1['hnormd_presc'])
hnormd_median = np.median(df1['hnormd_presc'])

# HEALTH NORM break down prescribers by quartiles
quartiles_list = list(df1.hnormd_presc.quantile([0.2,0.4,0.6, 0.8]))
df1['LowPresc_hnormd_Q1'] = np.where(df1['hnormd_presc'] <= quartiles_list[0], 1, 0)
df1['LowPresc_hnormd_Q2'] = np.where(df1['hnormd_presc'] <= quartiles_list[1], 1, 0)
df1['LowPresc_hnormd_Q3'] = np.where(df1['hnormd_presc'] <= quartiles_list[2], 1, 0)
df1['LowPresc_hnormd_Q4'] = np.where(df1['hnormd_presc'] <= quartiles_list[3], 1, 0)

########## OD
#define counties with highest overdose death rates
overdose_cutoff = np.mean(df1['rate_per_100k'])
df1['high_overdose_rate'] = np.where(df1['rate_per_100k'] >= overdose_cutoff, 1, 0)

# define counties with a high number of prescribers
df1['LowPresc_mean'] = np.where(df1['count'] <= basic_mean, 1, 0)
df1['LowPresc_mean_normd'] = np.where(df1['normd_presc'] <= normd_mean, 1, 0)
df1['LowPresc_mean_hnormd'] = np.where(df1['hnormd_presc'] <= hnormd_mean, 1, 0)

df1['LowPresc_median'] = np.where(df1['count'] <= basic_median, 1, 0)
df1['LowPresc_median_normd'] = np.where(df1['normd_presc'] <= normd_median, 1, 0)
df1['LowPresc_median_hnormd'] = np.where(df1['hnormd_presc'] <= hnormd_median, 1, 0)

# provider_count is new variable for number of providers that are X waivered
df1 = df1.rename(columns={'count': 'provider_count'})

#df1[['provider_count','County']].to_csv('waivered_data.csv')

temp_df = df1[['County', 'LowPresc_mean', 'provider_count', 'LowPresc_mean_normd', 'LowPresc_mean_hnormd', 'LowPresc_median', 'LowPresc_median_normd', 'LowPresc_median_hnormd', 'LowPresc_normd_Q1', 'LowPresc_normd_Q2', 'LowPresc_normd_Q3', 'LowPresc_normd_Q4', 'LowPresc_hnormd_Q1', 'LowPresc_hnormd_Q2', 'LowPresc_hnormd_Q3', 'LowPresc_hnormd_Q4','high_overdose_rate', 'population', 'Total']]
# read in bupe data

df2 = pd.read_csv('/Users/rcb95/Desktop/Buprenorphine data.csv')

# filter values to include all gender and all ages
df2 = df2.loc[df2['Gender'] == 'All Genders']
df2 = df2.loc[df2['Age Group'] == 'All Ages']

df2.to_csv('disp_data.csv')

# # capitalize all strings
df2 = df2.apply(lambda x: x.astype(str).str.upper())

# merge all the data

final_df = pd.merge(df2, temp_df, on='County', how='left')

# filter based on prescriptions or dispensations
final_df = final_df.loc[final_df['Measure'] == 'NUMBER OF DISPENSATIONS (BY PHARMACY LOCATION)']
#final_df = final_df.loc[final_df['Measure'] == 'NUMBER OF PRESCRIPTIONS (BY PATIENT LOCATION)']

final_df['Count1'] = final_df['Count'].astype(float)


# norm number of waivered prescr by population size
final_df['normd_prescriptions'] = final_df['Count1']/final_df['population']

prescr_median = np.median(final_df['Count1'])
prescr_median_normd = final_df['normd_prescriptions'].median()

final_df['Presc_median'] = np.where(final_df['Count1'] <= prescr_median, 1, 0)
final_df['Presc_median_normd'] = np.where(final_df['normd_prescriptions'] <= prescr_median_normd, 1, 0)


# convert date to usable format
# + pd.offsets.QuarterEnd(0) 
# offset yields quarter end date, without offset get beginning date
final_df['date'] = pd.to_datetime(final_df['Time Period'].str.replace(' ', ''))

pd.to_datetime('2016-07-01').to_period(freq='Q')

# create year variable for event study
final_df['year'] = pd.DatetimeIndex(final_df['date']).year
final_df['treatment_year'] = 2022
final_df['time_to_treat_year'] = final_df['year'] - final_df['treatment_year']
final_df['treated_yearly'] = np.where(final_df['time_to_treat_year'] >= 0, 1, 0)

# create quarter variable for event study
final_df['Quarter'] = pd.to_datetime(final_df['Time Period'].str.replace(' ', '').astype(str))
final_df['treatment_quarter'] = pd.to_datetime('2022Q4') + pd.offsets.QuarterEnd(0) 
final_df['time_to_treat_quarter'] = (final_df['Quarter'].dt.to_period('Q')-final_df['treatment_quarter'].dt.to_period('Q')).apply(lambda x: x.n)
final_df['treated_quarterly'] = np.where(final_df['time_to_treat_quarter'] >= 0, 1, 0)

# calcualte final count of measure and log for analysis
final_df['final_count'] = final_df['Count'].astype(float)
final_df['rate_count'] = final_df['final_count']/10000
final_df['log_count'] = np.log(final_df['final_count']).astype(float)

# PA county size data
# https://www.pennsylvania-demographics.com/counties_by_population

# save csv of new df
final_df.to_csv('final_dispensations.csv')

#print(len(final_df))
# print(final_df.columns.values.tolist())
# print(final_df.head())
