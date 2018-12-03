import pandas as pd
import numpy as np

from bokeh.models import DataRange1d, FactorRange, ColumnDataSource, LabelSet
from bokeh.plotting import figure, Figure
from bokeh.layouts import gridplot

def getCategoricalRanges( df, cols ):
    # all columns that are not int or float
    colsC = list(df.columns[[(x in cols) and (df[x].dtype not in [np.float64,np.int64]) for x in df.columns]])
    print( 'categorical attributes', colsC )
    ranges = {}
    
    for c in colsC:
        ranges[c] = np.sort(df[c].unique())
    
    return ranges
    
def getAxisParameters( source, cats, x, y ):
    '''
    Return axis formatting parameters (numeric vs. categorical). 
    '''
    args = {}
    
    if (y in cats) and (x is not y):
        args['y_range'] = cats[y]
    if (x in cats) and ((x is y) or (y not in cats)):
        args['x_range'] = cats[x]

    return args


def setAxisTitles( plots, cols, x_padding, y_padding ):
    '''
    Set axis titles for the SPLOM, i.e., first column and last row.
    '''
    for pp, name in zip(plots, cols):
        p = pp[0]
        p.yaxis.visible = True
        p.yaxis.axis_label_text_font_size = '12pt'
        p.plot_width += y_padding
        p.yaxis.axis_label = name

    plots[0][0].yaxis.axis_label = 'probability'
    
    for p, name in zip(plots[-1], cols):
        p.xaxis.visible = True
        p.xaxis.axis_label_text_font_size = '12pt'
        p.plot_height += x_padding
        p.xaxis.axis_label = name    

def stackedBar( self, source, x, y, **kwargs ):
    '''
    A stacked barchart for categorical vs. categorical data.
    '''
    if not isinstance(source, pd.core.groupby.DataFrameGroupBy ):
        msg = "source has to be a pandas.DataFrameGroupyBy. Received " + str(type(df)) + " Use df.groupy([" + x + "," + y + "]) to obtain valid input."
        raise TypeError(msg)

    # make sure we have a quantitative variable that is used in source.describe()
    cds = ColumnDataSource(source)
    cds.add( source.count().index.get_level_values(1), 'labels' )
    factors = list(source[x].count().index.levels[0])
    
    self.vbar( x=x+'_'+y, top='mycnt_count', width=1, source=cds,
               line_color='white' )
    
    labels = LabelSet(x=x+'_'+y, y='mycnt_count', text='labels', level='glyph', text_align='center',
              text_font_size='6pt', y_offset=3, source=cds, render_mode='canvas')

    self.y_range.start = 0
    self.xgrid.grid_line_color = None
    self.xaxis.major_label_orientation = 1.2
    self.outline_line_color = None
    self.add_layout(labels)

Figure.stackedBar = stackedBar        
        
        
def splom( df: pd.DataFrame, splom_width=0, nbins_histogram=0, **kwargs ): 
    '''
    Create a scatterplot matrix of the given data.
    '''
    if not isinstance(df, pd.DataFrame ):
        raise TypeError("source has to be a pandas DataFrame. Received ", type(df))

    source = ColumnDataSource(df)
        
    # Read the keyword arguments and set defaults if not provided
    cols      = kwargs['cols']      if 'cols'      in kwargs else list(df.columns)    
    x_padding = kwargs['x_padding'] if 'x_padding' in kwargs else 40   
    y_padding = kwargs['y_padding'] if 'y_padding' in kwargs else 80    
    width     = int(splom_width / (len(cols)+1)) if splom_width > 0 else 200
    height    = int(splom_width / (len(cols)+1)) if splom_width > 0 else 200
    
    cats = getCategoricalRanges(df, cols)
    TOOLS = "box_select,lasso_select,reset,save,help"

    # make sure we have a quantitative variable that is used in source.describe()
    df['mycnt'] = 1
    
    plots = []    
    for i in cols:
        pp = []
        
        for j in cols:    
            myargs = getAxisParameters( df, cats, j, i )
            p = figure( tools=TOOLS, plot_width=width, plot_height=height, **myargs )
            p.xaxis.visible = False
            p.yaxis.visible = False
            
            if i is j:
                p.histogram( source=df, x=j, nbins=nbins_histogram )
            else:
                if i in cats:
                    if j in cats: 
                        group = df.groupby([j,i])
                        p = figure( tools=TOOLS, plot_width=width, plot_height=height, x_range=group )
                        p.xaxis.visible = False
                        p.yaxis.visible = False
                        p.stackedBar( source=group, x=j, y=i )
                    else:
                        p.hboxplot( source=df, x=j, y=i )
                elif j in cats:
                    p.vboxplot( source=df, x=j, y=i )
                else:
                    p.scatter( source=df, x=j, y=i )
                
            pp.append(p)
        plots.append(pp)
        
    del df['mycnt']
    setAxisTitles( plots, cols, x_padding, y_padding )

    return gridplot(plots)