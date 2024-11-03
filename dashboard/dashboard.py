import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter
from babel.numbers import format_currency

sns.set_theme(style='darkgrid')
# Opsi untuk menyembunyikan peringatan deprecation
# st.set_option('deprecation.showPyplotGlobalUse', False)

# Membaca Dataset
datetime_fields = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
                   "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
order_data = pd.read_csv("https://raw.githubusercontent.com/Fiqry-Wahyu-Diky/project-dicoding-data-analis/main/data/all_data.csv")
order_data.sort_values("order_approved_at", inplace=True)
order_data.reset_index(drop=True, inplace=True)

# Dataset Geolokasi
geo_data = pd.read_csv("https://raw.githubusercontent.com/Fiqry-Wahyu-Diky/project-dicoding-data-analis/main/data/geolocation.csv")
unique_customers = geo_data.drop_duplicates(subset='customer_unique_id')

# Konversi kolom tanggal ke tipe datetime
for field in datetime_fields:
    order_data[field] = pd.to_datetime(order_data[field])

start_range = order_data["order_approved_at"].min()
end_range = order_data["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.title("Fiqry Wahyu Diky W.")
    # Gambar logo (dapat diaktifkan dengan menghapus komentar)
    # st.image("https://raw.githubusercontent.com/Fiqry-Wahyu-Diky/project-dicoding-data-analis/main/dashboard/gcl.png")

    # Pilihan rentang tanggal
    start_date, end_date = st.date_input(
        "Select Date Range",
        value=[start_range, end_range],
        min_value=start_range,
        max_value=end_range
    )

# Filter berdasarkan tanggal yang dipilih
filtered_data = order_data[(order_data["order_approved_at"] >= str(start_date)) & (order_data["order_approved_at"] <= str(end_date))]

# Membuat objek analyzer dan plotter
analyzer = DataAnalyzer(filtered_data)
map_plotter = BrazilMapPlotter(unique_customers, plt, mpimg, urllib, st)

# Analisis Data
daily_orders = analyzer.create_daily_orders_df()
spending_summary = analyzer.create_sum_spend_df()
item_summary = analyzer.create_sum_order_items_df()
review_data, popular_score = analyzer.review_score_df()
state_data, popular_state = analyzer.create_bystate_df()
order_status_data, frequent_status = analyzer.create_order_status()

# Header Dashboard
st.header("E-Commerce Dashboard :convenience_store:")

# Pesanan Harian
st.subheader("Daily Orders")
col1, col2 = st.columns(2)

with col1:
    order_count = daily_orders["order_count"].sum()
    st.markdown(f"Total Orders: **{order_count}**")

with col2:
    revenue = format_currency(daily_orders["revenue"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Revenue: **{revenue}**")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    daily_orders["order_approved_at"],
    daily_orders["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

# Pengeluaran Pelanggan
st.subheader("Customer Spending")
col1, col2 = st.columns(2)

with col1:
    total_spending = format_currency(spending_summary["total_spend"].sum(), "IDR", locale="id_ID")
    st.markdown(f"Total Spending: **{total_spending}**")

with col2:
    average_spending = format_currency(spending_summary["total_spend"].mean(), "IDR", locale="id_ID")
    st.markdown(f"Average Spending: **{average_spending}**")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(
    spending_summary["order_approved_at"],
    spending_summary["total_spend"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

# Item Pesanan
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items_ordered = item_summary["product_count"].sum()
    st.markdown(f"Total Items Ordered: **{total_items_ordered}**")

with col2:
    avg_items_per_order = item_summary["product_count"].mean()
    st.markdown(f"Average Items per Order: **{avg_items_per_order:.2f}**")

fig, axes = plt.subplots(1, 2, figsize=(18, 10))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="product_count", y="product_category_name_english", data=item_summary.head(5), palette=colors, ax=axes[0])
axes[0].set_title("Most Sold Products")
sns.barplot(x="product_count", y="product_category_name_english",
            data=item_summary.sort_values(by="product_count", ascending=True).head(5), palette=colors, ax=axes[1])
axes[1].set_title("Least Sold Products")
axes[1].invert_xaxis()
st.pyplot(fig)

# Skor Ulasan
st.subheader("Review Scores")
col1, col2 = st.columns(2)

with col1:
    avg_review = review_data.mean()
    st.markdown(f"Average Review Score: **{avg_review:.2f}**")

with col2:
    most_frequent_review = review_data.index[0]
    st.markdown(f"Most Frequent Review Score: **{most_frequent_review}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=review_data.index, y=review_data.values,
            palette=["#068DA9" if score == popular_score else "#D3D3D3" for score in review_data.index])
plt.title("Customer Ratings")
st.pyplot(fig)

# Demografi Pelanggan
st.subheader("Customer Demographics")
tab1, tab2, tab3 = st.tabs(["By State", "Order Status", "Geolocation"])

with tab1:
    most_frequent_state = state_data["customer_state"].iloc[0]
    st.markdown(f"Most Common State: **{most_frequent_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state_data["customer_state"], y=state_data["customer_count"],
                palette=["#068DA9" if s == most_frequent_state else "#D3D3D3" for s in state_data["customer_state"]])
    plt.title("Customers by State")
    st.pyplot(fig)

with tab2:
    frequent_order_status = order_status_data.index[0]
    st.markdown(f"Most Common Order Status: **{frequent_order_status}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=order_status_data.index, y=order_status_data.values,
                palette=["#068DA9" if status == frequent_status else "#D3D3D3" for status in order_status_data.index])
    plt.title("Order Status Distribution")
    st.pyplot(fig)

with tab3:
    map_plotter.plot()

    with st.expander("Explanation"):
        st.write("Map shows that most customers are located in the southeastern and southern regions, with concentrations in capitals such as São Paulo and Rio de Janeiro.")
