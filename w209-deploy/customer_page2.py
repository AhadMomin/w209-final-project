from flask import Flask, render_template
import altair as alt
import pandas as pd
import numpy as np

file_path = "/home/amomin/w209/static/DataCoSupplyChainDataset.csv"


def display_customer_base_dash():

    df = pd.read_csv(file_path,encoding="ISO-8859-1")
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
    df["Year"] = df["order date (DateOrders)"].dt.year
    # Count the number of customers per city and year

    city_counts = df['Customer City'].value_counts().reset_index()
    city_counts.columns = ['Customer City', 'Count']

    p10, p30, p50, p70, p90, p100 = np.percentile(city_counts['Count'], [10, 30, 50, 70, 90, 100])

    # Create a new column 'Flag' in the city_counts DataFrame
    city_counts['Percentile'] = pd.cut(city_counts['Count'],
                                bins=[-float('inf'), p10, p30, p50, p70, p90, float('inf')],
                                labels=['p10', 'p30', 'p50', 'p70', 'p90','p100'])

    city_counts = city_counts.sort_values(by='Count', ascending=False)

    city_counts2 = df.groupby(['Customer City', 'Year']).size().reset_index(name='Count')

    city_counts3 = pd.merge(city_counts2,
                            city_counts,
                            left_on='Customer City',
                            right_on='Customer City').rename(columns=
                            {'Count_x':'Count','Count_y':'Count_Total'}   
                            )

    city_counts3 = city_counts3.sort_values(by='Count', ascending=False)


    top_list = []
    for item in city_counts3['Percentile'].unique():
        top_list.append(item)

    year_list = ['ALL']
    for item_ in city_counts3['Year'].unique():
        year_list.append(item_)

    top_dropdown = alt.binding_select(options=top_list, name="Top Cities By Percentile: ")
    selection = alt.selection_point(fields=["Percentile"], bind = top_dropdown)

    year_dropdown = alt.binding_select(options=year_list, name="Color By: ")
    selection_year= alt.selection_multi(fields=["Year"],clear = "dblclick",on = "click" ,bind = year_dropdown)
    # Create a bar chart using Altair
    bar_chart = alt.Chart(city_counts3).mark_bar().encode(
        x=alt.X('Customer City:N', title='City'),  # N indicates nominal data (categorical)
        y=alt.Y('Count:Q', title='Number of Customers'),
        color= alt.condition(selection_year, alt.Color('Year:N'),alt.value('lightgray')), # Sort the bars in descending order
        tooltip=['Customer City:N', 'Count:Q']
    ).add_params(
        selection_year
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title='Top Cities by Number of Customers',
        width=800,
        height=350
    )

    # bar_chart

    bar_chart_norm =alt.Chart(city_counts3).mark_bar().encode(
        x=alt.X('Customer City:N', title='City'),  # N indicates nominal data (categorical)
        y=alt.Y('Count:Q', title='Number of Customers %',stack='normalize'),
        color= alt.condition(selection_year, alt.Color('Year:N'),alt.value('lightgray')), # Sort the bars in descending order
        tooltip=['Customer City:N', 'Count:Q']
    ).add_params(
        selection_year
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title='Top Cities by Number of Customers (Normalized)',
        width=800,
        height=350
    )
    pie_chart = alt.Chart(city_counts3).mark_arc().encode(
        theta='Count:Q',
        color='Customer City:N',
        tooltip=['Customer City:N', 'Count:Q', 'Percentile:N']
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title='Distribution of Customers by City',
        width=400,
        height=400
    )
    pie_chart2 = alt.Chart(city_counts3).mark_arc().encode(
        theta='Count:Q',
        color=alt.condition(selection_year, alt.Color('Year:N'),alt.value('lightgray')),
        tooltip=['Customer City:N', 'Count:Q', 'Percentile:N','Year:N']
    ).add_params(
        selection_year
    ).add_params(
        selection
    ).transform_filter(
        selection
    ).properties(
        title='Distribution of Customers by Year',
        width=400,
        height=400
    )

    chart1 = alt.hconcat(bar_chart, pie_chart2)
    chart2 = alt.hconcat(bar_chart_norm, pie_chart)
    final_chart = alt.vconcat(chart1,chart2).resolve_legend('independent')

    return final_chart.to_json() 


def display_customer_cohort_dash():
    df = pd.read_csv(file_path,encoding="ISO-8859-1")
    df["order date (DateOrders)"] = pd.to_datetime(df["order date (DateOrders)"])
    df["Year"] = df["order date (DateOrders)"].dt.year
    df['YearMonth'] = df['order date (DateOrders)'].dt.strftime('%Y-%m')

    df['CohortMonth'] = df.groupby('Customer Id')['order date (DateOrders)'].transform('min').dt.strftime('%Y-%m')

    # Calculate the difference in days and then convert to months
    df['CohortIndex'] = ((pd.to_datetime(df['YearMonth']) - pd.to_datetime(df['CohortMonth'])).dt.days / 30).astype(int)

    # Calculate the percentage of customers in each cohort
    cohorts = df.groupby(['CohortMonth', 'CohortIndex'])['Customer Id'].nunique().reset_index(name='Customer Count')
    total_customers = cohorts.groupby('CohortMonth')['Customer Count'].transform('sum')
    cohorts['Customer Percentage'] = (cohorts['Customer Count'] / total_customers) * 100
    cohorts['Year'] = pd.to_datetime(cohorts['CohortMonth']).dt.year

    brush = alt.selection_interval()
    color_scale_count = alt.Scale(scheme='plasma', domain=[0, 30], range=['#f0f921', '#3e31b0', '#44ac44', '#000000'])
    color_scale_percentage = alt.Scale(scheme='plasma', domain=[0, 100], range=['#f0f921', '#3e31b0', '#44ac44', '#000000'])
    year_list = [None]
    for year in cohorts['CohortMonth'].str[:4].unique():
        year_list.append(int(year))

    year_labels = ["All"]
    for year in cohorts['CohortMonth'].str[:4].unique():
        year_labels.append(str(year))

    year_dropdown = alt.binding_select(options=year_list, labels=year_labels, name="Year")
    year_selection = alt.selection_point(fields=["Year"], bind=year_dropdown, value = None)
    date_chart = alt.Chart(cohorts).mark_line().encode(
        x=alt.X('CohortMonth:N', title="")).add_params(brush).properties(title="Date Filter Slider", width=450).add_params(year_selection).transform_filter(year_selection).properties(
        width=700,
        height=50)

    heatmap = alt.Chart(cohorts).mark_rect().encode( 
        x='CohortIndex:O',
        y=alt.Y('CohortMonth:O', sort='descending'),
        color=alt.Color('Customer Percentage:Q', scale=color_scale_percentage),
        tooltip=['CohortMonth:N', 'CohortIndex:O', 'Customer Percentage:Q']
    ).transform_filter(brush
    ).add_params(
        year_selection
    ).transform_filter(
        year_selection
    ).properties(
        width=700,
        height=500,
        title='Customer Order Retention Analysis (Cohort Heatmap) by Percentage'
    )

    heatmap2 = alt.Chart(cohorts).mark_rect().encode( 
            x='CohortIndex:O',
            y=alt.Y('CohortMonth:O', sort='descending'),
            color=alt.Color('Customer Count:Q', scale=color_scale_count),
            tooltip=['CohortMonth:N', 'CohortIndex:O', 'Customer Count:Q']
    ).transform_filter(brush
    ).add_params(
        year_selection
    ).transform_filter(
        year_selection
    ).properties(
        width=700,
        height=500,
        title='Customer Order Retention Analysis (Cohort Heatmap) by Count'
    )


    # Calculate the initial customers for each cohort
    initial_customers = cohorts[cohorts['CohortIndex'] == 0][['CohortMonth', 'Customer Count']]
    initial_customers.columns = ['CohortMonth', 'InitialCustomers']

    # Merge the initial customers back to cohorts DataFrame
    cohorts = pd.merge(cohorts, initial_customers, on='CohortMonth', how='left')

    # Calculate the retention percentage
    cohorts['Retention'] = cohorts['Customer Count'] / cohorts['InitialCustomers'] * 100

    # Create a line plot for retention percentage
    line_chart = alt.Chart(cohorts).mark_line().encode(
        x='CohortIndex:O',
        y='Retention:Q',
        color='CohortMonth:N',
        tooltip=['CohortMonth:N', 'CohortIndex:O', 'Retention:Q']
    ).properties(
        width=700,
        height=500,
        title='Customer Order Retention Analysis (Cohort Line Plot)'
    ).transform_filter(brush
    ).add_params(
        year_selection
    ).transform_filter(
        year_selection
    ).properties(
        width=700,
        height=500,
        title='Customer Order Retention Analysis (Cohort Heatmap) by Percentage'
    )

    map = alt.hconcat(heatmap,heatmap2).resolve_legend('independent')
    date_retention = alt.hconcat(date_chart,line_chart).resolve_legend('independent')
    final = alt.vconcat(map,date_retention)
    return final.to_json()