

# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from __flowers__ import *

# ======================================================================
# CREATE TABS
# ======================================================================

def create_tab_one():

	##### import data

	df1 = pd.read_csv('data1.csv')
	df2 = pd.read_csv('data2.csv')
	df3 = pd.read_csv('data3.csv', dtype={'yyyymmdd':'str'})

	##### define last day

	s_max_day = df3['yyyymmdd'].max()

	##### create objects

	params = {'height':400, 'width':800, 'barwidth':0.7, 'title':'Region weight (data @: ' + s_max_day + ')', 'default':'OVERALL'}
	o_plot1, o_drop1 = BarPlotWithDropDown(df1, 'region', 'weight', 'portfolio_name', params, False).create_widgets()

	params = {'height':400, 'width':800, 'barwidth':0.7, 'title':'Sector weight (data @: ' + s_max_day + ')', 'default':'OVERALL'}
	o_plot2, o_drop2 = BarPlotWithDropDown(df2, 'sector_name', 'weight', 'portfolio_name', params, False).create_widgets()

	params = {'height':840, 'width':800, 'barwidth':0.7, 'title':'Portolios weight by region', 'default':s_max_day}
	o_plot3, o_drop3 = MultiBarPlotWithDropDown(df3, ['region', 'portfolio_name'], 'weight', 'yyyymmdd', params, False).create_widgets()
	
	o_layout = row(column(column(o_drop1, o_plot1), column(o_drop2, o_plot2)), column(o_drop3, o_plot3)) 

	return Panel(child = o_layout, title = 'Segments')		

# ======================================================================
# WRAP UP
# ======================================================================

o_tab = create_tab_one()
o_tabs = Tabs(tabs = [o_tab])
curdoc().add_root(o_tabs)
