from datetime import datetime

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row
from bokeh.models import NumeralTickFormatter, Span, BoxAnnotation
import pandas as pd

# look whos talking https://www.boxofficemojo.com/movies/?page=weekly&id=lookwhostalking.htm

df = pd.read_csv("data/data.csv")
print(df['Gross'])

x = [
datetime(89,10,13),
datetime(89,10,20),
datetime(89,10,27),

datetime(89,11,3),
datetime(89,11,10),
datetime(89,11,17),
datetime(89,11,24),

datetime(89,12,1),
datetime(89,12,8),
datetime(89,12,15),
datetime(89,12,22),
datetime(89,12,29),

datetime(90,1,5),
datetime(90,1,12),
datetime(90,1,19),
datetime(90,1,26),
datetime(90,2,2),
datetime(90,2,9),
datetime(90,2,15),
]


y = df['Gross']

y_rank = df['RankWeekly']

# output to static HTML file
output_file("filmgross.html")

# create a new plot with a title and axis labels
p = figure(title="Weekly Gross ($) of Look Who's Talking (1989-1990)",
            plot_width=500,
            x_axis_label='date',
            y_axis_label='weekly gross',
            x_axis_type="datetime")

rank_chart = figure(title="Weekly Rank (1-20) of Look Who's Talking (1989-1990)",
            plot_width=500,
            x_axis_label='date',
            y_axis_label='weekly ranking',
            x_axis_type="datetime")

low_box = BoxAnnotation(top=10, fill_alpha=0.1, fill_color='green')
top_10 = Span(location=10,dimension='width', line_dash='dashed', line_width=3)
over_10 = BoxAnnotation(bottom=10, fill_alpha=0.1, fill_color='red')

# add a line renderer with legend and line thickness
p.line(x, y, legend="Weekly Gross (1989-1990)", line_width=2 )

rank_chart.line(x, y_rank, legend="Rank", line_width=2)
rank_chart.add_layout(top_10)
rank_chart.add_layout(over_10)
rank_chart.add_layout(low_box)

# use a formatter to display y-axis tick labels in million dollars
p.yaxis[0].formatter = NumeralTickFormatter(format="($ 0.00 a)")

show(row(p, rank_chart))
