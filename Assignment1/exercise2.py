import pandas as pd
import math
from math import pi
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.io import export_png
from bokeh.models import Legend
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.transform import dodge
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

df = pd.read_csv("data/studio_data.csv")

output_file("html/ex2.html")


categories = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
sub_categories = ['2015', '2016', '2017']

sum_of_movies = sum(df['2005Movies'][:10])
df['2005Movies'] = df['2005Movies'][:10]

top_10 = df.head(10)
top_10['average_count_of_movies'] = (top_10['2005Movies']/ top_10['2005Movies'].sum())*100

data = {'fruits' : top_10['Distributor'],
        '2015' : top_10['MarketShare'],
        '2016' :  top_10['average_count_of_movies']}

source = ColumnDataSource(data=data)

p = figure(x_range=data['fruits'], plot_width=800,
           title="Studios Industry Market Share and Percent of Films Released of Top 10 Films (2005)",
           toolbar_location=None, tools="")


p.vbar(x=dodge('fruits', -0.25, range=p.x_range), top='2015', width=0.2, source=source,
       color="#c9d9d3", legend=value("Market Share (%)"))

p.vbar(x=dodge('fruits',  0.0,  range=p.x_range), top='2016', width=0.2, source=source,
       color="#718dbf", legend=value("Count of 2005 Films (%)"))


p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "vertical"
p.xaxis.major_label_orientation = math.pi/2
p.title.align = 'center'


data = df.head(10)
data['angle'] = data['MarketShare']/data['MarketShare'].sum() * 2*pi
data['color'] = Category20c[10]

data["legend"] = df['Distributor'].astype(str) + " (" + df['MarketShare'].astype(str) + "%)"

p_pie = figure(plot_width=800, title="2005 Distributor Market Share % -- top 10", toolbar_location=None,
           tools="hover", tooltips="@Distributor: @MarketShare", x_range=(-0.5, 1.0))


p_pie.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend="legend", source=data)

p_pie.title.align = 'center'
p_pie.axis.axis_label=None
p_pie.axis.visible=False
p_pie.grid.grid_line_color = None

show(column(p_pie, p))
export_png(p_pie, filename="submission/bubble_chart.png")
export_png(p, filename="submission/exercise2.png")