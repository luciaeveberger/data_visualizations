# Biopic -> Music https://www.boxofficemojo.com/genres/chart/?id=musicbio.htm
import pandas as pd
from datetime import datetime
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
from bokeh.models import NumeralTickFormatter, Span, BoxAnnotation

df = pd.read_csv("genre_data.csv")
# print(df['Date'])
x = df['Date']
y = df['Gross']
print(y)
x_axis = list()
for val in x:
    val = val.split("/")
    x_axis.append(int(val[2]))
print(x_axis)


output_file("html/exercise3.html")
p = figure(title="Gross of Film by Year in Genre Biopic -> Music",
           plot_width=800,
           x_axis_label='year',
           y_axis_label='total gross',
           x_range=(1979,2019),
           tools="hover", tooltips="Straight out of Compton (2015) ")


palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
           "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b",
           "#67001f"]

melting_points = df['Gross']
low = min(melting_points)
high = max(melting_points)
colors_inds = [int(10 * (x - low) / (high - low)) for x in melting_points] #gives items in colors a value from 0-10
df['melting_colors'] = [palette[i] for i in colors_inds]


#p.line(y=y, x=x_axis, legend="Weekly Gross (1989-1990)", line_width=2)
p.circle(x=x_axis, y=df['Gross'], fill_alpha=0.9, size=20, color=df['melting_colors'])
low_box = BoxAnnotation(top=50000000, fill_alpha=0.1, fill_color='red')

# use a formatter to display y-axis tick labels in million dollars
p.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")
p.add_layout(low_box)
show(row(p))




