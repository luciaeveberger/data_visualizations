# Biopic -> Music https://www.boxofficemojo.com/genres/chart/?id=musicbio.htm
import pandas as pd
from bokeh.io import export_png
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
from bokeh.models import NumeralTickFormatter, Span, BoxAnnotation
from bokeh.models import LinearColorMapper, LogTicker, ColorBar


df = pd.read_csv("data/genre_data.csv")
x = df['Date']

x_axis = list()
for val in x:
    val = val.split("/")
    x_axis.append(int(val[2]))
df['Date'] = x_axis


output_file("html/exercise3.html")
p = figure(title="Gross of Film by Year in Genre Biopic Music",
           plot_width=900,
           x_axis_label='year',
           y_axis_label='total gross',
           x_range=(1979,2019),
<<<<<<< HEAD
           tools="hover", tooltips="Straight out of Compton (2015): " + "$y{int}" + " $ million")
=======
           tools="hover", tooltips="@Title: $ @Gross:", )
>>>>>>> 461536739dea4da759de5dad1d5fdbec2de4c6b7

label = ['$0.00', '$200.00 m']

palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
           "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b",
           "#67001f"]

melting_points = df['Gross']
low = min(melting_points)
high = max(melting_points)
colors_inds = [int(10 * (x - low) / (high - low)) for x in melting_points]

#print(colors_inds)

df['melting_colors'] = [palette[i] for i in colors_inds]


<<<<<<< HEAD
#p.line(y=y, x=x_axis, legend="Weekly Gross (1989-1990)", line_width=2)
p.circle(x=x_axis, y=df['Gross'], fill_alpha=0.9, size=20, color=df['melting_colors'], legend='Weekly Gross in Million $')
p.legend.location = "top_left"

low_box = BoxAnnotation(top=50000000, fill_alpha=0.1, fill_color='red')
=======

# need to fix the legend
# creates the circle
p.circle(x='Date', y='Gross', fill_alpha=0.9, size=20, color='melting_colors', source=df, legend='melting_colors')
low_box = BoxAnnotation(top=50000000, fill_alpha=0.1, fill_color='red', )
>>>>>>> 461536739dea4da759de5dad1d5fdbec2de4c6b7

# use a formatter to display y-axis tick labels in million dollars
p.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
p.add_layout(low_box)
<<<<<<< HEAD

# add a colour map for y-axis
color_mapper = LinearColorMapper(palette=palette, low=0, high=200)
color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),label_standoff=12, border_line_color=None, location=(0,0))
p.add_layout(color_bar, 'right')

=======
p.title.align = 'center'
p.legend.location = "top_left"
>>>>>>> 461536739dea4da759de5dad1d5fdbec2de4c6b7
show(row(p))





