import pandas as pd
from bokeh.models import ColumnDataSource, GMapOptions,NumeralTickFormatter
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure


df = pd.read_csv('data/foreign_gross_data.csv')
output_file("html/stacked.html")


names = df['MovieName']
straight_of = df.loc[df['MovieName'] == 'Straight out of Compton']
countries = df['Country'].unique()
years = ['Straight out of Compton', 'Walk the Line', 'I Can Only Imagine']
colors = ["#c9d9d3", "#718dbf", "#e84d60"]

data = {'fruits': straight_of['Country'],
        'Straight out of Compton': straight_of['TotalGross'],
        'Walk the Line' : df.loc[df['MovieName'] == 'Walk the Line']['TotalGross'],
        'I Can Only Imagine': df.loc[df['MovieName'] == 'I Can Only Imagine']['TotalGross'],
        }

p = figure(x_range=countries, plot_height=1000, plot_width=1000, title="Foreign Performance: Total Gross",
           toolbar_location=None, tools="hover", tooltips="$name @fruits: @$name")

p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=data,
             legend=[value(x) for x in years])

p.y_range.start = 0
p.xaxis.major_label_orientation = "vertical"
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "vertical"
p.xaxis.major_label_orientation = "vertical"
p.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
show(p)
