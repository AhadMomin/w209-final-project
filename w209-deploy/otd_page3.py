# -*- coding: utf-8 -*-
"""otd_page3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uatZ2pheGBZE-vZNA9JkQ_nv030ZxC4q

## Imports & Inits
"""

# Assume altair-5 is already installed. If not, run this command:
# !pip install altair==5

import altair as alt
import numpy as np
import pandas as pd
import os
import sys

print(alt.__version__)

# Enable large dataset.
alt.data_transformers.disable_max_rows()

# Setup base dir.
BASE_DIR=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'w209')

# Special setup if this script is running in colab.
IN_COLAB = 'google.colab' in sys.modules
if (IN_COLAB):
  from google.colab import drive
  drive.mount('/content/drive')
  BASE_DIR = '/content/drive/MyDrive/Colab Notebooks/datasci-209/final-project'

# Setup frequently-used directories.
DATA_DIR=os.path.join(BASE_DIR, 'static')
LIB_DIR=os.path.join(BASE_DIR, 'lib')

# Include the lib dir in the module-search path.
sys.path.append(LIB_DIR)

# Import utilities library.
from otd_utils import selectable_legend, plot_shipper_map_points, plot_customer_map_points, title_styles_heading

# Hard-code URLs to the map data to avoid installing vega_datasets on the web server.
world_110m_url='https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/world-110m.json'
us_10m_url='https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json'

"""## EDA
- Actual EDA works are done in Final-Project_Delivery-Status_EDA notebook.
- Please refer to the details in that notebook.
- The current notebook is only responsible of loading the dataset from the data file created in the EDA notebook.
- This will make the current notebook clean and improve performance.
"""

def load_data(year=2015):
  # Load aggregation-specific and map-specific dataset.
  agg_df = pd.read_csv(os.path.join(DATA_DIR,'DataCoSupplyChainDataset_DS_AGG.csv'),encoding='unicode_escape')
  map_df = pd.read_csv(os.path.join(DATA_DIR,'DataCoSupplyChainDataset_DS_MAP.csv'),encoding='unicode_escape')

  # Uncomment below to inspect the dataframe.
  # pd.set_option('display.max_columns',None)
  # display(agg_df.head())
  # display(agg_df.shape)

  agg_df_by_year = agg_df[ agg_df['Order Year'] == year ]
  map_df_by_year = map_df[ map_df['Order Year'] == year ]

  return agg_df_by_year, map_df_by_year

"""## Build Views: Page-3

### Viz-3.1: Shipper Map - Worldwide
"""

# Create shipper map.
def create_shipper_map(map_df, legend, preview=False):
  # Read in a polygons from topo-json
  world = alt.topo_feature(world_110m_url, 'countries')

  # Plot the background with a world map.
  background = alt.Chart(world).mark_geoshape(
      fill='lightgray',
      stroke='white'
  ).properties(
      width=1000,
      height=500
  ).project('equirectangular') # naturalEarth1

  # Plot points for each delivery status.
  world_status_map = background + plot_shipper_map_points(map_df, legend)

  if (preview):
    world_status_map.display()

  return world_status_map

"""### Viz-3.2: Customer Map - USA"""

# Create customer map.
def create_customer_map(map_df, legend, preview=False):
  # Read in a polygons from topo-json
  states = alt.topo_feature(us_10m_url, feature='states')

  # Plot the background with a US map.
  background = alt.Chart(states).mark_geoshape(
      fill='lightgray',
      stroke='white'
  ).properties(
      width=1000,
      height=500
  ).project('albersUsa')

  # Plot points for each delivery status.
  usa_status_map = background + plot_customer_map_points(map_df, legend)

  if (preview):
    usa_status_map.display()

  return usa_status_map

"""### Page-3: Combined Map"""

def create_shipper_customer_map(preview=False):
  # Load data.
  agg_df, map_df = load_data()

  # Create a common legend.
  legend = selectable_legend(agg_df, 'Delivery Status:N')
  # legend['plot'] # Uncomment to test.

  # Create Shipper Map.
  world_status_map = create_shipper_map(map_df, legend)
  world_status_map = world_status_map.properties(
      title = title_styles_heading(
        subtitle=["Shippers Delivery Status Around the World"])
  )

  # Create Customer Map.
  usa_status_map = create_customer_map(map_df, legend)
  usa_status_map = usa_status_map.properties(
      title = title_styles_heading(
        subtitle=["Customers Delivery Status in US"])
  )

  # Create Main View: Shipper Map & Customer Map.
  chart = (world_status_map & usa_status_map)

  # Create Main View: Shipper Map & Customer Map (with legend)
  # chart = ((world_status_map | legend['plot']) & usa_status_map)
  chart = chart.properties(
    title = title_styles_heading(center=True,
        title='Shippers and Customers Delivery Status')
  )

  if (preview):
    chart.display()

  return chart.to_json()

"""## Unit Tests"""

def __test_create_shipper_map():
  agg_df, map_df = load_data()
  legend = selectable_legend(agg_df, 'Delivery Status:N')

  create_shipper_map(map_df, legend, preview=True)

# __test_create_shipper_map()

def __test_create_customer_map():
  agg_df, map_df = load_data()
  legend = selectable_legend(agg_df, 'Delivery Status:N')

  create_customer_map(map_df, legend, preview=True)

# __test_create_customer_map()

def __test_create_shipper_customer_map():
  create_shipper_customer_map(preview=True)

# __test_create_shipper_customer_map()

"""## Experiment"""

def __exp1():
  exp_map_df = pd.read_csv(os.path.join(DATA_DIR,'DataCoSupplyChainDataset_DS_AGG.csv'),encoding='unicode_escape')
  exp_df_by_year = exp_map_df[ exp_map_df['Order Year'] == 2015 ]

  display(exp_map_df.shape)
  display(exp_df_by_year.shape)

def __exp2():
  exp_map_df = pd.read_csv(os.path.join(DATA_DIR,'DataCoSupplyChainDataset_DS_MAP.csv'),encoding='unicode_escape')
  exp_df_by_year = exp_map_df[ exp_map_df['Order Year'] == 2015 ]

  display(exp_map_df.shape)
  display(exp_df_by_year.shape)

def __exp3():
  agg_df, map_df = load_data(2017)

  display(agg_df.shape)
  display(map_df.shape)

  cols = [
    'Order Longitude', 'Order Latitude',
    'Delivery Status', 'Order City', 'Order State', 'Order Country',
  ]

  map_df[cols]