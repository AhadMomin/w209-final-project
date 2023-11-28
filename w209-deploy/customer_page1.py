from flask import Flask, render_template
import altair as alt
import pandas as pd
import numpy as np

file_path = "/home/amomin/w209/static/DataCoSupplyChainDataset.csv"


def display_customer_base_bar():
    df = pd.read_csv(file_path,encoding="ISO-8859-1")
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
    df["Year"] = df["order date (DateOrders)"].dt.year
    # Count the number of customers per city and year
    city_counts = df.groupby(['Customer City', 'Year']).size().reset_index(name='Count')

    # Sort the DataFrame by count in descending order and select the top 20 cities
    top_20_cities = city_counts.nlargest(20, 'Count').sort_values(by='Count', ascending=False)

    # Create a stacked bar chart using Altair for the top 20 cities by year with heading and axis labels
    bar_chart = alt.Chart(top_20_cities).mark_bar().encode(
        x=alt.X('Customer City:N', title='City'),  # N indicates nominal data (categorical)
        y=alt.Y('Count:Q', title='Number of Customers', stack='normalize'),  # Stack bars by year and normalize the stack
        color='Year:N',  # Color bars by year
        tooltip=['Customer City:N', 'Count:Q', 'Year:N']
    ).properties(
        width=400,
        height=300,
        title='Top 10 Cities by Number of Customers (Stacked by Year Normalized)'
    )

    # Show the stacked bar chart
    return bar_chart.to_json()


def display_customer_cohort_heatmap():
    # Assuming df is your DataFrame
    df = pd.read_csv(file_path,encoding="ISO-8859-1")
    df= pd.DataFrame(df)
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
    df["Year"] = df["order date (DateOrders)"].dt.year
    df['YearMonth'] = df['order date (DateOrders)'].dt.strftime('%Y-%m')

    df['CohortMonth'] = df.groupby('Customer Id')['order date (DateOrders)'].transform('min').dt.strftime('%Y-%m')

    # Calculate the difference in days and then convert to months
    df['CohortIndex'] = ((pd.to_datetime(df['YearMonth']) - pd.to_datetime(df['CohortMonth'])).dt.days / 30).astype(int)

    cohorts = df.groupby(['CohortMonth', 'CohortIndex'])['Customer Id'].nunique().reset_index(name='Customer Count')

    color_scale = alt.Scale(scheme='viridis', domain=[0, 2000], range=['#f0f921', '#3e31b0', '#44ac44', '#000000'])

    heatmap = alt.Chart(cohorts).mark_rect().encode(
        x='CohortIndex:O',
        y=alt.Y('CohortMonth:O', sort='descending'),
        color=alt.Color('Customer Count:Q', scale=color_scale),
        tooltip=['CohortMonth:N', 'CohortIndex:O', 'Customer Count:Q']
    ).properties(
        width=500,
        height=400,
        title='Customer Order Retention Analysis (Cohort Heatmap)'
    )


    # Show the heatmap
    return heatmap.to_json()



