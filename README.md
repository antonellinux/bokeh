# bokeh

flowers.py provides a framework written on top of Bokeh which allows the creation of interactive objects within 1 single method.
This example shows how simple can be, creating a BarPlot object that refreshes when the value of a dropdown is changed:

params = {'height':370, 'width':800, 'barwidth':0.7, 'title':'Region weight (data @: ' + s_max_day + ')', 'default':'OVERALL'}
o_plot, o_drop = BarPlotWithDropDown(df1, 'region', 'weight', 'portfolio_name', params, False).create_widgets()
