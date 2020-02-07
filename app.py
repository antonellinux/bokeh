
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
import __flowers__ as fw

# ======================================================================
# COMMON OBJECTS
# ======================================================================

LOGO = fw.Div(text = "<p><img src = 'https://www.localpensionspartnership.org.uk/Files/Templates/Designs/BasicDesign/images/LPP_logo.svg' height = 40 width = 120 align = right></p>", align = "end")
TITLE_STYLE = {'font-size':'100%', 'color':'#54BBAB'}

# ======================================================================
# TAB1
# ======================================================================

class Tab1( object ):

	def panel():

		sec = fw.Div(text = "<h1>tab1</h1>", style = {'font-size':'100%', 'color':'black'})
		return fw.Panel(child = sec, title = '1 - Summary')

# ======================================================================
# TAB2
# ======================================================================

class Tab2( object ):				

	#################### GET DATA

	df_char_overall = pd.read_csv('data/equity_char_overall.csv', dtype = {'yyyymmdd':'str'})		
	df_char_overall = df_char_overall.sort_values(by = ['yyyymmdd', 'portfolio'], ascending = [False, True])	

	#################### CREATE OBJECTS

	def object1( self ):

		params = {'height':300, 'width':1000, 'default':str(self.df_char_overall['yyyymmdd'].max()), 'columns':['portfolio', 'mkt_val', 'weight'], 'formats':['na', '0,0', '0.0%']}
		table, drop = fw.TableWithDropDown(self.df_char_overall, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Market value by month / portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, table
		

	def object2( self ):
		
		params = {'height':300, 'width':1000, 'title':'', 'default':'LPPI GEF INTERNAL EQUITY BNYMILTD', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_char_overall, 'yyyymmdd', 'weight', 'portfolio', params, True).create_widgets()
		div = fw.Div(text = "<b><i>Time series of market value weight</i></b>", style = TITLE_STYLE)	

		return div, drop, plot

	#################### CREATE PANEL

	def panel( self ):

		div1, drop1, table1 = self.object1()
		div2, drop2, plot2 = self.object2()
					
		sec1 = fw.Div(text = "<h1>OVERALL</h1>", style = {'font-size':'100%', 'color':'black'})		
		layout = fw.column(LOGO, sec1, fw.row(fw.column(div1, drop1, table1), fw.column(div2, drop2, plot2)))

		return fw.Panel(child = layout, title = '2 - Portfolio Characteristics')	

# ======================================================================
# TAB3
# ======================================================================

class Tab3( object ):

	#################### GET DATA

	df_risk_overall = pd.read_csv('data/equity_risk_overall.csv', dtype = {'yyyymmdd':'str'})
	df_risk_sec_reg = pd.read_csv('data/equity_risk_sec_reg.csv', dtype = {'yyyymmdd':'str'})
	df_risk_port = pd.read_csv('data/equity_risk_port.csv', dtype = {'yyyymmdd':'str'})
	df_risk_tick = pd.read_csv('data/equity_risk_tick.csv', dtype = {'yyyymmdd':'str'})
	df_risk_scnr = pd.read_csv('data/equity_risk_scnr.csv', dtype = {'yyyymmdd':'str'})	

	#################### SUBSET DATA

	df_risk_sec = df_risk_sec_reg.groupby(['yyyymmdd', 'sector'])[['allocation', 'contribution']].sum().reset_index()
	df_risk_reg = df_risk_sec_reg.groupby(['yyyymmdd', 'region'])[['allocation', 'contribution']].sum().reset_index()	

	#################### SORT DATA

	df_risk_overall = df_risk_overall.sort_values(by = ['yyyymmdd', 'volatility_1yr'], ascending = [False, False])
	df_risk_port = df_risk_port.sort_values(by = ['yyyymmdd', 'contribution'], ascending = [False, False])	
	df_risk_tick = df_risk_tick.sort_values(by = ['yyyymmdd', 'contribution'], ascending = [False, False])
	df_risk_scnr = df_risk_scnr.sort_values(by = ['yyyymmdd', 'p&l_amount'], ascending = [False, False])
	df_risk_sec = df_risk_sec.sort_values(by = ['yyyymmdd', 'contribution'], ascending = [False, False])
	df_risk_reg = df_risk_reg.sort_values(by = ['yyyymmdd', 'contribution'], ascending = [False, False])	

	max_day = str(df_risk_overall['yyyymmdd'].max())

	#################### CREATE OBJECTS

	def object1( self ):

		columns = ['portfolio', 'var_%_mv', 'cvar_%_mv', 'volatility_1yr', 'volatility_1yr_vs_msci']
		formats = ['na', '0.0%', '0.0%', '0.0%', '0.0%']

		params = {'height':325, 'width':1000, 'default':self.max_day, 'columns':columns, 'formats':formats}
		table, drop = fw.TableWithDropDown(self.df_risk_overall, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Risk table by month</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object2( self ):

		params = {'height':325, 'width':1000, 'title':'', 'default':'OVERALL', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_risk_overall, 'yyyymmdd', 'volatility_1yr', 'portfolio', params, True).create_widgets()
		div = fw.Div(text = "<b><i>Time series of Volatility by portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object3( self ):
		
		params = {'height':350, 'width':1000, 'default':self.max_day, 'columns':['sector', 'allocation', 'contribution'], 'formats':['na', '0.0%', '0.0%']}
		table, drop = fw.TableWithDropDown(self.df_risk_sec, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Risk table by month / sector</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object4( self ):

		params = {'height':350, 'width':1000, 'barwidth':0.7, 'title':'', 'default':str(self.df_risk_sec['yyyymmdd'].max())}
		plot, drop = fw.BarPlotWithDropDown(self.df_risk_sec, 'sector', 'contribution', 'yyyymmdd', params, False).create_widgets()
		div = fw.Div(text = "<b><i>Contribution by sector</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object5( self ):

		params = {'height':350, 'width':1000, 'default':self.max_day, 'columns':['region', 'allocation', 'contribution'], 'formats':['na', '0.0%', '0.0%']}
		table, drop = fw.TableWithDropDown(self.df_risk_reg, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Risk table by month / region</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object6( self ):

		params = {'height':350, 'width':1000, 'barwidth':0.7, 'title':'', 'default':str(self.df_risk_reg['yyyymmdd'].max())}
		plot, drop = fw.BarPlotWithDropDown(self.df_risk_reg, 'region', 'contribution', 'yyyymmdd', params, False).create_widgets()
		div = fw.Div(text = "<b><i>Contribution by region</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object7( self ):

		params = {'height':325, 'width':1000, 'default':self.max_day, 'columns':['portfolio', 'allocation', 'contribution'], 'formats':['na', '0.0%', '0.0%']}
		table, drop = fw.TableWithDropDown(self.df_risk_port, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Risk table by month / portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, table	


	def object8( self ):

		params = {'height':325, 'width':1000, 'barwidth':0.7, 'title':'', 'default':str(self.df_risk_port['yyyymmdd'].max())}
		plot, drop = fw.BarPlotWithDropDown(self.df_risk_port, 'portfolio', 'contribution', 'yyyymmdd', params, False).create_widgets()
		div = fw.Div(text = "<b><i>Contribution by portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object9( self ):

		params = {'height':550, 'width':1000, 'default':self.max_day, 'columns':['security', 'allocation', 'contribution'], 'formats':['na', '0.0%', '0.0%']}
		table, drop = fw.TableWithDropDown(self.df_risk_tick, 'yyyymmdd', params).create_widgets()			

		return drop, table	


	def object10( self ):

		params = {'height':350, 'width':1000, 'default':self.max_day, 'columns':['measure', 'p&l_%', 'p&l_amount'], 'formats':['na', '0.0%', '0,0']}	
		table, drop = fw.TableWithDropDown(self.df_risk_scnr, 'yyyymmdd', params).create_widgets()		
		div = fw.Div(text = "<b><i>Stress scenarios by day</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object11( self ):

		params = {'height':350, 'width':1000, 'title':'', 'default':'p&l_lehman_default_2008_p', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_risk_scnr, 'yyyymmdd', 'p&l_%', 'measure', params, True).create_widgets()
		div = fw.Div(text = "<b><i>Time series of P&L_%</i></b>", style = TITLE_STYLE)

		return div, drop, plot

	#################### CREATE PANEL

	def panel( self ):

		sec1 = fw.Div(text = "<h1>OVERALL</h1>", style = {'font-size':'100%', 'color':'black'})
		sec2 = fw.Div(text = "<h1>BY SECTOR</h1>", style = {'font-size':'100%', 'color':'black'})
		sec3 = fw.Div(text = "<h1>BY REGION</h1>", style = {'font-size':'100%', 'color':'black'})
		sec4 = fw.Div(text = "<h1>BY PORTFOLIO</h1>", style = {'font-size':'100%', 'color':'black'})
		sec5 = fw.Div(text = "<h1>TOP 20 - RISK CONTRIBUTORS</h1>", style = {'font-size':'100%', 'color':'black'})
		sec6 = fw.Div(text = "<h1>STRESS & SCENARIOS</h1>", style = {'font-size':'100%', 'color':'black'})	


		div1, drop1, table1 = self.object1()
		div2, drop2, plot2 = self.object2()
		div3, drop3, table3 = self.object3()
		div4, drop4, plot4 = self.object4()
		div5, drop5, table5 = self.object5()
		div6, drop6, plot6 = self.object6()
		div7, drop7, table7 = self.object7()
		div8, drop8, plot8 = self.object8()
		drop9, table9 = self.object9()
		div10, drop10, table10 = self.object10()
		div11, drop11, plot11 = self.object11()

		layout = fw.column(sec1, fw.row(fw.column(div1, drop1, table1), fw.column(div2, drop2, plot2)))
		layout = fw.column(layout, sec2, fw.row(fw.column(div3, drop3, table3), fw.column(div4, drop4, plot4)))
		layout = fw.column(layout, fw.column(sec3, fw.row(fw.column(div5, drop5, table5), fw.column(div6, drop6, plot6))))
		layout = fw.column(layout, fw.column(sec4, fw.row(fw.column(div7, drop7, table7), fw.column(div8, drop8, plot8))))
		layout = fw.column(layout, fw.column(sec5, drop9, table9))
		layout = fw.column(LOGO, layout, sec6, fw.row(fw.column(div10, drop10, table10), fw.column(div11, drop11, plot11)))
			
		return fw.Panel(child = layout, title = '3 - Investment Risk')

# ======================================================================
# TAB4
# ======================================================================

class Tab4( object ):

	#################### GET DATA

	df_perf_overall = pd.read_csv('data/equity_perf_overall.csv', dtype = {'yyyymmdd':'str'})
	df_perf_sec_reg_port = pd.read_csv('data/equity_perf_sec_reg_port.csv', dtype = {'yyyymmdd':'str'})	

	#################### SUBSET DATA

	df_perf_overall_sub1 = df_perf_overall[(df_perf_overall['gross_net'] == 'net') & (df_perf_overall['variable'] == 'TOTAL NET OF FEES')]
	df_perf_overall_sub2 = df_perf_overall[(df_perf_overall['gross_net'] == 'net') & (df_perf_overall['variable'].str.slice(0,4) == 'MSCI')]

	df_perf_sec = df_perf_sec_reg_port[df_perf_sec_reg_port['label'] == 'sector']
	df_perf_reg = df_perf_sec_reg_port[df_perf_sec_reg_port['label'] == 'region']
	df_perf_port = df_perf_sec_reg_port[df_perf_sec_reg_port['label'] == 'portfolio']	

	#################### SORT DATA

	df_perf_overall_sub1 = df_perf_overall_sub1.sort_values(by = 'yyyymmdd')
	df_perf_overall_sub2 = df_perf_overall_sub2.sort_values(by = 'yyyymmdd')
	df_perf_sec = df_perf_sec.sort_values(by = ['yyyymmdd', '%_end_weight'], ascending = [False, False])
	df_perf_reg = df_perf_reg.sort_values(by = ['yyyymmdd', '%_end_weight'], ascending = [False, False])
	df_perf_port = df_perf_port.sort_values(by = ['yyyymmdd', 'tot_rtn_ytd'], ascending = [False, False])	

	#################### COMMON OBJECTS

	columns = ['name', '%_end_weight', 'tot_rtn_mtd', 'tot_rtn_ytd']
	formats = ['na', '0.0%', '0.0%', '0.0%']	
	
	#################### CREATE OBJECTS

	def object1( self ):

		columns = ['structure','gross_net','variable','market_value','month','quarter_to_date','months_3','fiscal_ytd','ytd','year_1','year_3','itd']
		formats = ['na', 'na', 'na', '0,0', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%', '0.0%']

		params = {'height':800, 'width':1000, 'default':str(self.df_perf_overall['yyyymmdd'].max()), 'columns':columns, 'formats':formats}
		table, drop = fw.TableWithDropDown(self.df_perf_overall, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Performance table by month</i></b>", style = TITLE_STYLE)

		return div, drop, table		


	def object2( self ):	

		params = {'height':390, 'width':1000, 'title':'Total Net of Fees', 'default':'Global Equity Fund', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_perf_overall_sub1, 'yyyymmdd', 'month', 'structure', params, True).create_widgets()	

		div = fw.Div(text = "<b><i>Time series of performance by structure</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object3( self ):	

		params = {'height':390, 'width':1000, 'title':'MSCI Index', 'default':'Global Equity Fund', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_perf_overall_sub2, 'yyyymmdd', 'month', 'structure', params, True).create_widgets()	

		return drop, plot


	def object4( self ):

		params = {'height':350, 'width':1000, 'default':str(self.df_perf_sec['yyyymmdd'].max()), 'columns':self.columns, 'formats':self.formats}
		table, drop = fw.TableWithDropDown(self.df_perf_sec, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Performance table by month / sector</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object5( self ):

		params = {'height':350, 'width':1000, 'title':'', 'default':'Financials', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_perf_sec, 'yyyymmdd', 'tot_rtn_ytd', 'name', params, True).create_widgets()	
		div = fw.Div(text = "<b><i>Time series of YTD performance by sector</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object6( self ):

		params = {'height':350, 'width':1000, 'default':str(self.df_perf_reg['yyyymmdd'].max()), 'columns':self.columns, 'formats':self.formats}
		table, drop = fw.TableWithDropDown(self.df_perf_reg, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Performance table by month / region</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object7( self ):

		params = {'height':350, 'width':1000, 'title':'', 'default':'North America', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_perf_reg, 'yyyymmdd', 'tot_rtn_ytd', 'name', params, True).create_widgets()	
		div = fw.Div(text = "<b><i>Time series of YTD performance by region</i></b>", style = TITLE_STYLE)

		return div, drop, plot


	def object8( self ):

		params = {'height':325, 'width':1000, 'default':str(self.df_perf_port['yyyymmdd'].max()), 'columns':self.columns, 'formats':self.formats}
		table, drop = fw.TableWithDropDown(self.df_perf_port, 'yyyymmdd', params).create_widgets()	
		div = fw.Div(text = "<b><i>Performance table by month / portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, table


	def object9( self ):

		params = {'height':325, 'width':1000, 'title':'', 'default':'LPPI GLOBAL EQUITIES POOL [Aggregated Group]', 'percentage':True}
		plot, drop = fw.TimeSeriesPlotWithDropDown(self.df_perf_port, 'yyyymmdd', 'tot_rtn_ytd', 'name', params, True).create_widgets()	
		div = fw.Div(text = "<b><i>Time series of YTD performance by portfolio</i></b>", style = TITLE_STYLE)

		return div, drop, plot

	#################### CREATE PANEL

	def panel( self ):

		sec1 = fw.Div(text = "<h1>OVERALL</h1>", style = {'font-size':'100%', 'color':'black'})
		sec2 = fw.Div(text = "<h1>BY SECTOR</h1>", style = {'font-size':'100%', 'color':'black'})
		sec3 = fw.Div(text = "<h1>BY REGION</h1>", style = {'font-size':'100%', 'color':'black'})
		sec4 = fw.Div(text = "<h1>BY PORTFOLIO</h1>", style = {'font-size':'100%', 'color':'black'})

		div1, drop1, table1 = self.object1()
		div2, drop2, plot2 = self.object2()
		drop3, plot3 = self.object3()
		div4, drop4, table4 = self.object4()
		div5, drop5, plot5 = self.object5()
		div6, drop6, table6 = self.object6()
		div7, drop7, plot7 = self.object7()
		div8, drop8, table8 = self.object8()
		div9, drop9, plot9 = self.object9()

		layout = fw.column(sec1, fw.row(fw.column(div1, drop1, table1), fw.column(div2, drop2, plot2, drop3, plot3)))
		layout = fw.column(layout, fw.column(sec2, fw.row(fw.column(div4, drop4, table4), fw.column(div5, drop5, plot5))))
		layout = fw.column(layout, fw.column(sec3, fw.row(fw.column(div6, drop6, table6), fw.column(div7, drop7, plot7))))
		layout = fw.column(LOGO, layout, sec4, fw.row(fw.column(div8, drop8, table8), fw.column(div9, drop9, plot9)))
		
		return fw.Panel(child = layout, title = '4 - Performance')		

# ======================================================================
# TAB5
# ======================================================================

class Tab5( object ):

	def panel():

		sec = fw.Div(text = "<h1>tab5</h1>", style = {'font-size':'100%', 'color':'black'})
		return fw.Panel(child = sec, title = '5 - Risk Monitoring')		

# ======================================================================
# TAB6
# ======================================================================

class Tab6( object ):

	#################### GET DATA

	df_addan_fx = pd.read_csv('data/equity_addan_fx.csv', dtype = {'yyyymmdd':'str'})
	df_addan_top10_daily = pd.read_csv('data/equity_addan_top10_daily.csv')
	df_addan_top10_history = pd.read_csv('data/equity_addan_top10_history.csv', dtype = {'yyyymmdd':'str'})
	df_addan_top_stocks = pd.read_csv('data/equity_addan_top_stocks.csv', dtype = {'yyyymmdd':'str'})	

	#################### SUBSET DATA

	df_addan_fx_sub = df_addan_fx[df_addan_fx['to_ccy'].isin(['EUR', 'USD', 'AUD', 'NZD', 'CHF', 'CAD'])]
	df_addan_top_stocks_sub = df_addan_top_stocks.groupby('stock_name').tail(60)	

	#################### SORT DATA

	df_addan_top10_daily = df_addan_top10_daily.sort_values(by = ['portfolio_name', 'mkt_val_gbp'], ascending = [True, False])	
	df_addan_top10_history = df_addan_top10_history.sort_values(by = ['yyyymmdd', 'mkt_val_gbp'], ascending = [False, False])	
	df_addan_top_stocks = df_addan_top_stocks.sort_values(by = ['stock_name', 'yyyymmdd'], ascending = [True, False])	

	#################### COMMON OBJECTS

	max_day = str(df_addan_top10_history['yyyymmdd'].max())
	default_stock = df_addan_top10_daily[df_addan_top10_daily['portfolio_name'] == 'OVERALL'].reset_index(drop = True).iloc[0,1]

	#################### CREATE OBJECTS

	def object1( self ):

		params = {'height':400, 'width':1000, 'title':'', 'default':'USD', 'percentage':False}
		plot, dd = fw.TimeSeriesPlotWithDropDown(self.df_addan_fx, 'yyyymmdd', 'fx_rate', 'to_ccy', params, True).create_widgets()	
		div = fw.Div(text = "<b><i>FxRate vs GBP</i></b>", style = TITLE_STYLE)	

		return div, dd, plot


	def object2( self ):

		plot = fw.TimeSeriesPlot(self.df_addan_fx_sub, 'yyyymmdd', 'fx_rate', 'to_ccy', {'height':440, 'width':1000, 'title':'', 'percentage':False}, True).create_plot()
		div = fw.Div(text = "<b><i>FxRate (AUD-CAD-CHF-EUR-NZD-USD)</i></b>", style = TITLE_STYLE)		

		return div, plot


	def object3( self ):
		
		params = {'height':280, 'width':1000, 'default':'OVERALL', 'formats':['na', '0,0', '0,0', '0.0%'], 'columns':['security_name', 'positions', 'mkt_val_gbp', 'weight_in_total']}
		table, dd = fw.TableWithDropDown(self.df_addan_top10_daily, 'portfolio_name', params).create_widgets()	
		div = fw.Div(text = "<b><i>Top stocks by portfolio (data @ " + self.max_day + ")</i></b>", style = TITLE_STYLE)

		return div, dd, table


	def object4( self ):

		params = {'height':280, 'width':1000, 'default':self.max_day, 'formats':['na', '0,0', '0,0', '0.0%'], 'columns':['security_name', 'positions', 'mkt_val_gbp', 'weight_in_total']}
		table, dd = fw.TableWithDropDown(self.df_addan_top10_history, 'yyyymmdd', params).create_widgets()
		div = fw.Div(text = "<b><i>Top stocks timeseries (OVERALL portfolio)</i></b>", style = TITLE_STYLE)
		
		return div, dd, table		


	def object5( self ):

		params = {'height':400, 'width':1000, 'title':'', 'default':self.default_stock, 'percentage':False}
		plot, dd = fw.TimeSeriesPlotWithDropDown(self.df_addan_top_stocks, 'yyyymmdd', 'close', 'stock_name', params, True).create_widgets()
		div = fw.Div(text = "<b><i>Timeseries of Stock quotes</i></b>", style = TITLE_STYLE)

		return div, dd, plot


	def object6( self ):

		params = {'height':400, 'width':1000, 'title':'', 'default':self.default_stock, 'percentage':True}	
		plot, dd = fw.TimeSeriesPlotWithDropDown(self.df_addan_top_stocks_sub, 'yyyymmdd', 'per_change', 'stock_name', params, True).create_widgets()	
		div = fw.Div(text = "<b><i>Last 60 days volatility</i></b>", style = TITLE_STYLE)	

		return div, dd, plot

	#################### CREATE PANEL

	def panel( self ):

		sec1 = fw.Div(text = "<h1>FX RATES</h1>", style = {'font-size':'100%', 'color':'black'})
		sec2 = fw.Div(text = "<h1>TOP 10 STOCKS</h1>", style = {'font-size':'100%', 'color':'black'})
		sec3 = fw.Div(text = "<h1>STOCKS PERFORMANCE AND VOLATILITY </h1>", style = {'font-size':'100%', 'color':'black'})
		
		div1, dd1, plot1 = self.object1()
		div2, plot2 = self.object2()
		div3, dd3, table3 = self.object3()
		div4, dd4, table4 = self.object4()
		div5, dd5, table5 = self.object5()
		div6, dd6, table6 = self.object6()

		layout = fw.column(sec1, fw.row(fw.column(div1, dd1, plot1), fw.column(div2, plot2)))
		layout = fw.column(layout, sec2, fw.row(fw.column(div3, dd3, table3), fw.column(div4, dd4, table4)))
		layout = fw.column(layout, sec3, fw.row(fw.column(div5, dd5, table5), fw.column(div6, dd6, table6)))
		layout = fw.column(LOGO, layout)

		return fw.Panel(child = layout, title = '6 - Additional Analysis')			
	
# ======================================================================
# WRAP UP
# ======================================================================

tabs = fw.Tabs(tabs = [Tab1.panel(), Tab2().panel(), Tab3().panel(), Tab4().panel(), Tab5.panel(), Tab6().panel()])
fw.curdoc().add_root(tabs)