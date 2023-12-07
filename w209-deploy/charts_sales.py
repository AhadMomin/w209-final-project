from flask import Flask, render_template
import altair as alt
import pandas as pd


from otd_utils import selectable_legend, selectable_bar, global_styles, title_styles_heading, title_styles_footer


def display_chart_country():
    file_path = "/home/casey.hahn/w209/static/DataCoSupplyChainDataset.csv"
    df = pd.read_csv(file_path,encoding="ISO-8859-1")
    df_state = df.groupby(["Customer State", 'Department Name'])["Order Item Quantity"].sum().reset_index()

    df_state = df_state[(df_state['Customer State'] != "91732") & (df_state['Customer State'] != "95758")]

    country_list = [None]
    for item in df_state['Customer State'].unique():
        country_list.append(item)

    country_labels = ["All"]
    for item in df_state['Customer State'].unique():
        country_labels.append(item)

    department_list = [None]
    for item in df_state['Department Name'].unique():
        department_list.append(item)

    department_labels = ["All"]
    for item in df_state['Department Name'].unique():
        department_labels.append(item)


    department_dropdown = alt.binding_select(options=department_list, labels = department_labels, name="Department Name")
    #country_dropdown = alt.binding_select(options=country_list, labels = country_labels, name="Customer State")

    selection = alt.selection_point(fields=["Department Name"], on = "click", clear = "dblclick",bind = department_dropdown)
    selection_country = alt.selection_multi(fields=["Customer State"]) #,bind = country_dropdown

    # Calculating proportions
    df_state['proportion'] = df_state.groupby('Customer State')['Order Item Quantity'].transform(lambda x: x / x.sum())

    # Chart with normalized values
    chart = alt.Chart(df_state).mark_bar().encode(
        x=alt.X('Customer State', sort='-y'),
        y=alt.Y('proportion:Q',  title="Order Quantity (Normalized)"),
        tooltip=[ 'Customer State','proportion','Department Name'],
        color=alt.Color('Department Name:N').scale(scheme="tableau20")).add_params(
        selection).transform_filter(selection).properties(width = 900, height = 400).properties(
      title = title_styles_heading('Proportion of Sales by Department',['By Customer Region'], center=True))

    chart_text = alt.Chart(df_state).mark_text(text="").properties(title=title_styles_footer(global_styles['filter-notes']))

    chart_text_2 = alt.Chart(df_state).mark_text(text="").properties(
    title=title_styles_footer([' ', ' ', ' ',
        'Use widget below to filter data by shipper or customer regions.',
        "Select 'All' to see all data under that field.",
    ]))

    # Convert Altair chart to JSON
    chart_combined = chart & chart_text & chart_text_2
    chart_json = chart_combined.to_json()

    return chart_json


def display_chart_sales():
    df_daily_file_path = "/home/casey.hahn/w209/static/df_daily.csv"
    df_daily = pd.read_csv(df_daily_file_path,encoding="ISO-8859-1")
    df_daily_file_products_path = "/home/casey.hahn/w209/static/df_daily_products.csv"
    df_daily_products = pd.read_csv(df_daily_file_products_path,encoding="ISO-8859-1")
    df_daily_products['Products'] = df_daily_products['Product_Name_top5_per_department_others']


    product_sorted_list = ['Perfect Fitness Perfect Rip Deck',
     "Nike Men's Dri-FIT Victory Golf Polo",
     "O'Brien Men's Neoprene Life Vest",
     "Nike Men's Free 5.0+ Running Shoe",
     "Under Armour Girls' Toddler Spine Surge Runni",
     "Nike Men's CJ Elite 2 TD Football Cleat",
     'Field & Stream Sportsman 16 Gun Fire Safe',
     'Pelican Sunstream 100 Kayak',
     "Diamondback Women's Serene Classic Comfort Bi",
     'ENO Atlas Hammock Straps',
     "Nike Men's Comfort 2 Slide",
     'adidas Youth Germany Black/Red Away Match Soc',
     'Team Golf St. Louis Cardinals Putter Grip',
     "LIJA Women's Eyelet Sleeveless Golf Polo",
     "Glove It Women's Imperial Golf Glove",
     "adidas Men's F10 Messi TRX FG Soccer Cleat",
     "Glove It Women's Mod Oval 3-Zip Carry All Gol",
     'Glove It Imperial Golf Towel',
     "Columbia Men's PFG Anchor Tough T-Shirt",
     'Bridgestone e6 Straight Distance NFL Carolina',
     "Under Armour Women's Ignite Slide",
     'Team Golf Tennessee Volunteers Putter Grip',
     'Titleist Pro V1x High Numbers Personalized Go',
     "Nike Men's Deutschland Weltmeister Winners Bl",
     "Nike Women's Tempo Shorts",
     'Bridgestone e6 Straight Distance NFL San Dieg',
     'Team Golf Texas Longhorns Putter Grip',
     "Hirzl Women's Soffft Flex Golf Glove",
     'Clicgear 8.0 Shoe Brush',
     "Hirzl Women's Hybrid Golf Glove",
     "Top Flite Women's 2014 XL Hybrid",
     'Team Golf Pittsburgh Steelers Putter Grip',
     'Glove It Urban Brick Golf Towel',
     'Nike Dri-FIT Crew Sock 6 Pack',
     "TYR Boys' Team Digi Jammer",
     'Team Golf San Francisco Giants Putter Grip',
     'Clicgear Rovic Cooler Bag',
     "Hirzl Men's Hybrid Golf Glove",
     'Titleist Pro V1x Golf Balls',
     "adidas Men's Germany Black Crest Away Tee",
     'Titleist Pro V1 High Numbers Personalized Gol',
     "Under Armour Women's Ignite PIP VI Slide",
     "Under Armour Women's Micro G Skulpt Running S",
     'Under Armour Hustle Storm Medium Duffle Bag',
     'Bag Boy Beverage Holder',
     'Fighting video games',
     "Under Armour Men's Tech II T-Shirt",
     'Team Golf New England Patriots Putter Grip',
     "Under Armour Men's Compression EV SL Slide",
     'Bridgestone e6 Straight Distance NFL Tennesse',
     "Glove It Women's Mod Oval Golf Glove",
     "Nike Women's Legend V-Neck T-Shirt",
     'Titleist Pro V1x High Numbers Golf Balls',
     "Under Armour Kids' Mercenary Slide",
     "adidas Kids' F5 Messi FG Soccer Cleat",
     "Children's heaters",
     'Summer dresses',
     'Web Camera',
     'Toys ',
     'Adult dog supplies',
     'Lawn mower',
     'Porcelain crafts',
     'DVDs ',
     'Dell Laptop',
     'Rock music',
     'Industrial consumer electronics',
     'Sports Books ',
     'First aid kit',
     'Smart watch ',
     'CDs of rock',
     'Elevation Training Mask 2.0',
     "LIJA Women's Mid-Length Panel Golf Shorts",
     "Brooks Women's Ghost 6 Running Shoe",
     'Bag Boy M330 Push Cart',
     "Men's gala suit",
     'Baby sweater',
     "Merrell Women's Grassbow Sport Hiking Shoe",
     "Nike Women's Free 5.0 TR FIT PRT 4 Training S",
     "Nike Men's Free TR 5.0 TB Training Shoe",
     'Polar FT4 Heart Rate Monitor',
     "LIJA Women's Argyle Golf Polo",
     'TaylorMade White Smoke IN-12 Putter',
     'Fitbit The One Wireless Activity & Sleep Trac',
     "Nike Kids' Grade School KD VI Basketball Shoe",
     "The North Face Women's Recon Backpack",
     'MDGolf Pittsburgh Penguins Putter',
     "Merrell Men's All Out Flash Trail Running Sho",
     'Garmin Approach S3 Golf GPS Watch',
     "LIJA Women's Button Golf Dress",
     "Cleveland Golf Women's 588 RTX CB Satin Chrom",
     "Merrell Women's Siren Mid Waterproof Hiking B",
     "TaylorMade Women's RBZ SL Rescue",
     'Mio ALPHA Heart Rate Monitor/Sport Watch',
     'TaylorMade 2014 Purelite Stand Bag',
     'Cleveland Golf Collegiate My Custom Wedge 588',
     'adidas Brazuca 2014 Official Match Ball',
     'Yakima DoubleDown Ace Hitch Mount 4-Bike Rack',
     "Nike Men's Fingertrap Max Training Shoe",
     "Nike Men's Kobe IX Elite Low Basketball Shoe",
     'Ogio Race Golf Shoes',
     'insta-bed Neverflat Air Mattress',
     'GolfBuddy VT3 GPS Watch',
     "Merrell Women's Grassbow Sport Waterproof Hik",
     'Polar Loop Activity Tracker',
     'Titleist Small Wheeled Travel Cover',
     'Pelican Maverick 100X Kayak',
     'Garmin Approach S4 Golf GPS Watch',
     'Total Gym 1400',
     'Garmin Forerunner 910XT GPS Watch',
     'Titleist Club Glove Travel Cover',
     'GoPro HERO3+ Black Edition Camera',
     "Diamondback Boys' Insight 24 Performance Hybr",
     "Diamondback Girls' Clarity 24 Hybrid Bike 201",
     'Stiga Master Series ST3100 Competition Indoor',
     'SOLE E35 Elliptical',
     'Bushnell Pro X7 Jolt Slope Rangefinder',
     'SOLE E25 Elliptical',
     'Bowflex SelectTech 1090 Dumbbells']

    department_list = [None]
    for item in df_daily['Department Name'].unique():
        department_list.append(item)

    department_labels = ["All"]
    for item in df_daily['Department Name'].unique():
        department_labels.append(item)

    # Dropdown selection for department
    department_dropdown = alt.binding_select(options=department_list, labels = department_labels, name="Department Name")
    selection = alt.selection_point(fields=["Department Name"], on = "click", clear = "dblclick",bind = department_dropdown, value = None)

    # Range slider for minimum and maximum year_month selection
    brush = alt.selection_interval()

    # Dropdown selection for year
    year_list = [None]
    for year in df_daily['year_month'].str[:4].unique():
        year_list.append(int(year))

    year_labels = ["All"]
    for year in df_daily['year_month'].str[:4].unique():
        year_labels.append(str(year))

    year_dropdown = alt.binding_select(options=year_list, labels=year_labels, name="Year")
    year_selection = alt.selection_point(fields=["year"], bind=year_dropdown, value = None)

    inputs_chart = alt.vconcat(
        alt.Chart().mark_text(text="").encode(),
    ).properties(title="Input Controls").add_params(
        selection, year_selection
    )

    # Chart with interactive selection
    date_chart = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title="")).add_params(brush).properties(title=alt.TitleParams(text="Date Filter Slider", anchor='start'), width=450).add_params(year_selection).transform_filter(year_selection)

    chart_total = alt.Chart(df_daily).mark_bar().encode(
        x=alt.X('year_month:N', title=""),
        y=alt.Y('sum(Order Item Quantity):Q', scale=alt.Scale(zero=False), title="Order Quantity"),
        color=alt.condition(selection,alt.Color('Department Name:N').scale(scheme="tableau20"),alt.value('lightgray')),
        tooltip=[ 'Department Name','sum(Order Item Quantity)'],
    ).properties(width=450, height=300).add_params(
        selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(
      title = title_styles_heading('Total Items Sold',['By Department'], center=True))

    chart_by_product = alt.Chart(df_daily_products).mark_line().encode(
        x = alt.X('year_month:N',title = ""),
        y = alt.Y('sum(Order Item Quantity):Q', scale = alt.Scale(zero=False), title = "Order Quantity"),
        color = alt.Color("Products:N",sort = product_sorted_list).scale(scheme="tableau20"),
        tooltip=['Products', 'sum(Order Item Quantity)'],
        ).properties(width = 450, height = 300).add_params(
        selection).transform_filter(selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(
      title = title_styles_heading('Total Items Sold',['By Product'], center=True))


    chart_text = alt.Chart(df_daily_products).mark_text(text="").properties(title=title_styles_footer(global_styles['filter-notes']))

    chart_text_2 = alt.Chart(df_daily_products).mark_text(text="").properties(
    title=title_styles_footer([' ', ' ', ' ',
        'Use widget below to filter data by shipper or customer regions.',
        "Select 'All' to see all data under that field.",
    ]))
    

    chart = (chart_total  | chart_by_product).resolve_scale(color='independent')  & inputs_chart & chart_text & chart_text_2 & date_chart

    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json


def display_chart_sales_state():
    df_daily_file_path = "/home/casey.hahn/w209/static/df_daily_state.csv"

    df_daily = pd.read_csv(df_daily_file_path) #,encoding="ISO-8859-1"

    department_list = [None]
    for item in df_daily['Customer State'].unique():
        department_list.append(item)

    department_labels = ["All"]
    for item in df_daily['Customer State'].unique():
        department_labels.append(item)


    # Dropdown selection for department
    department_dropdown = alt.binding_select(options=department_list, labels = department_labels, name="Customer State")
    selection = alt.selection_point(fields=["Customer State"], bind = department_dropdown, clear = 'dblclick',on = "click", value = None)

    # Range slider for minimum and maximum year_month selection
    brush = alt.selection_interval()

    # Dropdown selection for year
    year_list = [None]
    for year in df_daily['year_month'].str[:4].unique():
        year_list.append(int(year))

    year_labels = ["All"]
    for year in df_daily['year_month'].str[:4].unique():
        year_labels.append(str(year))

    year_dropdown = alt.binding_select(options=year_list, labels=year_labels, name="Year")
    year_selection = alt.selection_point(fields=["year"], bind=year_dropdown, value = None)

    inputs_chart = alt.vconcat(
        alt.Chart().mark_text(text="").encode(),
    ).properties(title="Input Controls").add_params(
        selection, year_selection
    )

    # Chart with interactive selection
    date_chart = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title="")).add_params(brush).properties(title="Date Filter Slider", width=450).add_params(year_selection).transform_filter(year_selection)


    chart_total = alt.Chart(df_daily).mark_bar().encode(
        x=alt.X('year_month:N', title=""),
        y=alt.Y('sum(Order Item Quantity):Q', stack='zero', title="Order Quantity"),
        color=alt.condition(selection,alt.Color('Customer State:N').scale(scheme="tableau20"),alt.value('lightgray')),
        #color=alt.Color('Customer State:N',legend=None),
        tooltip=['Customer State:N', 'sum(Order Item Quantity):Q']
    ).properties(width=450, height=300).add_params(
        selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(
      title = title_styles_heading('Total Items Sold',['By Customer Region (stacked bar))'], center=True))

    chart_by_product = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title=""),
        y=alt.Y('sum(Order Item Quantity):Q', title="Order Quantity"),
        tooltip=['Customer State:N', 'sum(Order Item Quantity):Q'],
        color = alt.Color('Customer State:N').scale(scheme="tableau20")
    ).properties(width=450, height=300).add_params(
        selection).transform_filter(selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(
      title = title_styles_heading('Total Items Sold',['By Customer Region (line chart)'], center=True))


    chart_text = alt.Chart(df_daily).mark_text(text="").properties(title=title_styles_footer(global_styles['filter-notes']))

    chart_text_2 = alt.Chart(df_daily).mark_text(text="").properties(
    title=title_styles_footer([' ', ' ', ' ',
        'Use widget below to filter data by shipper or customer regions.',
        "Select 'All' to see all data under that field.",
    ]))

    chart = (chart_total  | chart_by_product) & inputs_chart & chart_text & chart_text_2 & date_chart
    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json

def display_sales():
    df_daily_file_path = "/home/casey.hahn/w209/static/df_daily_state.csv"

    df_daily = pd.read_csv(df_daily_file_path) #,encoding="ISO-8859-1"

    # Range slider for minimum and maximum year_month selection
    brush = alt.selection_interval()

    # Dropdown selection for year
    year_list = [None]
    for year in df_daily['year_month'].str[:4].unique():
        year_list.append(int(year))

    year_labels = ["All"]
    for year in df_daily['year_month'].str[:4].unique():
        year_labels.append(str(year))

    year_dropdown = alt.binding_select(options=year_list, labels=year_labels, name="Year")
    year_selection = alt.selection_point(fields=["year"], bind=year_dropdown, value = None)

    inputs_chart = alt.vconcat(
        alt.Chart().mark_text(text="").encode(),
    ).properties(title="Input Controls").add_params(
        year_selection
    )

    # Chart with interactive selection
    date_chart = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title="")).add_params(brush).properties(title="Date Filter Slider", width=450).add_params(year_selection).transform_filter(year_selection)


    chart_total = alt.Chart(df_daily).mark_bar().encode(
        x=alt.X('year_month:N', title=""),
        y=alt.Y('sum(Order Item Quantity):Q', stack='zero', title="Order Quantity"),
        #color=alt.Color('Customer State:N',legend=None),
        tooltip=['year_month:N', 'sum(Order Item Quantity):Q']
    ).properties(width=450, height=300).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(
      title = title_styles_heading('Total Items Sold',[''], center=True))

    chart_text = alt.Chart(df_daily).mark_text(text="").properties(title=title_styles_footer(global_styles['filter-notes']))

    chart_text_2 = alt.Chart(df_daily).mark_text(text="").properties(
    title=title_styles_footer([' ', ' ', ' ',
        'Use widget below to filter data by shipper or customer regions.',
        "Select 'All' to see all data under that field.",
    ]))

    chart = (chart_total) & inputs_chart & chart_text & chart_text_2 & date_chart
    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json


def display_heatmap():
    df_heatmap = "/home/casey.hahn/w209/static/df_heatmap.csv"

    df_heatmap_1 = pd.read_csv(df_heatmap) #,encoding="ISO-8859-1"

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    day_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    heatmap_chart_month_day = alt.Chart(df_heatmap_1).mark_rect().encode(
        x=alt.X('order_date_month:N', sort=month_order, title='Month'),
        y=alt.Y('order_date_day_name:N', sort=day_order, title='Day'),
        color=alt.Color('mean(Order Item Quantity):Q', title='Total Quantity').scale(scheme='blues'),
        tooltip = ['mean(Order Item Quantity)']
    ).properties(
        width=400,
        height=300).properties(
      title = title_styles_heading('Average Order Item Quantity',['By Month and Day of the Week'], center=True))

    # Create the Altair chart for month
    heatmap_chart_month = alt.Chart(df_heatmap_1).mark_rect().encode(
        x=alt.X('order_date_month:N', sort=month_order, title='Month'),
        color=alt.Color('mean(Order Item Quantity):Q', title='Total Quantity').scale(scheme='blues'),
        tooltip = ['mean(Order Item Quantity)']
    ).properties(
        width=400,
        height=50).properties(
      title = title_styles_heading('Average Order Item Quantity',['By Month'], center=True))

    # Create the Altair chart for weekday
    heatmap_chart_weekday = alt.Chart(df_heatmap_1).mark_rect().encode(
        x=alt.X('order_date_day_name:N', sort=day_order, title='Day'),
        color=alt.Color('mean(Order Item Quantity):Q', title='Total Quantity').scale(scheme='blues'),
        tooltip = ['mean(Order Item Quantity)']
    ).properties(
        width=400,
        height=50).properties(
      title = title_styles_heading('Average Order Item Quantity',['By Day of the Week'], center=True))

    # Combine and resolve the charts
    chart = (heatmap_chart_month & heatmap_chart_weekday & heatmap_chart_month_day).resolve_scale(color='independent')

    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json

