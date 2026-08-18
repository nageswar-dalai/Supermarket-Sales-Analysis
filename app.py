
import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Supermarket Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL DARK THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 100%);
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

h1 {
    color: #f8fafc !important;
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    margin-bottom: 0.2rem;
}

h2 {
    color: #e2e8f0 !important;
    font-weight: 700 !important;
}

h3 {
    color: #cbd5e1 !important;
}

p {
    color: #cbd5e1;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        rgba(30, 41, 59, 0.95),
        rgba(15, 23, 42, 0.95)
    );
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 22px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: #f8fafc !important;
    font-weight: 800;
}

[data-testid="stSidebar"] {
    background: #0b1220;
    border-right: 1px solid #334155;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] label {
    color: #e2e8f0 !important;
}

[data-testid="stSidebar"] p {
    color: #94a3b8 !important;
}

.stDownloadButton > button {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: #1d4ed8;
}

hr {
    border-color: #334155;
}

.insight-card {
    background: linear-gradient(
        145deg,
        rgba(30, 41, 59, 0.95),
        rgba(15, 23, 42, 0.95)
    );
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.20);
}

.insight-title {
    color: #94a3b8;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 8px;
}

.insight-value {
    color: #f8fafc;
    font-size: 1.25rem;
    font-weight: 700;
}

.insight-small {
    color: #cbd5e1;
    font-size: 0.9rem;
    margin-top: 8px;
}

.section-note {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: -10px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("supermarket_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.month_name()

# =========================================================
# HEADER
# =========================================================

st.title("🛒 Supermarket Sales Analytics")

st.markdown(
    "### Interactive Business Intelligence Dashboard"
)

st.markdown(
    """
    <p class="section-note">
    Analyze sales performance, customer behavior, product performance,
    payment preferences and business trends.
    </p>
    """,
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the dataset."
)

branch_filter = st.sidebar.multiselect(
    "🏢 Branch",
    options=sorted(df["Branch"].unique()),
    default=sorted(df["Branch"].unique())
)

city_filter = st.sidebar.multiselect(
    "📍 City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

product_filter = st.sidebar.multiselect(
    "🛍️ Product Line",
    options=sorted(df["Product line"].unique()),
    default=sorted(df["Product line"].unique())
)

customer_filter = st.sidebar.multiselect(
    "👥 Customer Type",
    options=sorted(df["Customer type"].unique()),
    default=sorted(df["Customer type"].unique())
)

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df["Branch"].isin(branch_filter))
    & (df["City"].isin(city_filter))
    & (df["Product line"].isin(product_filter))
    & (df["Customer type"].isin(customer_filter))
]

# =========================================================
# EMPTY DATA CHECK
# =========================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data available for the selected filters. "
        "Please select at least one option from each filter."
    )

    st.stop()

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_quantity = filtered_df["Quantity"].sum()

gross_income = filtered_df["gross income"].sum()

avg_rating = filtered_df["Rating"].mean()

total_transactions = len(filtered_df)

# =========================================================
# KPI CARDS
# =========================================================

st.markdown("---")

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

k2.metric(
    "📦 Total Quantity",
    f"{total_quantity:,}"
)

k3.metric(
    "💵 Gross Income",
    f"${gross_income:,.2f}"
)

k4.metric(
    "⭐ Average Rating",
    f"{avg_rating:.2f}"
)

st.caption(
    f"Showing {total_transactions:,} transactions based on current filters."
)

# =========================================================
# CHART THEME FUNCTION
# =========================================================

def style_chart(fig):

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#e2e8f0"
        ),
        title_font=dict(
            size=20,
            color="#f8fafc"
        ),
        legend=dict(
            font=dict(
                color="#cbd5e1"
            )
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    fig.update_xaxes(
        gridcolor="rgba(148,163,184,0.15)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    fig.update_yaxes(
        gridcolor="rgba(148,163,184,0.15)",
        zerolinecolor="rgba(148,163,184,0.15)"
    )

    return fig

# =========================================================
# SALES OVERVIEW
# =========================================================

st.markdown("---")

st.header("📊 Sales Overview")

st.markdown(
    '<p class="section-note">Monthly sales performance based on selected filters.</p>',
    unsafe_allow_html=True
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly_sales = (
    filtered_df
    .groupby("Month_Name")["Sales"]
    .sum()
    .reindex(month_order)
    .dropna()
    .reset_index()
)

fig_month = px.line(
    monthly_sales,
    x="Month_Name",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Total Sales"
)

fig_month = style_chart(fig_month)

st.plotly_chart(
    fig_month,
    use_container_width=True
)

# =========================================================
# PRODUCT & BRANCH PERFORMANCE
# =========================================================

st.markdown("---")

st.header("🏆 Product & Branch Performance")

col1, col2 = st.columns(2)

# Product Sales

product_sales = (
    filtered_df
    .groupby("Product line")["Sales"]
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
    yaxis_title="Product Line"
)

fig_product = style_chart(fig_product)

col1.plotly_chart(
    fig_product,
    use_container_width=True
)

# Branch Sales

branch_sales = (
    filtered_df
    .groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
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
    yaxis_title="Total Sales"
)

fig_branch = style_chart(fig_branch)

col2.plotly_chart(
    fig_branch,
    use_container_width=True
)

# =========================================================
# CUSTOMER & PAYMENT ANALYSIS
# =========================================================

st.markdown("---")

st.header("👥 Customer & Payment Analysis")

col1, col2 = st.columns(2)

# Customer Type

customer_sales = (
    filtered_df
    .groupby("Customer type")["Sales"]
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

fig_customer = style_chart(fig_customer)

col1.plotly_chart(
    fig_customer,
    use_container_width=True
)

# Payment Method

payment_sales = (
    filtered_df
    .groupby("Payment")["Sales"]
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
    yaxis_title="Total Sales"
)

fig_payment = style_chart(fig_payment)

col2.plotly_chart(
    fig_payment,
    use_container_width=True
)

# =========================================================
# CUSTOMER DEMOGRAPHICS & RATING
# =========================================================

st.markdown("---")

st.header("👤 Customer Demographics & Rating")

col1, col2 = st.columns(2)

# Gender Sales

gender_sales = (
    filtered_df
    .groupby("Gender")["Sales"]
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
    yaxis_title="Total Sales"
)

fig_gender = style_chart(fig_gender)

col1.plotly_chart(
    fig_gender,
    use_container_width=True
)

# Rating

rating_product = (
    filtered_df
    .groupby("Product line")["Rating"]
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
    yaxis_title="Product Line"
)

fig_rating = style_chart(fig_rating)

col2.plotly_chart(
    fig_rating,
    use_container_width=True
)

# =========================================================
# BUSINESS INSIGHTS
# =========================================================

st.markdown("---")

st.header("💡 Key Business Insights")

product_group = (
    filtered_df
    .groupby("Product line")["Sales"]
    .sum()
)

branch_group = (
    filtered_df
    .groupby("Branch")["Sales"]
    .sum()
)

customer_group = (
    filtered_df
    .groupby("Customer type")["Sales"]
    .sum()
)

payment_group = (
    filtered_df
    .groupby("Payment")["Sales"]
    .sum()
)

best_product = product_group.idxmax()
best_product_sales = product_group.max()

best_branch = branch_group.idxmax()
best_branch_sales = branch_group.max()

best_customer = customer_group.idxmax()

best_payment = payment_group.idxmax()

# Insight cards

i1, i2, i3 = st.columns(3)

with i1:

    st.markdown(
        f"""
        <div class="insight-card">

        <div class="insight-title">
        🏆 TOP PRODUCT LINE
        </div>

        <div class="insight-value">
        {best_product}
        </div>

        <div class="insight-small">
        Sales: ${best_product_sales:,.2f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with i2:

    st.markdown(
        f"""
        <div class="insight-card">

        <div class="insight-title">
        🏢 TOP BRANCH
        </div>

        <div class="insight-value">
        Branch {best_branch}
        </div>

        <div class="insight-small">
        Sales: ${best_branch_sales:,.2f}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with i3:

    st.markdown(
        f"""
        <div class="insight-card">

        <div class="insight-title">
        👥 TOP CUSTOMER TYPE
        </div>

        <div class="insight-value">
        {best_customer}
        </div>

        <div class="insight-small">
        Top Payment: {best_payment}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# BUSINESS RECOMMENDATIONS
# =========================================================

st.markdown("### 📌 Business Recommendations")

recommendations = [
    f"Focus marketing efforts on **{best_product}**, the highest-selling product line.",
    f"Analyze the strategies of **Branch {best_branch}**, the strongest-performing branch.",
    f"Strengthen loyalty initiatives for the **{best_customer}** customer segment.",
    f"Monitor **{best_payment}** payment usage and maintain convenient payment options."
]

for recommendation in recommendations:

    st.markdown(
        f"• {recommendation}"
    )

# =========================================================
# EXPORT DATA
# =========================================================

st.markdown("---")

st.header("📥 Export Data")

st.markdown(
    '<p class="section-note">Download the currently filtered dataset for further analysis.</p>',
    unsafe_allow_html=True
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv_data,
    file_name="supermarket_filtered_data.csv",
    mime="text/csv"
)

# =========================================================
# ABOUT PROJECT
# =========================================================

st.markdown("---")

st.header("📌 About This Project")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### 🎯 Project Objective

        This dashboard analyzes supermarket sales data to identify:

        - Sales performance and trends
        - Best-performing product lines
        - Branch-wise performance
        - Customer purchasing behavior
        - Payment preferences
        - Gender-wise sales patterns
        - Customer ratings
        """
    )

with col2:

    st.markdown(
        """
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
        """
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:20px;">
        🛒 <b>Supermarket Sales Analytics</b><br>
        Built with Python, Pandas, Plotly & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)

