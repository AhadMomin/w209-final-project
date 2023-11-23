from flask import Flask, render_template
import altair as alt
import pandas as pd

def display_chart_country():
    file_path = "/home/casey.hahn/w209/static/DataCoSupplyChainDataset.csv"
    df = pd.read_csv(file_path,encoding="ISO-8859-1")

    df_state = df.groupby(["Order Country", 'Department Name'])["Order Item Quantity"].sum().reset_index()

    country_list = [None]
    for item in df_state['Order Country'].unique():
        country_list.append(item)

    country_labels = ["All"]
    for item in df_state['Order Country'].unique():
        country_labels.append(item)

    department_list = [None]
    for item in df_state['Department Name'].unique():
        department_list.append(item)

    department_labels = ["All"]
    for item in df_state['Department Name'].unique():
        department_labels.append(item)


    department_dropdown = alt.binding_select(options=department_list, labels = department_labels, name="Department Name")
    country_dropdown = alt.binding_select(options=country_list, labels = country_labels, name="Country")

    selection = alt.selection_point(fields=["Department Name"], bind = department_dropdown)
    selection_country = alt.selection_point(fields=["Order Country"], clear = "dblclick",on = "click",bind = country_dropdown)

    # Calculating proportions
    df_state['proportion'] = df_state.groupby('Order Country')['Order Item Quantity'].transform(lambda x: x / x.sum())

    # Chart with normalized values
    chart = alt.Chart(df_state).mark_bar().encode(
        x=alt.X('Order Country', sort='-y'),
        y=alt.Y('proportion:Q',  title="Order Quantity (Normalized)"),
        color=alt.condition(selection_country,alt.Color('Department Name:N'),alt.value('lightgray'))).add_params(selection_country).add_params(
        selection).transform_filter(selection).properties(title = "Proportion of Sales by Department (Filter by Department)", width = 1000)

    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json


def display_chart_sales():
    df_daily_file_path = "/home/casey.hahn/w209/static/df_daily.csv"
    df_daily = pd.read_csv(df_daily_file_path,encoding="ISO-8859-1")
    df_daily_file_products_path = "/home/casey.hahn/w209/static/df_daily_products.csv"
    df_daily_products = pd.read_csv(df_daily_file_products_path,encoding="ISO-8859-1")

    department_list = [None]
    for item in df_daily['Department Name'].unique():
        department_list.append(item)

    department_labels = ["All"]
    for item in df_daily['Department Name'].unique():
        department_labels.append(item)

    # Dropdown selection for department
    department_dropdown = alt.binding_select(options=department_list, labels = department_labels, name="Department Name")
    selection = alt.selection_point(fields=["Department Name"], bind = department_dropdown, value = None)

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

    # Chart with interactive selection
    date_chart = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title="")).add_params(brush).properties(title="Date Filter Slider", width=450).add_params(year_selection).transform_filter(year_selection)

    chart_total = alt.Chart(df_daily).mark_line().encode(
        x=alt.X('year_month:N', title=""),
        y=alt.Y('sum(Order Item Quantity):Q', scale=alt.Scale(zero=False), title="Order Quantity"),
        tooltip=[ 'sum(Order Item Quantity)'],
    ).properties(width=400, height=200).add_params(
        selection).transform_filter(selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(title="Items Sold")

    chart_by_product = alt.Chart(df_daily_products).mark_line().encode(
        x = alt.X('year_month:N',title = ""),
        y = alt.Y('sum(Order Item Quantity):Q', scale = alt.Scale(zero=False), title = "Order Quantity"),
        color = "Product_Name_top5_per_department_others",
        tooltip=['Product_Name_top5_per_department_others', 'sum(Order Item Quantity)'],
        ).properties(width = 400, height = 200).add_params(
        selection).transform_filter(selection).transform_filter(brush).add_params(year_selection).transform_filter(year_selection).properties(title = "Items Sold by Product")


    chart = (chart_total  | chart_by_product) & date_chart

    # Convert Altair chart to JSON
    chart_json = chart.to_json()

    return chart_json


