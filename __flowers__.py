
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from bokeh.io import curdoc
from bokeh.client import push_session
from bokeh.models import ColumnDataSource, Panel, HoverTool, NumeralTickFormatter, CustomJS
from bokeh.models.widgets import TableColumn, DataTable, CheckboxGroup, Tabs, Select, Button, Div
from bokeh.plotting import figure
from bokeh.palettes import Category20, Category20b, Category20c
from bokeh.layouts import column, row

l_colors = Category20[20] + Category20b[20] + Category20c[20] ### list with 60 different colors

# ======================================================================
# TABLE WITH CHECKGROUP
# ======================================================================

class TableWithCheckGroup( object ):

	"""
	df_data = data frame with the data to be used for the table object	
	s_col_check_grp = colum of the data table to use for subsetting when the Checkbox changes
	params = dictionary with width and height of the table widget
	"""

	def __init__( self, df_data, s_col_check_grp, params ):

		self.df_data = df_data		
		self.s_col_check_grp = s_col_check_grp		
		self.params = params

	def create_data_points( self, l_sub_values ):

		########## create empty data frame

		df = pd.DataFrame(columns = list(self.df_data.columns))

		##########  append data to empty data frame
		
		for i in l_sub_values:			
			df = df.append(self.df_data[self.df_data[self.s_col_check_grp] == i])

		return df


	def create_widgets( self ):

		def callback( attr, old, new ):

			l_values = [o_wdg_check.labels[i] for i in o_wdg_check.active]			
			o_source_sub = ColumnDataSource(self.create_data_points(l_values))			
			o_source.data = o_source_sub.data

		########## list with values

		l_chkgrp_values = list(self.df_data[self.s_col_check_grp].unique())

		########## create widget table

		o_cols = [TableColumn(field = i, title = i) for i in self.df_data.columns]				
		o_source = ColumnDataSource(self.create_data_points(l_chkgrp_values))
		o_wdg_table = DataTable(source = o_source, columns = o_cols, width = self.params['width'], height = self.params['height'])

		##### create widget checkbox

		o_wdg_check = CheckboxGroup(labels = l_chkgrp_values)		
		o_wdg_check.on_change('active', callback)

		return o_wdg_table, o_wdg_check

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
# TIMESERIES PLOT WITH CHECKGROUP
# ======================================================================

class TimeSeriesPlotWithCheckGroup( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_time = name of the column with the time values 
	s_col_values = name of the column with values to plot
	s_col_labels = name of the column with labels used by the CheckGroup for subsetting
	params = dictionary with width/height/title of the plot
	b_yyyymmdd_to_time = True when the time column appears with format yyyymmdd	
	"""

	def __init__( self, df_data, s_col_time, s_col_values, s_col_labels, params, b_yyyymmdd_to_time = False ):

		self.df_data = df_data
		self.s_col_time = s_col_time		
		self.s_col_values = s_col_values
		self.s_col_labels = s_col_labels
		self.params = params
		self.b_yyyymmdd_to_time = b_yyyymmdd_to_time


	def create_data_points( self, df_data ):

		########## create l_values

		df_tmp = df_data.pivot(index = self.s_col_time, columns = self.s_col_labels, values = self.s_col_values)
		l_values = df_tmp.values.T.tolist()

		########## create l_time

		df_tmp = pd.DataFrame(df_data[self.s_col_time].unique())
		df_tmp.columns = [self.s_col_time]

		if self.b_yyyymmdd_to_time == True:
			df_tmp[self.s_col_time] = pd.to_datetime(df_tmp[self.s_col_time])		

		l_time = list(df_tmp.T.values) * len(l_values)

		########## create l_labels

		l_labels = list(df_data[self.s_col_labels].unique())

		return l_values, l_time, l_labels
		

	def create_widgets( self ):			

		def callback( attr, old, new ):

			l_active = [o_wdg_check.labels[i] for i in o_wdg_check.active]			
			df_sub_data = self.df_data[self.df_data[self.s_col_labels].isin(l_active)]
			l_values, l_time, l_labels = self.create_data_points(df_sub_data)
			o_source.data = {'x': l_time, 'y': l_values, 'labels':l_labels, 'mypal':l_colors[0:len(l_values)]}

		########## get data points

		l_values, l_time, l_labels = self.create_data_points(self.df_data)

		########## create widget plot

		o_source = ColumnDataSource(data = {'x': l_time, 'y': l_values, 'labels':l_labels, 'mypal':l_colors[0:len(l_values)]})		
		TOOLTIPS = [("item", "@labels"), ("value", "$y")]		
		o_wdg_plot = figure(width = self.params['width'], height = self.params['height'], x_axis_type = 'datetime', y_axis_type = 'linear', tooltips = TOOLTIPS, toolbar_location = None, title = self.params['title'])			
		o_wdg_plot.multi_line('x', 'y', source = o_source, line_width = 2, line_color = 'mypal', legend = 'labels')

		########## create widget checkbox 

		o_wdg_check = CheckboxGroup(labels = l_labels)
		o_wdg_check.on_change('active', callback)

		return o_wdg_plot, o_wdg_check


# ======================================================================
# TIMESERIES PLOT WITH DROPDOWN
# ======================================================================

class TimeSeriesPlotWithDropDown( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_time = name of the column with the time values 
	s_col_values = name of the column with values to plot
	s_col_labels = name of the column with labels used by the CheckGroup for subsetting
	params = dictionary with width/height/title/default value of the plot
	b_yyyymmdd_to_time = True when the time column appears with format yyyymmdd	
	"""

	def __init__( self, df_data, s_col_time, s_col_values, s_col_labels, params, b_yyyymmdd_to_time=False ):

		self.df_data = df_data
		self.s_col_time = s_col_time		
		self.s_col_values = s_col_values
		self.s_col_labels = s_col_labels
		self.params = params
		self.b_yyyymmdd_to_time = b_yyyymmdd_to_time
		

	def create_widgets( self ):			

		def callback( attr, old, new ):

			df_sub_data = self.df_data[self.df_data[self.s_col_labels] == o_dd.value]						
			o_source_sub = ColumnDataSource(df_sub_data)
			o_source.data = o_source_sub.data						

		########## create plot

		if self.b_yyyymmdd_to_time == True:			
			self.df_data[self.s_col_time] = pd.to_datetime(self.df_data[self.s_col_time])

		df_start = self.df_data[self.df_data[self.s_col_labels] == self.params['default']]
		o_source = ColumnDataSource(df_start)

		TOOLTIPS = [("value", "$y")]
		o_plot = figure(x_axis_type='datetime', width=self.params['width'], height=self.params['height'], title=self.params['title'], tooltips=TOOLTIPS, toolbar_location=None)
		o_plot.line(x=self.s_col_time, y=self.s_col_values, source=o_source)
		o_plot.ygrid.grid_line_color = None

		########## create dropdown

		l_labels = list(self.df_data[self.s_col_labels].unique()) 		
		o_dd = Select(value=self.params['default'], options=l_labels)
		o_dd.on_change('value', callback)	

		return o_plot, o_dd

# ======================================================================
# TIMESERIES PLOT (AND NOTHING ELSE)
# ======================================================================		

class TimeSeriesPlot( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_time = name of the column with the time values 
	s_col_values = name of the column with values to plot
	s_col_labels = name of the column with the labels 	
	params = dictionary with width/height/title of the plot
	b_yyyymmdd_to_time = True when the time column appears with format yyyymmdd	
	"""

	def __init__( self, df_data, s_col_time, s_col_values, s_col_labels, params, b_yyyymmdd_to_time = False ):

		self.df_data = df_data
		self.s_col_time = s_col_time		
		self.s_col_values = s_col_values
		self.s_col_labels = s_col_labels
		self.params = params
		self.b_yyyymmdd_to_time = b_yyyymmdd_to_time


	def create_data_points( self ):

		########## create l_values

		df_tmp = self.df_data.pivot(index = self.s_col_time, columns = self.s_col_labels, values = self.s_col_values)
		l_values = df_tmp.values.T.tolist()

		########## create l_time

		df_tmp = pd.DataFrame(self.df_data[self.s_col_time].unique())
		df_tmp.columns = [self.s_col_time]

		if self.b_yyyymmdd_to_time == True:
			df_tmp[self.s_col_time] = pd.to_datetime(df_tmp[self.s_col_time])		

		l_time = list(df_tmp.T.values) * len(l_values)

		########## create l_labels

		l_labels = list(self.df_data[self.s_col_labels].unique())

		return l_values, l_time, l_labels


	def create_plot( self ):

		########## get data points

		l_values, l_time, l_labels = self.create_data_points()

		########## create widget plot

		o_source = ColumnDataSource(data = {'x': l_time, 'y': l_values, 'labels':l_labels, 'mypal':l_colors[0:len(l_values)]})		
		TOOLTIPS = [("item", "@labels"), ("value", "$y")]		
		o_wdg_plot = figure(width = self.params['width'], height = self.params['height'], x_axis_type = 'datetime', y_axis_type = 'linear', tooltips = TOOLTIPS, toolbar_location = None, title = self.params['title'])			
		o_wdg_plot.multi_line('x', 'y', source = o_source, line_width = 2, line_color = 'mypal')#, legend = 'labels')
		o_wdg_plot.ygrid.grid_line_color = None
		
		return o_wdg_plot

# ======================================================================
# PIE CHART (AND NOTHING ELSE)
# ======================================================================		

class PieChart( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_label = name of the column with the labels 
	s_col_values = name of the column with values 	
	params = dictionary with width/height/radius/title of the pie chart
	"""

	def __init__( self, df_data, s_col_label, s_col_values, params ):

		self.df_data = df_data
		self.s_col_label = s_col_label
		self.s_col_values = s_col_values
		self.params = params


	def create_plot( self ):

		from math import pi
		from bokeh.transform import cumsum

		########## update data frame

		df = self.df_data.copy()
		df['angle'] = df[self.s_col_values] / df[self.s_col_values].sum() * 2*pi
		df['color'] = l_colors[0:df.shape[0]]

		########## create pie chart
		
		TOOLS = "@" + self.s_col_label + ": @" + self.s_col_values
		o_plot = figure(width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, x_range = (-0.5, 1.0), tooltips = TOOLS, title = self.params['title'])
		o_plot.wedge(x = 0, y = 1, radius = self.params['radius'], start_angle = cumsum('angle', include_zero = True), 
					end_angle = cumsum('angle'), line_color = 'white', 
					fill_color = 'color', legend = self.s_col_label, source = df)

		o_plot.axis.axis_label = None
		o_plot.axis.visible = None
		o_plot.grid.grid_line_color = None

		return o_plot

# ======================================================================
# BARPLOT (AND NOTHING ELSE)
# ======================================================================		

class BarPlot( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_label = name of the column with the labels 
	s_col_values = name of the column with values 
	params = dictionary with width/height/barwidth/title of the pie chart
	b_vbar = True for vertical bars and False for horizontal bars
	"""

	def __init__( self, df_data, s_col_label, s_col_values, params = None, b_vbar = True):

		self.df_data = df_data
		self.s_col_label = s_col_label
		self.s_col_values = s_col_values
		self.b_vbar = b_vbar

		if params == None:
			self.params = {'height':400, 'width':800, 'barwidth':0.5, 'title':''}
		else:
			self.params = params

	def create_plot( self ):

		########## manage df

		df = self.df_data.copy()		
		df.sort_values(by = self.s_col_values, ascending = False, inplace = True)

		########## create source

		l_labels = list(df[self.s_col_label])
		l_values = list(df[self.s_col_values])
		o_source = ColumnDataSource(dict(labels = l_labels, values = l_values, colors = l_colors[0:len(l_labels)]))

		########## create plot

		TOOLTIPS = [("item", "@labels"), ("value", "@values{0.0%}")]

		if self.b_vbar == True:

			o_plot = figure(x_range = l_labels, plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'], tooltips = TOOLTIPS)
			o_plot.vbar(x = 'labels', top = 'values', width = self.params['barwidth'], color = 'colors', source = o_source)
			o_plot.yaxis[0].formatter = NumeralTickFormatter(format="0%")

			o_plot.y_range.start = 0
			o_plot.y_range.end = 1
			o_plot.xgrid.grid_line_color = None
			o_plot.yaxis[0].formatter = NumeralTickFormatter(format="0%")

		else:

			o_plot = figure(y_range = l_labels, plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'], tooltips = TOOLTIPS)
			o_plot.hbar(y = 'labels', right = 'values', height = self.params['barwidth'], color = 'colors', source = o_source)

			o_plot.x_range.start = 0
			o_plot.x_range.end = 1
			o_plot.ygrid.grid_line_color = None
			o_plot.xaxis[0].formatter = NumeralTickFormatter(format="0%")

		return o_plot

# ======================================================================
# PIE CHART WITH SELECT WIDGET
# ======================================================================		

class PieChartWithSelect( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_label = name of the column with the labels 
	s_col_values = name of the column with values 	
	params = dictionary with width/height/radius/title of the pie chart
	"""
	from math import pi
	from bokeh.transform import cumsum

	def __init__( self, df_data, s_col_label, s_col_values, params ):

		self.df_data = df_data
		self.s_col_label = s_col_label
		self.s_col_values = s_col_values
		self.params = params


	def create_data_points( self, df ):

		########## update data frame

		df = df.copy()
		df['angle'] = df[self.s_col_values] / df[self.s_col_values].sum() * (2 * self.pi)
		df['color'] = l_colors[0:df.shape[0]]
		
		########## create source object			

		# return ColumnDataSource(data = dict(start = self.cumsum(df['angle']), end = self.cumsum(df['angle']), color = df['color']))
		return ColumnDataSource(data = dict(values = df['angle'], color = df['color']))


	def create_widgets( self ):

		########## create pie chart

		o_source = self.create_data_points(self.df_data)
		
		TOOLS = "@" + self.s_col_label + ": @" + self.s_col_values
		o_plot = figure(plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, x_range = (-0.5, 1.0), tooltips = TOOLS, title = self.params['title'])		
		o_plot.wedge(x = 0, y = 1, radius = self.params['radius'], start_angle = self.cumsum('values', include_zero = True), end_angle = self.cumsum('values'), line_color = 'white', fill_color = 'color', legend = self.s_col_label, source = o_source)

		return o_plot

# ======================================================================
# BARPLOT WITH DROPDOWN
# ======================================================================		

class BarPlotWithDropDown( object ):

	"""
	df_data = data frame with the data for building the plot
	s_col_label = name of the column with the labels 
	s_col_values = name of the column with values 
	s_col_filter = name of the column with dropdown filter
	params = dictionary with width/height/barwidth/title/default of the pie chart
	b_vbar = True for vertical bars and False for horizontal bars
	"""

	def __init__( self, df_data, s_col_label, s_col_values, s_col_filter, params, b_vbar = True):

		self.df_data = df_data
		self.s_col_label = s_col_label
		self.s_col_values = s_col_values
		self.s_col_filter = s_col_filter
		self.params = params
		self.b_vbar = b_vbar

	def create_data_points( self, df ):

		########## manage df

		df = df.copy()
		s_filter_val = list(df[self.s_col_filter].unique())[0]				
		df = df[df[self.s_col_filter] == s_filter_val] 
		df.sort_values(by = self.s_col_values, ascending = False, inplace = True)				

		########## create source
		
		l_labels = list(df[self.s_col_label])
		l_values = list(df[self.s_col_values])
		
		return ColumnDataSource(dict(labels = l_labels, values = l_values, colors = l_colors[0:len(l_labels)]))


	def create_widgets( self ):

		def callback( attr, old, new ):			

			df_sub_data = self.df_data[self.df_data[self.s_col_filter] == o_sel.value]						
			o_source_sub = self.create_data_points(df_sub_data)			
			o_source.data = o_source_sub.data

		########## create source

		l_sel_options = list(self.df_data[self.s_col_filter].unique())
		l_all_labels = list(self.df_data[self.s_col_label].unique())
		o_source = self.create_data_points(self.df_data[self.df_data[self.s_col_filter] == self.params['default']])		

		########## create plot

		TOOLTIPS = [("item", "@labels"), ("value", "@values{0.0%}")]

		if self.b_vbar == True:

			o_plot = figure(x_range = l_all_labels, plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'], tooltips = TOOLTIPS)
			o_plot.vbar(x = 'labels', top = 'values', width = self.params['barwidth'], color = 'colors', source = o_source)				
			o_plot.yaxis[0].formatter = NumeralTickFormatter(format="0%")

			o_plot.y_range.start = 0
			o_plot.y_range.end = 1						
			o_plot.xgrid.grid_line_color = None
			o_plot.yaxis[0].formatter = NumeralTickFormatter(format="0%")

		else:

			o_plot = figure(y_range = l_all_labels, plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'], tooltips = TOOLTIPS)
			o_plot.hbar(y = 'labels', right = 'values', height = self.params['barwidth'], color = 'colors', source = o_source)		

			o_plot.x_range.start = 0		
			o_plot.x_range.end = 1
			o_plot.ygrid.grid_line_color = None			
			o_plot.xaxis[0].formatter = NumeralTickFormatter(format="0%")		

		########## create dropdown widget

		o_sel = Select(value = self.params['default'], options = l_sel_options)
		o_sel.on_change('value', callback)

		return o_plot, o_sel		

# ======================================================================
# MULTI BARPLOT 
# ======================================================================		

class MultiBarPlot( object ):

	"""
	df_data = data frame with the data for building the plot
	l_label_cols = list with the name of the 2 columns to be used as labels of the multibar plot 
	s_col_values = name of the column with values 	
	params = dictionary with width/height/barwidth/title of the pie chart
	b_vbar = True for vertical bars and False for horizontal bars
	"""

	def __init__( self, df_data, l_label_cols, s_col_values, params, b_vbar = True ):

		self.df_data = df_data
		self.l_label_cols = l_label_cols
		self.s_col_values = s_col_values
		self.params = params
		self.b_vbar = b_vbar


	def create_data_points( self ):

		x1 = list(self.df_data[self.l_label_cols[0]].unique())
		x2 = list(self.df_data[self.l_label_cols[1]].unique())
		colors = l_colors[0:len(x2)] * len(x1)

		x = [(i1, i2) for i1 in x1 for i2 in x2]
		count = []
		
		for i in range(len(x)):
			
			s_filter = self.l_label_cols[0] + " == '" + x[i][0] + "' & " + self.l_label_cols[1] + " == '" + x[i][1] + "'"
						
			try:
				df = self.df_data.query(s_filter)	
				count.append(df[self.s_col_values].iloc[0])
				
			except:
				count.append(0)		

		return x, count, colors
		
		
	def create_plot( self ):

		from bokeh.models import FactorRange

		########## create source
		
		x, count, colors = self.create_data_points()
		o_source = ColumnDataSource(dict(x = x, count = count, colors = colors))

		########## create plot

		if self.b_vbar == True:

			o_plot = figure(x_range = FactorRange(*x), plot_height = self.params['height'], plot_width = self.params['width'], title = self.params['title'], toolbar_location = None)
			o_plot.vbar(x = 'x', top = 'count', width = self.params['barwidth'], color = 'colors', source = o_source)

			o_plot.y_range.start = 0
			o_plot.x_range.range_padding = 0.1
			o_plot.xaxis.major_label_orientation = 1		
			o_plot.xgrid.grid_line_color = None

		else:

			o_plot = figure(y_range = FactorRange(*x), plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'])
			o_plot.hbar(y = 'x', right = 'count', height = self.params['barwidth'], color = 'colors', source = o_source)	

			o_plot.x_range.start = 0		
			o_plot.ygrid.grid_line_color = None					

		return o_plot

# ======================================================================
# MULTI BARPLOT WITH DROPDOWN
# ======================================================================		

class MultiBarPlotWithDropDown( object ):

	"""
	df_data = data frame with the data for building the plot
	l_label_cols = list with the name of the 2 columns to be used as labels of the multibar plot 
	s_col_values = name of the column with values 	
	s_col_filter = name of the column with dropdown filter
	params = dictionary with width/height/barwidth/title/default of the bar chart
	b_vbar = True for vertical bars and False for horizontal bars
	"""

	def __init__( self, df_data, l_label_cols, s_col_values, s_col_filter, params, b_vbar = True ):

		self.df_data = df_data
		self.l_label_cols = l_label_cols
		self.s_col_values = s_col_values
		self.s_col_filter = s_col_filter
		self.params = params
		self.b_vbar = b_vbar


	def create_data_points( self, df ):

		########## manage df

		df = df.copy()
		s_filter_val = list(df[self.s_col_filter].unique())[0]				
		df = df[df[self.s_col_filter] == s_filter_val] 

		########## create lists with label 

		x1 = list(df[self.l_label_cols[0]].unique())
		x2 = list(df[self.l_label_cols[1]].unique())
		colors = l_colors[0:len(x2)] * len(x1)

		x = [(i1, i2) for i1 in x1 for i2 in x2]
		count = []
		
		########## create list with values

		for i in range(len(x)):
			
			s_filter = self.l_label_cols[0] + " == '" + x[i][0] + "' & " + self.l_label_cols[1] + " == '" + x[i][1] + "'"
						
			try:
				df_tmp = df.query(s_filter)	
				count.append(df_tmp[self.s_col_values].iloc[0])
				
			except:
				count.append(0)		

		return x, count, colors


	def create_widgets( self ):

		from bokeh.models import FactorRange

		def callback( attr, old, new ):

			df_sub_data = self.df_data[self.df_data[self.s_col_filter] == o_dd.value]
			x, count, colors = self.create_data_points(df_sub_data)
			o_source_sub = 	ColumnDataSource(dict(x = x, count = count, colors = colors))
			o_source.data = o_source_sub.data

		########## create source

		x, count, colors = self.create_data_points(self.df_data[self.df_data[self.s_col_filter] == self.params['default']])
		l_dd_values = list(self.df_data[self.s_col_filter].unique())
		o_source = ColumnDataSource(dict(x = x, count = count, colors = colors))

		########## create plot

		TOOLTIPS = [("item", "@x"), ("value", "@count{0.0%}")]

		if self.b_vbar == True:

			o_plot = figure(x_range = FactorRange(*x), plot_height = self.params['height'], plot_width = self.params['width'], title = self.params['title'], toolbar_location = None, tooltips = TOOLTIPS)
			o_plot.vbar(x = 'x', top = 'count', width = self.params['barwidth'], color = 'colors', source = o_source)

			o_plot.y_range.start = 0
			o_plot.y_range.end = 1
			o_plot.x_range.range_padding = 0.1
			o_plot.xaxis.major_label_orientation = 1		
			o_plot.xgrid.grid_line_color = None
			o_plot.yaxis[0].formatter = NumeralTickFormatter(format="0%")

		else:

			o_plot = figure(y_range = FactorRange(*x), plot_width = self.params['width'], plot_height = self.params['height'], toolbar_location = None, title = self.params['title'], tooltips = TOOLTIPS)
			o_plot.hbar(y = 'x', right = 'count', height = self.params['barwidth'], color = 'colors', source = o_source)	

			o_plot.x_range.start = 0		
			o_plot.x_range.end = 1
			o_plot.ygrid.grid_line_color = None			
			o_plot.xaxis[0].formatter = NumeralTickFormatter(format="0%")

		########## create dropdown widget

		o_dd = Select(value = self.params['default'], options = l_dd_values)
		o_dd.on_change('value', callback)

		return o_plot, o_dd

# ======================================================================
# EXPORT DATA BUTTON
# ======================================================================

class ExportDataButton( object ):

	def __init__( self, df_data, s_btn_label, s_file_name ):

		self.df_data = df_data
		self.s_btn_label = s_btn_label
		self.s_file_name = s_file_name

	def create_button( self ):

		s_java_script = """
						function table_to_csv(source) {
						    const columns = Object.keys(source.data)
						    const nrows = source.get_length()
						    const lines = [columns.join(',')]

						    for (let i = 0; i < nrows; i++) {
						        let row = [];
						        for (let j = 0; j < columns.length; j++) {
						            const column = columns[j]
						            row.push(source.data[column][i].toString())
						        }
						        lines.push(row.join(','))
						    }
						    return lines.join('\\n').concat('\\n')
						}


						const filename = 'XXXXXX'
						filetext = table_to_csv(source)
						const blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' })

						//addresses IE
						if (navigator.msSaveBlob) {
						    navigator.msSaveBlob(blob, filename)
						} else {
						    const link = document.createElement('a')
						    link.href = URL.createObjectURL(blob)
						    link.download = filename
						    link.target = '_blank'
						    link.style.visibility = 'hidden'
						    link.dispatchEvent(new MouseEvent('click'))
						}
		"""

		s_java_script = s_java_script.replace('XXXXXX', self.s_file_name)

		source = ColumnDataSource(self.df_data)
		o_btn = Button(label = self.s_btn_label, button_type = "success")		
		o_btn.callback = CustomJS(args = dict(source = source), code = s_java_script)
		# o_btn.js_on_click(CustomJS(args = dict(source = source), code = s_java_script))

		return o_btn
