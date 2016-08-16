
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.plotly as py
from plotly.graph_objs import *

elec = pd.read_csv('raw_data/full_dataset_2016-08-08.csv',
	skiprows=0,
	parse_dates={'timestamp':['DATE','START TIME'],
				'timestamp_end':['DATE','END TIME']},
				index_col='timestamp')

def plotly_daily_by_week():

	plotly_name = 'My Electricity Use Visualizations/Heatmap Daily by Week'
	
	

	daily_totals = pd.DataFrame(np.zeros([len(elec['USAGE'].resample('W-MON', how='sum')),7]),
                            index = elec['USAGE'].resample('W-MON', how='sum').index)

	# Drop the last two rows to ensure each row is a full week
	daily_totals = pd.DataFrame(np.zeros([len(elec['USAGE'].resample('W-MON', how='sum')),7]),
	                            index = elec['USAGE'].resample('W-MON', how='sum').index)

	daily_totals.drop(daily_totals.tail(2).index, inplace=True)

	for j in range(len(daily_totals)):
	    for i in range(7):
	        #print i, j
	        daily_totals[i].ix[j] = elec['USAGE'].resample('D', how='sum').ix[(daily_totals.ix[j].name + pd.to_timedelta(i, unit='d'))]

	daily_totals.columns = ['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']

	daily_totals.sort_index(ascending=False, inplace=True)

	data = Data([
	    Heatmap(
	        y = daily_totals.columns,
	        x = daily_totals.index,
	        z = np.transpose(np.array(daily_totals)),
	        colorscale='YIOrRd',
	        reversescale=True,
	        colorbar = ColorBar(
	        	title = 'Kilowatt-Hours',
        		titleside='right'
        	)
	    )
	])

	layout = Layout(
	    yaxis = YAxis(tickangle=0),
	    autosize = False,
	    width = 800,
	    height = 300,
	    margin=Margin(
	        l=50,
	        r=50,
	        b=50,
	        t=50,
	        pad=4
	    )
	)

	#plot_url = py.plot(data, layout=layout, filename='Daily_Totals_by_Week')
	fig = Figure(data=data, layout=layout)
	py.iplot(fig, filename=plotly_name)
	
	print "Sent to Plotly: ", plotly_name

def plotly_hourly_heatmap_last_week():

	plotly_name = 'My Electricity Use Visualizations/Heatmap Hourly Last Week'


	last_week = pd.DataFrame(elec['USAGE'].ix[elec['USAGE'].index.week == elec['USAGE'].index[-1].week])

	# Change this if not a full week at end of month!!
	week_index = ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']

	# Change size of dataframe if not a full week at end of month!!
	last_week_array = pd.DataFrame(np.zeros([6,24]))

	# Build array for last week
	for i in range(24):
	    last_week_array[i] = np.array(last_week[last_week.index.hour==i])
	last_week_array.index = week_index


	data = Data([
	    Heatmap(
	        x = range(0,24,1),
	        y = last_week_array.index,
	        z = np.array(last_week_array),
	        colorscale='YIGnBu',
	        reversescale=True)
	])

	layout = Layout(
	    title='Week of %s <br>'%last_week.ix[0].name.strftime('%B %d, %Y'),
	    yaxis = YAxis(autorange='reversed')
	)
	#plot_url = py.plot(data, filename='Last Week Heat Map')
	fig = Figure(data=data, layout=layout)
	py.iplot(fig, filename=plotly_name)

	print "Sent to Plotly: ", plotly_name

if __name__ == "__main__":
	main()
