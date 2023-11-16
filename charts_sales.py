from flask import Flask, render_template
import altair as alt
import pandas as pd


def display_chart_sales():
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