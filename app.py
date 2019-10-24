
# ======================================================================
# IMPORT MODULES
# ======================================================================

import pandas as pd
from __flowers__ import *

# ======================================================================
# CLASS CREATE TABS
# ======================================================================

def create_tab():

	df = pd.read_csv(r'\\lpfa-lon-fs-01\Users\antonello.briglia\Desktop\github\data.csv', dtype={'yyyymm':'str', 'yyyymmdd':'str'})
	
	o_tbl, o_chk = TableWithDropDown(df, 'yyyymm', {'height':400, 'width':800, 'default':'201910'}).create_widgets()	
	o_layout = column(o_chk, o_tbl)
	o_tab = Panel(child = o_layout, title = 'Staging Summary')		

	return o_tab


o_tab = create_tab()
o_tabs = Tabs(tabs = [o_tab])
curdoc().add_root(o_tabs)
