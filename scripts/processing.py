import pandas as pd
import numpy as np
import os


def get_average_hourly_profiles(data):
	grouped = data.groupby([(data.index.dayofweek==5) | (data.index.dayofweek==6),data.index.hour])["USAGE"].mean()
	return grouped

def get_start_of_last_full_week(data):
	last_day_in_data = data.ix[len(data)-1].name
	start_of_last_full_week = pd.to_datetime((last_day_in_data
		- pd.DateOffset(days=(last_day_in_data.dayofweek+8))).date())
	return start_of_last_full_week

#def get_week(data, raw_week_start)

def get_week_daily_sums(data, week_start):
	"""Returns time series of the last full week of data of daily summed kWh """
	#start_of_last_full_week = get_start_of_last_full_week(data)

	#data.ix[week_start:(week_start + pd.DateOffset(days=8))]
	last_week_daily_sums = data["USAGE"].ix[week_start:(week_start + pd.DateOffset(days=8))].resample("D", how="sum")
	return last_week_daily_sums

def get_week_hourly_profiles(data, week_start):
	#start_of_last_full_week = get_start_of_last_full_week(data)

	week_usage_data = ELEC_WEATHER["USAGE"].ix[week_start:(week_start + pd.DateOffset(days=7))]
	grouped = week_usage_data.groupby([week_usage_data.index.date,week_usage_data.index.hour])
	week_hourly_profiles = pd.DataFrame(grouped.agg(lambda x: x)).unstack(level=0)["USAGE"].iloc[:,:7]

	return week_hourly_profiles

def get_avg_week_daily_sums(data):
	void

if __name__ == "__main__":

	main()