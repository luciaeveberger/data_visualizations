import pandas as pd
import math
from math import pi
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import row
from bokeh.transform import dodge
from bokeh.palettes import Category20c
from bokeh.plotting import figure
from bokeh.transform import cumsum

df = pd.read_csv("studio_data.csv")

output_file("ex2.html")


fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
years = ['2015', '2016', '2017']


sum_of_movies = sum(df['2005Movies'][:10])
print(sum_of_movies)

data = {'fruits' : df['Distributor'][:10],
        '2015' : df['MarketShare'][:10],
        '2016' :  df['2005Movies'][:10],
        }

source = ColumnDataSource(data=data)

p = figure(x_range=data['fruits'], plot_height=550, title="Top 10 - Industry Market Share vs. Count of Films released (2003)",
           toolbar_location=None, tools="")

p.vbar(x=dodge('fruits', -0.25, range=p.x_range), top='2015', width=0.2, source=source,
       color="#c9d9d3", legend=value("Market Share in %"))

p.vbar(x=dodge('fruits',  0.0,  range=p.x_range), top='2016', width=0.2, source=source,
       color="#718dbf", legend=value("Count of 2005 Films released"))


p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "vertical"
p.xaxis.major_label_orientation = math.pi/2



x = {
    'Warner Bros': 15,
    'United Kingdom': 93,
    'Japan': 89,
    'China': 63,
    'Germany': 44,
    'India': 42,
    'Italy': 40,
}

#data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})

data = df.head(10)
print(data)


data['angle'] = data['MarketShare']/data['MarketShare'].sum() * 2*pi
data['color'] = Category20c[10]

print(data)

p_pie = figure(plot_height=550, title="2003 Distributor Market Share % -- top 10", toolbar_location=None,
           tools="hover", tooltips="@Distributor: @MarketShare", x_range=(-0.5, 1.0))

p_pie.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='Distributor', source=data)

p_pie.axis.axis_label=None
p_pie.axis.visible=False
p_pie.grid.grid_line_color = None

show(row(p_pie, p))