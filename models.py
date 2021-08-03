# import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from linearmodels import PanelOLS, PooledOLS

# output display settings
pd.options.display.max_columns = None
# import the two datasets, include a log of vacancies and drop weeks 1 and 52
df = pd.read_stata("BGT_totals.dta")
df = df[~df["week"].isin([1, 52])]
df["log_postings"] = np.log(df["job_postings_count"])

df_i = pd.read_stata("BGT_industries.dta")
df_i = df_i[~df_i["week"].isin([1, 52])]
df_i["log_postings"] = np.log(df_i["job_postings_count"])

# TOTAL Overall model with ln(Postings)
df1 = df.copy()
df1 = df1[~(df1["week"] > 48)]
df1["after"] = np.where(df1["week"] >= 11, 1, 0)  # 11
df1["y2020"] = np.where(df1["year"] == 2020, 1, 0)
df1 = df1.set_index(["year", "week"])

mod_1 = PanelOLS.from_formula(
    "log_postings ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df1
)
res_1 = mod_1.fit()
print(res_1)

# TOTAL Overall model with Postings
df1 = df.copy()
df1 = df1[~(df1["week"] > 48)]
df1["after"] = np.where(df1["week"] >= 11, 1, 0)
df1["y2020"] = np.where(df1["year"] == 2020, 1, 0)
df1 = df1.set_index(["year", "week"])

mod_2 = PanelOLS.from_formula(
    "job_postings_count ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df1
)
res_2 = mod_2.fit()
print(res_2)
print(res_2.params)
print(res_2.std_errors)

# TOTAL First wave model with ln(Postings)
df3 = df.copy()
df3 = df3[~(df3["week"] > 30)]
df3["after"] = np.where(df3["week"] >= 11, 1, 0)
df3["y2020"] = np.where(df3["year"] == 2020, 1, 0)
df3 = df3.set_index(["year", "week"])

mod_3 = PanelOLS.from_formula(
    "log_postings ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df3
)
res_3 = mod_3.fit()
print(res_3)

# TOTAL First wave model with Postings
df4 = df.copy()
df4 = df4[~(df4["week"] > 30)]
df4["after"] = np.where(df4["week"] >= 11, 1, 0)
df4["y2020"] = np.where(df4["year"] == 2020, 1, 0)
df4 = df4.set_index(["year", "week"])

mod_4 = PanelOLS.from_formula(
    "job_postings_count ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df4
)
res_4 = mod_4.fit()
print(res_4)
print(res_4.params)
print(res_4.std_errors)

# TOTAL Recovery phase model with ln(Postings)
df1 = df.copy()
df1 = df1[~(df1["week"] < 30)]
df1 = df1[~(df1["week"] > 48)]
df1["y2020"] = np.where(df1["year"] == 2020, 1, 0)
df1 = df1.set_index(["year", "week"])

mod_5 = sm.formula.ols(formula="log_postings ~ 1 + y2020", data=df1)
res_5 = mod_5.fit()
print(res_5.summary())

# TOTAL Recovery phase model with Postings
df1 = df.copy()
df1 = df1[~(df1["week"] < 30)]
df1 = df1[~(df1["week"] > 48)]
df1["y2020"] = np.where(df1["year"] == 2020, 1, 0)
df1 = df1.set_index(["year", "week"])

mod_6 = sm.formula.ols(formula="job_postings_count ~ 1 + y2020", data=df1)
res_6 = mod_6.fit()
print(res_6.summary())
print(res_6.params)
print(res_6.bse)

# pick industries for the industries models
industries = [
    "Professional scientific & technical activities",
    "Education",
    "Human health & social work activities",
    "Wholesale & retail trade; repair of motor vehicles and motor cycles",
    "Accommodation & food service activities",
    "Administrative & support service activities",
    "Financial & insurance activities",
    "Information & communication",
    "Transport & storage",
    "Manufacturing",
    "Other service activities",
    "Construction",
    "Arts, entertainment & recreation",
    "Real estate activities",
    "Water supply, sewerage, waste",
    "Mining & quarrying",
    "Agriculture, Forestry and Fishing",
    "Electricity, gas, steam & air conditioning supply",
]

# INDUSTRIES Overall model with ln(Postings) (outputs a regression for all industries seperately)
for industry in industries:
    df_i1 = df_i.copy()
    df_i1 = df_i1[df_i1["group_name"] == industry]
    df_i1 = df_i1[~(df_i1["week"] > 48)]
    df_i1["after"] = np.where(df_i1["week"] >= 11, 1, 0)
    df_i1["y2020"] = np.where(df_i1["year"] == 2020, 1, 0)
    df_i1 = df_i1.set_index(["year", "week"])

    mod_i1 = PanelOLS.from_formula(
        "log_postings ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df_i1
    )
    res_i1 = mod_i1.fit()
    print()
    print("****************" + industry)
    print(res_i1)
    print(res_i1.params)

# INDUSTRIES First wave model with ln(Postings) (outputs a regression for all industries seperately)
for industry in industries:
    df_i1 = df_i.copy()
    df_i1 = df_i1[df_i1["group_name"] == industry]
    df_i1 = df_i1[~(df_i1["week"] > 30)]
    df_i1["after"] = np.where(df_i1["week"] >= 11, 1, 0)
    df_i1["y2020"] = np.where(df_i1["year"] == 2020, 1, 0)
    df_i1 = df_i1.set_index(["year", "week"])

    mod_i2 = PanelOLS.from_formula(
        "log_postings ~ 1 + after : y2020 + EntityEffects + TimeEffects", data=df_i1
    )
    res_i2 = mod_i2.fit()
    print()
    print("****************" + industry)
    print(res_i2)
    print(res_i2.params)

# INDUSTRIES Recovery phase model with ln(Postings) (outputs a regression for all industries seperately)
for industry in industries:
    df_i1 = df_i.copy()
    df_i1 = df_i1[df_i1["group_name"] == industry]
    df_i1 = df_i1[~(df_i1["week"] < 30)]
    df_i1 = df_i1[~(df_i1["week"] > 48)]
    df_i1["y2020"] = np.where(df_i1["year"] == 2020, 1, 0)
    df_i1 = df_i1.set_index(["year", "week"])

    mod_i3 = sm.formula.ols(formula="log_postings ~ 1 + y2020", data=df_i1)
    res_i3 = mod_i3.fit()
    print()
    print("****************" + industry)
    print(res_i3.summary())
    print(res_i3.params)
