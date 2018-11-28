import pandas as pd
import numpy as np
from bokeh.plotting import Figure
from bokeh.models import Range1d, FactorRange, CategoricalColorMapper
from bokeh.palettes import Category10
import collections

def scatter( self, source, x, y, **kwargs ):
#    color_mapper = CategoricalColorMapper(factors=np.sort(source['Region'].unique()), 
#                    palette=Category10[3])
#    self.circle( source=source, x=x, y=y, line_alpha=0.3, fill_alpha=1,
#                color={'field': 'Region', 'transform': color_mapper}, size=3, **kwargs)
    color_mapper = CategoricalColorMapper(factors=np.sort(source['label'].unique()), 
                    palette=Category10[10])
    self.circle( source=source, x=x, y=y, line_alpha=0.3, fill_alpha=0.9,
                color={'field': 'label', 'transform': color_mapper}, size=5, **kwargs)
    
    
    # access the figure using the self variable
    #self.circle( source=source, x=x, y=y, line_alpha=0.3, fill_alpha=0.5, size=5, **kwargs)

Figure.scatter = scatter


def vboxplot( self, source, x, y, **kwargs ):
    if not isinstance(source, pd.DataFrame ):
        raise TypeError("source has to be a pandas DataFrame.")

    groups = source.groupby([x])[y]
    cats = list(groups.groups.keys())
        
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group > upper.loc[cat]) | (group < lower.loc[cat])]
    out = groups.apply(outliers).dropna()

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper = [min([x,y]) for (x,y) in zip(list(qmax),upper)]
    lower = [max([x,y]) for (x,y) in zip(list(qmin),lower)]

    # stems
    self.segment(cats, upper, cats, q3, line_color='slategray')
    self.segment(cats, lower, cats, q1, line_color='slategray')

    # whiskers (almost-0 height rects simpler than segments)
    self.rect(cats, lower, 0.2, 0.01, line_color='slategray')
    self.rect(cats, upper, 0.2, 0.01, line_color='slategray')

    # boxes
    self.vbar(cats, 0.7, q2, q3, fill_color='steelblue', line_color='darkslategray')
    self.vbar(cats, 0.7, q1, q2, fill_color='steelblue', line_color='darkslategray')

    # outliers
    for i in cats:
        if not out[i].empty:
            self.circle( x=[i]*len(out[i]), y=out[i], fill_color='deeppink' )


Figure.vboxplot = vboxplot

def hboxplot( self, source, x, y, **kwargs ):
    if not isinstance(source, pd.DataFrame ):
        raise TypeError("source has to be a pandas DataFrame.")

    groups = source.groupby([y])[x]
    cats = list(groups.groups.keys())
        
    q1 = groups.quantile(q=0.25)
    q2 = groups.quantile(q=0.5)
    q3 = groups.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group > upper.loc[cat]) | (group < lower.loc[cat])]
    out = groups.apply(outliers).dropna()

    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper = [min([x,y]) for (x,y) in zip(list(qmax),upper)]
    lower = [max([x,y]) for (x,y) in zip(list(qmin),lower)]

    # stems
    self.segment(upper, cats, q3, cats, line_color='slategray')
    self.segment(lower, cats, q1, cats, line_color='slategray')

    # whiskers (almost-0 height rects simpler than segments)
    self.rect(lower, cats, 0.01, 0.2, line_color='slategray')
    self.rect(upper, cats, 0.01, 0.2, line_color='slategray')

    # boxes
    self.hbar(cats, 0.7, q2, q3, fill_color='steelblue', line_color='darkslategray')
    self.hbar(cats, 0.7, q1, q2, fill_color='steelblue', line_color='darkslategray')

    for i in cats:
        if not out[i].empty:
            self.circle( y=[i]*len(out[i]), x=out[i], fill_color='deeppink' )


Figure.hboxplot = hboxplot


def histogram( self, source, x, nbins=0, *args, **kwargs ):
    
    if not isinstance(source, pd.DataFrame ):
        raise TypeError("source has to be a pandas.DataFrame. Received ", type(df))

    data = source[x]   
    bins = nbins  if nbins > 0 else 9    
    n    = len(data)
    
    self.y_range = Range1d(-0.05,1.05);
    self.xgrid.grid_line_color = None
    if n < 0:
        return
    
    # create a histogram for numerical data
    if data.dtype in (np.float64,np.int64):
        hist, edges = np.histogram( data, density=False, bins=bins )
        self.quad( top=hist/n, bottom=0, left=edges[:-1], right=edges[1:], fill_color='orange', line_color='slategray' )

    #create a histogram for categorical data
    else:
        cnt = collections.Counter(data)
        hist = np.array( list(cnt.values()) ) / n
        labels = list(cnt.keys())
        self.vbar( x=labels, top=hist, width=0.3, fill_color='orange', line_color='slategray')

Figure.histogram = histogram