import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sb
import os
import processing as pr

plt.ioff()

PARAMS = 	{ 	"labelsize" : 16 ,
				"titlesize" : 18
			}

ELEC = pd.read_csv('../data/elec_full_dataset_2016-08-08.csv',
	skiprows=0,
	parse_dates={'timestamp':['DATE','START TIME'],
	'timestamp_end':['DATE','END TIME']},
	index_col='timestamp')

WEATHER = pd.read_csv('../data/weather_full_dataset_2016-08-10.csv',
	skiprows=0,
	parse_dates='timestamp',
	index_col='timestamp')

ELEC_WEATHER = pd.merge(WEATHER,ELEC,left_index=True,right_index=True)

def average_hourly_profiles():
	grouped = pr.get_average_hourly_profiles(ELEC_WEATHER)

	fig = plt.figure(figsize=[10,5])
	ax1 = plt.subplot(1,1,1)
	grouped[False].plot(label="Weekday")
	grouped[True].plot(label="Weekend")

	return fig

def all_weekly_sums():

	fig = plt.figure(figsize=[8,6])
	ax1 = plt.subplot(1,1,1)

	ELEC["USAGE"].resample("W",how="sum").plot()

	# turn off square border around plot
	ax1.spines["top"].set_visible(False)  
	ax1.spines["bottom"].set_visible(False)  
	ax1.spines["right"].set_visible(False)  
	ax1.spines["left"].set_visible(False)

	# turn off ticks
	ax1.tick_params(axis="both", which="both", bottom="off", top="off",
	               labelbottom="on", left="off", right="off", labelleft="on",labelsize=14) 
	
	plt.ylabel("Weekly Usage (kilowatt-hours)", fontsize=PARAMS["labelsize"])
	plt.title("Weekly Electricity Usage", fontsize=PARAMS["titlesize"])
	#plt.grid("off")
	return fig

def week_daily_sums(week_start):
	
	daily_sums = pr.get_week_daily_sums(ELEC_WEATHER, week_start)

	fig = plt.figure(figsize=[10,6])
	ax1 = plt.subplot(1,1,1)

	daily_sums[:7].plot(kind="bar")

	# turn off square border around plot
	ax1.spines["top"].set_visible(False)  
	ax1.spines["bottom"].set_visible(False)  
	ax1.spines["right"].set_visible(False)  
	ax1.spines["left"].set_visible(False)

	# turn off ticks
	ax1.tick_params(axis="both", which="both", bottom="off", top="off",
	               labelbottom="on", left="off", right="off", labelleft="on",labelsize=14) 
	
	ax1.set_xticklabels(daily_sums.index.map(lambda x: x.strftime("%A \n %b %d")),rotation=0)

 	plt.ylabel("Daily Usage (kilowatt-hours)", fontsize=PARAMS["labelsize"])
 	plt.xlabel("")
	plt.title("Daily Total Electricity Usage", fontsize=PARAMS["titlesize"])
	plt.grid("off")
# 	plt.show()

def week_hourly_profiles(week_start):

	fig = plt.figure(figsize=[10,6])
	ax1 = plt.subplot(1,1,1)

	week_hourly_profiles_df = pr.get_week_hourly_profiles(ELEC_WEATHER, week_start)

	week_hourly_profiles_df.plot()

def scatter_usage_temp():

	fig = plt.figure(figsize=[8,6])
	ax1 = plt.subplot(1,1,1)
	plt.plot(ELEC_WEATHER["tempF"], ELEC_WEATHER["USAGE"],
		marker="x", color='k',alpha=0.3, linestyle="none")
	

	plt.ylabel("Hourly Usage (kilowatt-hours)", fontsize=PARAMS["labelsize"])
	plt.xlabel("Outdoor Temperature (deg F)", fontsize=PARAMS["labelsize"])
	plt.title("Hourly Electricity Usage vs. Outdoor Temperature", fontsize=PARAMS["titlesize"])

	return fig

def heatmap():

	array = pd.DataFrame(np.zeros([len(ELEC['USAGE'].resample('d',how='sum')),24]),index=ELEC['USAGE'].resample('d',how='sum').index)

	for i in range(0,24):
	    array[i] = np.array(ELEC['USAGE'][ELEC.index.hour==i])

	array.sort_index(ascending=True, inplace=True)

	import matplotlib.dates as mdates

	#sundays = pd.Series(array[array.index.dayofweek==0].index)

	fig, ax = plt.subplots(figsize=[10,25])
	title('My Electricity Usage \n', fontsize=18)
	plt.imshow(array, interpolation='none', cmap='YlGnBu')
	plt.tick_params(axis="both", which="both", bottom="on", top="on",
	                labelbottom="on", labeltop='on', left="on", right="off", labelleft="on") 
	colorbar_ax = fig.add_axes([0.8, .375, .04, .25])
	cb = plt.colorbar(cax = colorbar_ax)
	cb.set_label('kilowatt-hours',fontsize = 16)

	xticks = range(0,24,4)
	yticks = range(0,len(array),7)

	ax.set_xticks(xticks)
	ax.set_yticks(yticks)
	ax.set_yticklabels(sundays.apply(lambda x: x.strftime('%B %d')), fontsize=14)
	ax.yaxis_date()

	#ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y')) This didn't work for me

	plt.tight_layout()
	plt.show()

def main():

	raw_week_start = raw_input("Enter start of week (YYYY MM DD):")
	week_start = pd.to_datetime(raw_week_start)
	# display = raw_input("Display All Plots? (yes or no)")
	# save = raw_input("Save Plots? (yes or no)")

	plots = {
		"all_weekly_sums_plot" : all_weekly_sums(),
		"scatter_usage_temp_plot" : scatter_usage_temp(),
		"average_profiles_plot" : average_hourly_profiles(),
		"week_daily_sums" : week_daily_sums(week_start),
		"week_hourly_profiles" : week_hourly_profiles(week_start),
	}

	plt.show()


if __name__ == "__main__":

	main()