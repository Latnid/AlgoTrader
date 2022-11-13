import time
import numpy as np
import pandas as pd
import holoviews as hv
import streamz
import streamz.dataframe

from holoviews import opts
from holoviews.streams import Pipe, Buffer

hv.extension('bokeh')
pipe = Pipe(data=[])
vector_dmap = hv.DynamicMap(hv.VectorField, streams=[pipe])
vector_dmap.opts(color='Magnitude', xlim=(-1, 1), ylim=(-1, 1))