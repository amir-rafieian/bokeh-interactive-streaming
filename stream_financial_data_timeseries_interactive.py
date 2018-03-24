# =============================================================================
# importing libraries
# =============================================================================
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource,Range1d,DatetimeTickFormatter,Select
from random import randrange
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
from bokeh.layouts import layout

#import pytz
#from pytz import timezone
from math import radians



# =============================================================================
# Webscrapping to extract value
# pip install beautifulsoup4
# =============================================================================
def extract_value(market_name='bitstampUSD'):
    r = requests.get("https://bitcoincharts.com/markets/"+market_name+".html",headers={'User-Agent':"Mozilla/5.0"})
    c = r.content    
    soup = BS(c,"html.parser")
    soup.clear
    value_raw = soup.find_all("span")
    value_net = value_raw[1]
    value_net = float(value_net.text) #float(value_net.span.text.replace("$","").replace(",",""))
    return value_net


# =============================================================================
# Plotting
# =============================================================================
f = figure(x_axis_type='datetime')
f.plot_width= 1100 #pixels


source = ColumnDataSource (dict(x=[],y=[])) 

#Create Glyphs
f.circle(x='x',y='y',source=source,color='olive',line_color='brown')
f.line(x='x',y='y',source=source,line_color='blue')


#To get all the timezones
#for tz in pytz.all_timezones:
#    print (tz)

def update():
    new_data = dict(x=[datetime.now()],y=[extract_value(select.value)])
    source.stream(new_data,rollover=200) #we keep last 200 glyphs on the plot only
    print(source.data)

#Format the x-ticks to show datetime properly
#https://bokeh.pydata.org/en/latest/docs/reference/models/formatters.html
f.xaxis.formatter = DatetimeTickFormatter(seconds=['%Y-%m-%d %H:%M:%S'],
                                          minsec=['%Y-%m-%d %H:%M:%S'],
                                          minutes=['%Y-%m-%d %H:%M:%S'],
                                          hourmin=['%Y-%m-%d %H:%M:%S'],
                                          hours=['%Y-%m-%d %H:%M:%S'],
                                          days=['%Y-%m-%d %H:%M:%S'],
                                          months=['%Y-%m-%d %H:%M:%S'],
                                          years=['%Y-%m-%d %H:%M:%S'])

#Rotate the x-labels
f.xaxis.major_label_orientation = radians(90) #Have to enter in radians


# =============================================================================
# Create Select Widget
# =============================================================================
def update_market_name(attr, old, new):
    source.data = dict(x=[],y=[]) #Remove the data from previous selection
    update()
    
options = [("bitstampUSD","Bitstamp"),("krakenUSD","Kraken")]
#Create the Select widget
select=Select(title="Market Name", options=options,value = "bitstampUSD") #Value is the initial value
select.on_change("value",update_market_name)

# Set The Layouts for Widgets
lay_out=layout([[select]])

# =============================================================================
# Run the Server
# =============================================================================
curdoc().add_root(f)
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update,5000) #call the function every 5000ms


#Enter this command in commandline:
#python -m bokeh serve widgets_bokeh_server.py
#or:
#bokeh serve categorical_axis_select_widgets.py
#or:
#bokeh serve widgets_bokeh_server.py --port 5007