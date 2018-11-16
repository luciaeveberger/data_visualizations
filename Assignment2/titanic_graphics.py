from bokeh.plotting import figure, show
import pandas as pd
from math import pi

from bokeh.layouts import row
from bokeh.palettes import Reds, Greens
from bokeh.plotting import figure
from bokeh.transform import cumsum

def create_bar_chart():
    df_home_destinations = (df['home.dest'].value_counts().to_frame('count'))[:25]
    df_home_destinations.head()
    list_of_places = list(df_home_destinations.index)
    p = figure(x_range=list_of_places, width=1000,title="Top 25: Geographical Distribution of Destinations" )
    p.vbar(source=df_home_destinations, x='index', width=1.0, bottom=0, top='count',
            line_color='white', fill_color='cornflowerblue')
    # rotates the axis
    p.y_range.start = 0
    p.title.align = 'center'
    p.xaxis.major_label_orientation = "vertical"
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None# annotate the graphic
    p.xaxis.axis_label = "Desination [name]"
    p.yaxis.axis_label = "count"
    p.xgrid.visible = False
    show(p)


def create_class_sp():
    survival_rate = df.loc[df['survived'] == 1]
    death_rate = df.loc[df['survived'] == 0]
    rates_of_survival = {'1': 0, '2': 0, '3': 0}
    rates_of_death = {'1': 0, '2': 0, '3': 0}
    for i in range(1,4):
        rates_of_survival[str(i)] = len(survival_rate.loc[survival_rate['pclass'] == i])/len(survival_rate)
        rates_of_death[str(i)] = len(death_rate.loc[death_rate['pclass'] == i])/len(death_rate)

    death_chart = create_wedge_chart(rates_of_death, Reds, "Rate of Death by Class")
    survival_chart = create_wedge_chart(rates_of_survival, Greens, "Rate of Survival by Class")
    show(row(survival_chart, death_chart))


def create_wedge_chart(data, colors, title):
    data = pd.Series(data).reset_index(name='value').rename(columns={'index': 'rates_of_death'})
    print(data.head)
    data["legend"] = "Class" + data['rates_of_death'].astype(str) \
                     + " " + (data['value']).astype(str) + "%)"
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['color'] = colors[len(data)]

    p = figure(plot_height=350, title=title, toolbar_location=None,
               tools="hover", tooltips="@rates_of_death: @value")

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='legend', source=data)
    return p


from bokeh.core.properties import value
from bokeh.models import ColumnDataSource

def survival_rate_by_age():
    age_sorted = df.sort_values(by='age')
    columns = ['age_bracket', 'count', 'survival', 'male', 'female']
    lst = list()
    for i in range(1, 90, 10):
        subset = age_sorted.loc[(age_sorted["age"] < i + 10) & (age_sorted["age"] > i - 10)]
        count_of_male = len(subset.loc[
            (subset['sex'] == 'male') & (subset['survived'] == 1)])
        count_of_female = len(subset.loc[
                                (subset['sex'] == 'female') & (subset['survived'] == 1)])

        lst.append([i, len(subset), len(subset.loc[subset['survived'] == 1]) / len(subset),
                    count_of_male, count_of_female])

    from bokeh.transform import dodge
    age_survival_dict = pd.DataFrame(lst, columns=columns)
    line_chart = figure(plot_width=400, plot_height=400)
    line_chart.line(source=age_survival_dict, x='age_bracket', y='survival', line_width=2)


    age_cohorts = ['0-10', '11-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70+']
    sex = ["male", "female"]
    colors = ["#c9d9d3", "#718dbf"]

    data = {'age_cohorts': age_cohorts,
            'male': age_survival_dict['male'][:8],
            'female': age_survival_dict['female'][:8]}
    source = ColumnDataSource(data=data)

    p = figure(x_range=age_cohorts, y_range=(0, 300), plot_height=250, title="Fruit Counts by Year",
               toolbar_location=None, tools="")

    p.vbar(x=dodge('age_cohorts', -0.25, range=p.x_range), top='male', width=0.2, source=source,
           color="#c9d9d3", legend=value("male"))

    p.vbar(x=dodge('age_cohorts', 0.0, range=p.x_range), top='female', width=0.2, source=source,
           color="#718dbf", legend=value("female"))

    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    show(row(line_chart,p))


filename = "titanic3.csv"
df = pd.read_csv( filename, header=0 )
#create_class_sp()
survival_rate_by_age()

