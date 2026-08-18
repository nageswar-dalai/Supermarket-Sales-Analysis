import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Professional Dark Blue Theme
# -----------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    color: #f8fafc;
    font-size: 2.7rem;
    font-weight: 800;
}

h2 {
    color: #e2e8f0;
    font-weight: 700;
}

h3 {
    color: #cbd5e1;
}

p {
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.9);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8;
}

[data-testid="stMetricValue"] {
    color: #f8fafc;
    font-weight: 800;
}

[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label {
    color: #e2e8f0;
}

.stSelectbox,
.stMultiSelect {
    color: #f8fafc;
}

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)

# Load data
df = pd.read_csv("supermarket_sales.csv")

# Convert date
df["Date"] = pd.to_datetime(df["Date"])

# Month columns
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()

st.title("🛒 Supermarket Sales Analytics")
st.subheader("Interactive Business Intelligence Dashboard")

st.write(
    "Analyze sales performance, customer behavior, product performance "
    "and business trends."
)

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("🔎 Dashboard Filters")

branch_filter = st.sidebar.multiselect(
    "Select Branch",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

city_filter = st.sidebar.multiselect(
    "Select City",
    options=df["City"].unique(),
    default=df["City"].unique()
)

product_filter = st.sidebar.multiselect(
    "Select Product Line",
    options=df["Product line"].unique(),
    default=df["Product line"].unique()
)

customer_filter = st.sidebar.multiselect(
    "Customer Type",
    options=df["Customer type"].unique(),
    default=df["Customer type"].unique()
)

# Apply filters
filtered_df = df[
    (df["Branch"].isin(branch_filter)) &
    (df["City"].isin(city_filter)) &
    (df["Product line"].isin(product_filter)) &
    (df["Customer type"].isin(customer_filter))
]

# -----------------------------
# KPI Calculations
# -----------------------------

total_sales = filtered_df["Sales"].sum()
total_quantity = filtered_df["Quantity"].sum()
gross_income = filtered_df["gross income"].sum()
avg_rating = filtered_df["Rating"].mean()

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📦 Total Quantity",
    f"{total_quantity:,}"
)

col3.metric(
    "💵 Gross Income",
    f"${gross_income:,.2f}"
)

col4.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)

# -----------------------------
# Sales Overview
# -----------------------------

st.markdown("---")
st.header("📊 Sales Overview")

monthly_sales = (
    filtered_df
    .groupby("Month_Name", sort=False)["Sales"]
    .sum()
    .reset_index()
)

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

monthly_sales["Month_Name"] = pd.Categorical(
    monthly_sales["Month_Name"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month_Name")

fig_month = px.line(
    monthly_sales,
    x="Month_Name",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Sales",
    template="plotly_white"
)

st.plotly_chart(fig_month, use_container_width=True)

# -----------------------------
# Product & Branch Performance
# -----------------------------

st.markdown("---")
st.header("🏆 Product & Branch Performance")

col1, col2 = st.columns(2)

# Product Line Sales
product_sales = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig_product = px.bar(
    product_sales,
    x="Sales",
    y="Product line",
    orientation="h",
    title="Sales by Product Line",
    text_auto=".2s"
)

fig_product.update_layout(
    xaxis_title="Total Sales",
    yaxis_title="Product Line",
    template="plotly_white"
)

col1.plotly_chart(
    fig_product,
    use_container_width=True
)


# Branch Sales
branch_sales = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .reset_index()
)

fig_branch = px.bar(
    branch_sales,
    x="Branch",
    y="Sales",
    title="Sales by Branch",
    text_auto=".2s"
)

fig_branch.update_layout(
    xaxis_title="Branch",
    yaxis_title="Total Sales",
    template="plotly_white"
)

col2.plotly_chart(
    fig_branch,
    use_container_width=True
)

# -----------------------------
# Customer & Payment Analysis
# -----------------------------

st.markdown("---")
st.header("👥 Customer & Payment Analysis")

col1, col2 = st.columns(2)

# Customer Type Sales
customer_sales = (
    filtered_df.groupby("Customer type")["Sales"]
    .sum()
    .reset_index()
)

fig_customer = px.pie(
    customer_sales,
    names="Customer type",
    values="Sales",
    title="Sales by Customer Type",
    hole=0.45
)

col1.plotly_chart(
    fig_customer,
    use_container_width=True
)


# Payment Method Sales
payment_sales = (
    filtered_df.groupby("Payment")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_payment = px.bar(
    payment_sales,
    x="Payment",
    y="Sales",
    title="Sales by Payment Method",
    text_auto=".2s"
)

fig_payment.update_layout(
    xaxis_title="Payment Method",
    yaxis_title="Total Sales",
    template="plotly_white"
)

col2.plotly_chart(
    fig_payment,
    use_container_width=True
)

# -----------------------------
# Customer Demographics & Rating
# -----------------------------

st.markdown("---")
st.header("👤 Customer Demographics & Rating")

col1, col2 = st.columns(2)

# Gender-wise Sales
gender_sales = (
    filtered_df.groupby("Gender")["Sales"]
    .sum()
    .reset_index()
)

fig_gender = px.bar(
    gender_sales,
    x="Gender",
    y="Sales",
    title="Sales by Gender",
    text_auto=".2s"
)

fig_gender.update_layout(
    xaxis_title="Gender",
    yaxis_title="Total Sales",
    template="plotly_white"
)

col1.plotly_chart(
    fig_gender,
    use_container_width=True
)


# Product Line Rating
rating_product = (
    filtered_df.groupby("Product line")["Rating"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig_rating = px.bar(
    rating_product,
    x="Rating",
    y="Product line",
    orientation="h",
    title="Average Rating by Product Line",
    text_auto=".2f"
)

fig_rating.update_layout(
    xaxis_title="Average Rating",
    yaxis_title="Product Line",
    template="plotly_white"
)

col2.plotly_chart(
    fig_rating,
    use_container_width=True
)

# -----------------------------
# Business Insights
# -----------------------------

st.markdown("---")
st.header("💡 Key Business Insights")

# Best Product Line
best_product = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .idxmax()
)

best_product_sales = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .max()
)

# Best Branch
best_branch = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .idxmax()
)

best_branch_sales = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .max()
)

# Best Customer Type
best_customer = (
    filtered_df.groupby("Customer type")["Sales"]
    .sum()
    .idxmax()
)

# Best Payment Method
best_payment = (
    filtered_df.groupby("Payment")["Sales"]
    .sum()
    .idxmax()
)

# Best Gender
best_gender = (
    filtered_df.groupby("Gender")["Sales"]
    .sum()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        f"🏆 **Top Product Line**\n\n"
        f"{best_product}\n\n"
        f"Sales: ${best_product_sales:,.2f}"
    )

with col2:
    st.success(
        f"🏢 **Top Branch**\n\n"
        f"Branch {best_branch}\n\n"
        f"Sales: ${best_branch_sales:,.2f}"
    )

with col3:
    st.warning(
        f"👥 **Top Customer Type**\n\n"
        f"{best_customer}\n\n"
        f"Payment Preference: {best_payment}"
    )

st.markdown("### 📌 Business Recommendations")

st.write(
    f"• Focus on **{best_product}** because it generates the highest sales."
)

st.write(
    f"• **Branch {best_branch}** is currently the strongest-performing branch."
)

st.write(
    f"• The **{best_customer}** customer segment contributes the most sales."
)

st.write(
    f"• **{best_payment}** is the most frequently preferred payment method "
    f"based on sales."
)

# -----------------------------
# Download Filtered Data
# -----------------------------

st.markdown("---")
st.header("📥 Export Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="supermarket_filtered_data.csv",
    mime="text/csv"
)

# -----------------------------
# About Project
# -----------------------------

st.markdown("---")
st.header("📌 About This Project")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Project Objective

    This dashboard analyzes supermarket sales data to identify:

    - Sales performance and trends
    - Best-performing product lines
    - Branch-wise performance
    - Customer purchasing behavior
    - Payment preferences
    - Gender-wise sales patterns
    - Customer ratings
    """)

with col2:
    st.markdown("""
    ### 🛠️ Technologies Used

    - **Python**
    - **Pandas**
    - **Plotly**
    - **Streamlit**
    - **Data Analysis**
    - **Exploratory Data Analysis (EDA)**

    ### 📊 Dataset

    Supermarket Sales Dataset containing
    transaction, customer, product and sales information.
    """)