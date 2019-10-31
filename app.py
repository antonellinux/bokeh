
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from __flowers__ import *

# ======================================================================
# COMMON OBJECTS
# ======================================================================

o_div_logo = Div(text="<p><img src = 'https://www.localpensionspartnership.org.uk/Files/Templates/Designs/BasicDesign/images/LPP_logo.svg' height = 40 width = 120></p>")

df1 = pd.read_csv('data/data1.csv')
df2 = pd.read_csv('data/data2.csv')
df3 = pd.read_csv('data/data3.csv', dtype={'yyyymmdd':'str'})
df4 = pd.read_csv('data/data4.csv', dtype={'yyyymmdd':'str'})	
df4_sub = df4[df4['to_ccy'].isin(['EUR', 'USD', 'AUD', 'NZD', 'CHF', 'CAD'])]
df5 = pd.read_csv('data/data5.csv')	
df6 = pd.read_csv('data/data6.csv', dtype={'yyyymmdd':'str'})	
df7 = pd.read_csv('data/data7.csv', dtype={'yyyymmdd':'str'})

s_max_day = df3['yyyymmdd'].max()

# ======================================================================
# CREATE TABS
# ======================================================================

def create_tab_one():		
	
	params = {'height':370, 'width':800, 'barwidth':0.7, 'title':'Region weight (data @: ' + s_max_day + ')', 'default':'OVERALL'}
	o_plot1, o_drop1 = BarPlotWithDropDown(df1, 'region', 'weight', 'portfolio_name', params, False).create_widgets()

	params = {'height':370, 'width':800, 'barwidth':0.7, 'title':'Sector weight (data @: ' + s_max_day + ')', 'default':'OVERALL'}
	o_plot2, o_drop2 = BarPlotWithDropDown(df2, 'sector_name', 'weight', 'portfolio_name', params, False).create_widgets()

	params = {'height':780, 'width':800, 'barwidth':0.7, 'title':'Portolios weight by region', 'default':s_max_day}
	o_plot3, o_drop3 = MultiBarPlotWithDropDown(df3, ['region', 'portfolio_name'], 'weight', 'yyyymmdd', params, False).create_widgets()
	
	o_layout = column(o_div_logo, row(column(column(o_drop1, o_plot1), column(o_drop2, o_plot2)), column(o_drop3, o_plot3))) 

	return Panel(child = o_layout, title = 'Segments')	


def create_tab_two():	

	o_plot1, o_dd1 = TimeSeriesPlotWithDropDown(df4, 'yyyymmdd', 'fx_rate', 'to_ccy', {'height':400, 'width':800, 'title':'FxRate vs GBP', 'default':'USD'}, True).create_widgets()	
	o_plot2 = TimeSeriesPlot(df4_sub, 'yyyymmdd', 'fx_rate', 'to_ccy', {'height':440, 'width':800, 'title':'FxRate (AUD-CAD-CHF-EUR-NZD-USD)'}, True).create_plot()

	o_layout = column(o_div_logo, row(column(o_dd1, o_plot1), o_plot2))

	return Panel(child = o_layout, title = 'FX Rates')


def create_tab_three():	
	
	df5.sort_values(by=['portfolio_name', 'mkt_val_gbp'], ascending=[True, False], inplace=True)	
	o_tbl1, o_chk1 = TableWithDropDown(df5, 'portfolio_name', {'height':280, 'width':800, 'default':'OVERALL'}).create_widgets()	
	o_div1 = Div(text="<b>Top 10 Stocks by portfolio (data @: " + str(s_max_day) + ") </b>", style={'font-size': '100%'})
	
	df6.sort_values(by=['yyyymmdd', 'mkt_val_gbp'], ascending=[True, False], inplace=True)	
	o_tbl2, o_chk2 = TableWithDropDown(df6, 'yyyymmdd', {'height':280, 'width':800, 'default':str(s_max_day)}).create_widgets()	
	o_div2 = Div(text="<b>Top 10 Stocks by day</b>", style={'font-size': '100%'})

	df7.sort_values(by=['stock_name', 'yyyymmdd'], ascending=[True, True], inplace=True)	
	o_plot1, o_dd1 = TimeSeriesPlotWithDropDown(df7, 'yyyymmdd', 'close', 'stock_name', {'height':400, 'width':800, 'title':'Stock Quotes', 'default':'Accenture PLC'}, True).create_widgets()	
	
	df7_sub = df7.groupby('stock_name').tail(60)	
	o_plot2, o_dd2 = TimeSeriesPlotWithDropDown(df7_sub, 'yyyymmdd', 'per_change', 'stock_name', {'height':400, 'width':800, 'title':'Last 60 days volatility', 'default':'Accenture PLC'}, True).create_widgets()	

	o_layout = column(o_div_logo, row(column(o_div1, o_chk1, o_tbl1, o_dd1, o_plot1), column(o_div2, o_chk2, o_tbl2, o_dd2, o_plot2)))

	return Panel(child = o_layout, title = 'Stocks')


def create_tab_four():

	o_div = Div(text="<b>Download each data source</b>", style={'font-size': '100%'})

	o_btn1 = ExportDataButton(df1, 'data1', 'data1.csv').create_button()
	o_btn2 = ExportDataButton(df2, 'data2', 'data2.csv').create_button()
	o_btn3 = ExportDataButton(df3, 'data3', 'data3.csv').create_button()
	o_btn4 = ExportDataButton(df4, 'data4', 'data4.csv').create_button()
	o_btn5 = ExportDataButton(df5, 'data5', 'data5.csv').create_button()
	o_btn6 = ExportDataButton(df6, 'data6', 'data6.csv').create_button()
	o_btn7 = ExportDataButton(df7, 'data7', 'data7.csv').create_button()		

	o_layout = column(o_div_logo, o_div, o_btn1, o_btn2, o_btn3, o_btn4, o_btn5, o_btn6, o_btn7)

	return Panel(child = o_layout, title = 'Get Data')	

# ======================================================================
# WRAP UP
# ======================================================================

o_tab1 = create_tab_one()
o_tab2 = create_tab_two()
o_tab3 = create_tab_three()
o_tab4 = create_tab_four()

o_tabs = Tabs(tabs = [o_tab1, o_tab2, o_tab3, o_tab4])
curdoc().add_root(o_tabs)

