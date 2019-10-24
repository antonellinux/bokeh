
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from __flowers__ import *

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
