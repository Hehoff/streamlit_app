
import streamlit as st
import pandas as pd
import datetime as dt
import plotly.graph_objects as go


st.set_page_config(layout='wide')

header = st.container()
csv_upload = st.container()
chart1 = st.container()
chart2 = st.container()
chart3 = st.container()

with header:
    st.title('Interactive Grocery Sales Dashboard')
    st.text('The follwoing charts show the visualisation of a grocery data set in 2016 from a supermarket chain in Equador.')

with csv_upload:
    st.header('CSV File Uploader')

    csv = st.file_uploader('Select your csv-file with your sales data')

    if csv is not None:
        subset = pd.read_csv(csv)
        st.text('This is a first impression of your data table')
        st.write(subset.head())

with chart1:
    st.header('Personal Planning Chart')
    st.text('In the following, you can see the development of the total daily sales of the individual stores over time. The historical trends provide information for staff planning, as it becomes clear which stores sell more and, for example, in which months, weeks or weekdays the most products are sold.')

    #personal = subset.groupby(by = ['date', 'store_nbr'])['unit_sales'].agg('sum').reset_index()
    personal = subset.groupby(by = ['date', 'store_nbr'])['unit_sales'].agg('sum').reset_index()

    store_id = st.selectbox("Select your store", personal.store_nbr.drop_duplicates())
    data_store_id = personal[personal.store_nbr == store_id]
    st.write('You selected:', store_id)

    fig = go.Figure(data=go.Scatter(x=data_store_id.date, y=data_store_id.unit_sales))
    fig.update_layout(title='Unit Sales per Date for Store {store_id}'.format(store_id=store_id),
                   yaxis_title='Sales in 1.000')
    st.write(fig)

with chart2:
    st.header('Item Boxplot-Chart')
    st.text('In the following, you can create and compare a boxplot for up to three exemplary items. This provides information about the quantity sold of the corresponding item.')

    mask = subset['item_nbr'].isin([564534, 315220, 2010329])
    subset_2 = subset.loc[mask]

    item_id = st.multiselect("Select your item",subset_2.item_nbr.drop_duplicates())
    st.write('You selected:', item_id)

    if len(item_id) == 1:
        item1 = subset_2[subset_2.item_nbr == item_id[0]]

        iq_1 = ((item1['unit_sales'].quantile(0.75) - item1['unit_sales'].quantile(0.25))*3)+item1['unit_sales'].quantile(0.75)

        fig = go.Figure()
        fig.add_trace(go.Box(y=item1.unit_sales, name=item_id[0]))

        fig.update_layout(title='Boxplots for Item-IDs {item_1}'.format(item_1=item_id[0]),
                           yaxis_title='Unit sales in 1.000')
        st.write(fig)

    elif len(item_id) == 2:
        item1 = subset_2[subset_2.item_nbr == item_id[0]]
        item2 = subset_2[subset_2.item_nbr == item_id[1]]

        iq_1 = ((item1['unit_sales'].quantile(0.75) - item1['unit_sales'].quantile(0.25))*3)+item1['unit_sales'].quantile(0.75)
        iq_2 = ((item2['unit_sales'].quantile(0.75) - item2['unit_sales'].quantile(0.25))*3)+item2['unit_sales'].quantile(0.75)

        fig = go.Figure()
        fig.add_trace(go.Box(y=item1.unit_sales,name=item_id[0]))
        fig.add_trace(go.Box(y=item2.unit_sales,name=item_id[1]))

        if iq_1>iq_2:
            fig.update_layout(yaxis_range=[0,iq_1])
        else:
            fig.update_layout(yaxis_range=[0,iq_2])

        fig.update_layout(title='Boxplots for Item-IDs {item_1} and {item_2}'.format(item_1=item_id[0], item_2=item_id[1]),
                           yaxis_title='Unit sales in 1.000')
        st.write(fig)

    elif len(item_id) == 3:
        item1 = subset_2[subset_2.item_nbr == item_id[0]]
        item2 = subset_2[subset_2.item_nbr == item_id[1]]
        item3 = subset_2[subset_2.item_nbr == item_id[2]]

        iq_1 = ((item1['unit_sales'].quantile(0.75) - item1['unit_sales'].quantile(0.25))*3)+item1['unit_sales'].quantile(0.75)
        iq_2 = ((item2['unit_sales'].quantile(0.75) - item2['unit_sales'].quantile(0.25))*3)+item2['unit_sales'].quantile(0.75)
        iq_3 = ((item3['unit_sales'].quantile(0.75) - item3['unit_sales'].quantile(0.25))*3)+item3['unit_sales'].quantile(0.75)

        fig = go.Figure()
        fig.add_trace(go.Box(y=item1.unit_sales,name=item_id[0]))
        fig.add_trace(go.Box(y=item2.unit_sales,name=item_id[1]))
        fig.add_trace(go.Box(y=item3.unit_sales,name=item_id[2]))


        if (iq_1>iq_2 and iq_1>iq_3):
            fig.update_layout(yaxis_range=[0,iq_1])
        elif (iq_2>iq_1 and iq_2>iq_3):
            fig.update_layout(yaxis_range=[0,iq_2])
        else:
            fig.update_layout(yaxis_range=[0,iq_3])

        fig.update_layout(title='Boxplots for Item-IDs {item_1}, {item_2} and {item_3}'.format(item_1=item_id[0], item_2=item_id[1], item_3=item_id[2]),
                           yaxis_title='Unit sales in 1.000')
        st.write(fig)

# Für 1 und 3 auch machen

with chart3:
    st.header('On/Off Promotion Chart')
    st.text('The on/off promotion chart shows for a selected week the average amount of items sold on and off promotion. The comparison can be an indicator of whether the promotion was successful in that week.')

    subset['date'] =  pd.to_datetime(subset['date'])
    subset['Week_Number'] = subset['date'].dt.week
    subset_3 = subset.groupby(['Week_Number', 'onpromotion']).agg({'unit_sales': 'sum', 'item_nbr': 'nunique'}).reset_index()
    subset_3['unit_sales_per_item']=subset_3['unit_sales']/subset_3['item_nbr']

    barchart1 = subset_3.loc[subset_3.onpromotion == False]
    barchart2 = subset_3.loc[subset_3.onpromotion == True]

    week = st.select_slider('Select the week', options=subset_3.Week_Number)

    fig = go.Figure(data=[
    go.Bar(name='On Promotion', x=barchart2[barchart2.Week_Number == week].Week_Number, y=barchart2[barchart2.Week_Number == week].unit_sales_per_item),
    go.Bar(name='Off Promotion', x=barchart1[barchart1.Week_Number == week].Week_Number, y=barchart1[barchart1.Week_Number == week].unit_sales_per_item)
    ])
    # Change the bar mode
    fig.update_layout(barmode='group', title='On/Off Promotion', yaxis_title='Mean of unit sales per item' )
    st.write(fig)





    #chart1_data = personal[personal.store_nbr == store_id]

    #fig = go.Figure(data=go.Scatter(x=chart1_data.date, y=chart1_data.unit_sales))
    #fig.update_layout(title='Unit Sales per Date for Store {store_id}'.format(store_id=store_id),
    #               yaxis_title='Sales in 1.000')
    #fig.show()

    #subset = pd.read_csv('subset.csv')

    #mask = subset['item_nbr'].isin([564534, 315220, 2010329])
    #subset_2 = subset.loc[mask]


# subset["date"] = pd.to_datetime(subset['date'])
# subset["date"] = subset['date'].values.astype('int64')

#subset = subset.rename(columns={'date':'index'}).set_index('index')

#unit_sales_sel = subset.store_nbr.unique()

#select_sales = st.multiselect("select stores", unit_sales_sel)

#subset_filtered = subset[subset.store_nbr.isin(select_sales)]

#st.dataframe(subset_filtered)
#st.line_chart(data=subset_filtered)
