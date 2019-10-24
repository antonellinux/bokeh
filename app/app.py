
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from bokeh.io import curdoc
from bokeh.client import push_session
from bokeh.models import ColumnDataSource, Panel, HoverTool, NumeralTickFormatter, CustomJS
from bokeh.models.widgets import TableColumn, DataTable, CheckboxGroup, Tabs, Select, Button
from bokeh.plotting import figure
from bokeh.palettes import Category20, Category20b, Category20c
from bokeh.layouts import column, row

l_colors = Category20[20] + Category20b[20] + Category20c[20] ### list with 60 different colors

# ======================================================================
# TABLE WITH DROPDOWN
# ======================================================================

class TableWithDropDown( object ):

	"""
	df_data = data frame with the data to be used for the table object	
	s_col_dd = colum of the data table to use for subsetting when the DropDown changes
	params = dictionary with width/height of the table
	"""

	def __init__( self, df_data, s_col_dd, params ):

		self.df_data = df_data		
		self.s_col_dd = s_col_dd		
		self.params = params


	def create_data_points( self, s_filter ):

		df = self.df_data[self.df_data[self.s_col_dd] == s_filter]
		return ColumnDataSource(df)


	def create_widgets( self ):

		def callback( attr, old, new ):
			
			o_source_sub = self.create_data_points(o_dd.value)						
			o_source.data = o_source_sub.data

		########## list with values

		l_dd_values = list(self.df_data[self.s_col_dd].unique())		

		########## create widget table

		o_cols = [TableColumn(field = i, title = i) for i in self.df_data.columns]				
		o_source = self.create_data_points(self.params['default'])
		o_table = DataTable(source = o_source, columns = o_cols, width = self.params['width'], height = self.params['height'])

		########## create dropdown

		o_dd = Select(value = self.params['default'], options = l_dd_values)
		o_dd.on_change('value', callback)						

		return o_table, o_dd

# ======================================================================
# CLASS CREATE TABS
# ======================================================================

def create_tab():

	#df = pd.read_csv('data.csv', dtype={'yyyymm':'str', 'yyyymmdd':'str'})
	d = {'yyyymm': ['201910','201910'], 'yyyymmdd': ['20191022','20191023'], 'nbr_tables':[6,6], 'nbr_rows':[3020,3071]}
	df = pd.DataFrame(data=d)
	
	o_tbl, o_chk = TableWithDropDown(df, 'yyyymm', {'height':400, 'width':800, 'default':'201910'}).create_widgets()	
	o_layout = column(o_chk, o_tbl)
	o_tab = Panel(child = o_layout, title = 'Staging Summary')		

	return o_tab


o_tab = create_tab()
o_tabs = Tabs(tabs = [o_tab])
curdoc().add_root(o_tabs)
