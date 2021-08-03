# import dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from scipy.interpolate import make_interp_spline, BSpline

# import the two datasets
df = pd.read_stata("BGT_totals.dta")
df2 = pd.read_stata("BGT_industries.dta")

# FIGURE 1 - TOTAL WEEKLY VACANCIES
# drop weeks 1 and 52
df = df[~df["week"].isin([1, 52])]
# split dataset into three years
year18 = df[df["year"] == 2018]
year19 = df[df["year"] == 2019]
year20 = df[df["year"] == 2020]
# prepare 2018 smooth data
x18 = year18["week"]
y18 = year18["job_postings_count"]
x18new = np.linspace(x18.min(), x18.max(), 300)
spl18 = make_interp_spline(x18, y18, k=3)
y18smooth = spl18(x18new)
# prepare 2019 smooth data
x19 = year19["week"]
y19 = year19["job_postings_count"]
x19new = np.linspace(x19.min(), x19.max(), 300)
spl19 = make_interp_spline(x19, y19, k=3)
y19smooth = spl19(x19new)
# prepare 2020 smooth data
x20 = year20["week"]
y20 = year20["job_postings_count"]
x20new = np.linspace(x20.min(), x20.max(), 300)
spl20 = make_interp_spline(x20, y20, k=3)
y20smooth = spl20(x20new)
# create the figure, include all lines and labels, save it
plt.figure(figsize=(12, 8))
plt.plot(x18new, y18smooth, "#D0C9CC", label="2018")
plt.plot(x19new, y19smooth, "#8A8285", label="2019")
plt.plot(x20new, y20smooth, "#D81B60", label="2020", linewidth=2)
plt.axvline(
    x=[10],
    color="#FFC107",
    lw=2,
    label="First death",
)
plt.axvline(
    x=[13],
    color="#1E88E5",
    lw=2,
    label="First lockdown starts",
)
plt.axvline(
    x=[30],
    color="#25D2FF",
    lw=2,
    label="First lockdown ends",
)
plt.axvline(
    x=[42],
    color="#338F20",
    lw=2,
    label="Second lockdown starts",
)
plt.xlabel("Weeks of the year")
plt.ylabel("Vacancies per week")
plt.legend()
plt.savefig("Figure1")

# FIGRURE 2 - WEEKLY VACANCIES IN DIFFERENT INDUSTRIES
# make logs of vacancies
df2["log_postings"] = np.log(df2["job_postings_count"])
# drop weeks 1 and 52
df2 = df2[~df2["week"].isin([1, 52])]
# prepare the "canvas"
fig, axs = plt.subplots(6, 3, figsize=(27, 36))
# pick the industries I am using
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
# for every industry, create their individual chart with all lines and labels
for i, ax in enumerate(axs.flat):
    industry = industries[i]

    year18 = df2[(df2["year"] == 2018) & (df2["group_name"] == industry)]
    year19 = df2[(df2["year"] == 2019) & (df2["group_name"] == industry)]
    year20 = df2[(df2["year"] == 2020) & (df2["group_name"] == industry)]

    x18 = year18["week"]
    y18 = year18["log_postings"]
    x18new = np.linspace(x18.min(), x18.max(), 300)
    spl18 = make_interp_spline(x18, y18, k=3)
    y18smooth = spl18(x18new)

    x19 = year19["week"]
    y19 = year19["log_postings"]
    x19new = np.linspace(x19.min(), x19.max(), 300)
    spl19 = make_interp_spline(x19, y19, k=3)
    y19smooth = spl19(x19new)

    x20 = year20["week"]
    y20 = year20["log_postings"]
    x20new = np.linspace(x20.min(), x20.max(), 300)
    spl20 = make_interp_spline(x20, y20, k=3)
    y20smooth = spl20(x20new)

    ax.plot(x18new, y18smooth, "#D0C9CC", label="2018")
    ax.plot(x19new, y19smooth, "#8A8285", label="2019")
    ax.plot(x20new, y20smooth, "#D81B60", label="2020", linewidth=2)
    ax.axvline(
        x=[10],
        color="#FFC107",
        lw=2,
        label="First death",
    )
    ax.axvline(
        x=[13],
        color="#1E88E5",
        lw=2,
        label="First lockdown starts",
    )
    ax.axvline(
        x=[30],
        color="#25D2FF",
        lw=2,
        label="First lockdown ends",
    )
    ax.axvline(
        x=[42],
        color="#338F20",
        lw=2,
        label="Second lockdown starts",
    )
    ax.set_title(industry, fontsize=16)
    ax.set(xlabel="Week of the year", ylabel="Log of vacancies per week")
    if ax == axs.flat[-1]:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(
            handles,
            labels,
            loc="upper center",
            ncol=7,
            fontsize=20,
            fancybox=True,
            bbox_to_anchor=(0.5, 0.11),
        )
# save the final figure
plt.savefig("Figure2")

# FIGURE 3 - RESULTS
# name and pick final industries + the whole labour market
res_industries = [
    "THE WHOLE LABOUR MARKET",
    "Professional scientific & technical activities",
    "Education",
    "Human health & social work activities*",
    "Wholesale & retail trade",
    "Accommodation & food service activities",
    "Administrative & support service activities",
    "Financial & insurance activities",
    "Information & communication",
    "Transport & storage**",
    "Manufacturing",
    "Other service activities",
    "Construction**",
    "Arts, entertainment & recreation",
    "Real estate activities",
    "Water supply, sewerage, waste**",
    "Mining & quarrying",
    "Agriculture, Forestry and Fishing",
    "Electricity, gas, steam & air conditioning supply",
]
res_industries.reverse()
# estimates from the Overall model
overall = [
    -29.17,
    -40.98,
    -32.22,
    -0.80,
    -40.77,
    -74.09,
    -41.97,
    -33.20,
    -32.91,
    -39.40,
    -42.27,
    -44.53,
    -40.73,
    -61.58,
    -40.79,
    -40.08,
    -73.07,
    -37.43,
    -42.99,
]
overall.reverse()
# estimates from the First wave model
first_wave = [
    -39.34,
    -50.38,
    -37.55,
    -1.27,
    -50.69,
    -82.53,
    -53.93,
    -41.41,
    -42.87,
    -57.19,
    -54.12,
    -51.55,
    -56.40,
    -68.81,
    -52.53,
    -48.75,
    -73.43,
    -38.34,
    -53.76,
]
first_wave.reverse()
# estimates from the Recovery phase model
recovery = [
    -12.49,
    -17.08,
    -20.11,
    16.14,
    -26.05,
    -57.63,
    -28.58,
    -17.01,
    -12.83,
    -9.30,
    -19.05,
    -19.03,
    -2.88,
    -50.96,
    -15.67,
    -7.30,
    -54.86,
    -17.50,
    -52.84,
]
recovery.reverse()
data = {
    "Recovery phase": recovery,
    "First wave": first_wave,
    "Overall": overall,
}
# merge the results
df3 = pd.DataFrame(data, index=res_industries)
# create a chart from them and save it
plt.rc("axes", axisbelow=True)
plt.rc("xtick", labelsize=22)
plt.rc("ytick", labelsize=22)
df3.plot.barh(figsize=(20, 26), width=0.8, color=["#338F20", "#1E88E5", "#FFC107"])
plt.grid(b=True)
handles, labels = plt.gca().get_legend_handles_labels()
order = [2, 1, 0]
plt.legend(
    [handles[idx] for idx in order],
    [labels[idx] for idx in order],
    loc="upper center",
    ncol=3,
    fancybox=True,
    bbox_to_anchor=(0.5, -0.02),
    fontsize=24,
)
plt.tight_layout()
plt.gca().xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}%"))
plt.figtext(
    0.5,
    -0.01,
    "* - Overall and First wave effects not statistically significant",
    fontsize=20,
)
plt.figtext(
    0.5, -0.02, "** - Recovery phase effects not statistically significant", fontsize=20
)
plt.savefig("Figure3")