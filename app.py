import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOGIN
# =========================

USERNAME = "admin"
PASSWORD = "ecommerce123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("E-Commerce Analytics Dashboard")

    username = st.text_input("User ID")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid User ID or Password")

    st.stop()

# =========================
# LOAD DATA
# =========================

st.sidebar.header("Upload Project Data")

orders_file = st.sidebar.file_uploader(
    "Upload orders.csv",
    type=["csv"],
    key="orders_file"
)

website_sessions_file = st.sidebar.file_uploader(
    "Upload website_sessions.csv",
    type=["csv"],
    key="website_sessions_file"
)

website_pageviews_file = st.sidebar.file_uploader(
    "Upload website_pageviews.csv",
    type=["csv"],
    key="website_pageviews_file"
)

order_item_refunds_file = st.sidebar.file_uploader(
    "Upload order_item_refunds.csv",
    type=["csv"],
    key="order_item_refunds_file"
)

order_items_file = st.sidebar.file_uploader(
    "Upload order_items.csv",
    type=["csv"],
    key="order_items_file"
)

products_file = st.sidebar.file_uploader(
    "Upload products.csv",
    type=["csv"],
    key="products_file"
)

all_files_uploaded = all([
    orders_file,
    website_sessions_file,
    website_pageviews_file,
    order_item_refunds_file,
    order_items_file,
    products_file
])

if not all_files_uploaded:
    st.info(
        "Please upload all six project CSV files from the sidebar "
        "to open the dashboard. The files are not stored in the GitHub repository."
    )
    st.stop()

orders = pd.read_csv(orders_file)
website_sessions = pd.read_csv(website_sessions_file)
website_pageviews = pd.read_csv(website_pageviews_file)
order_item_refunds = pd.read_csv(order_item_refunds_file)
order_items = pd.read_csv(order_items_file)
products = pd.read_csv(products_file)

model = joblib.load("ecommerce_conversion_model.pkl")



# =========================
# CALCULATE KPIs
# =========================

total_revenue = orders["price_usd"].sum()
total_cogs = orders["cogs_usd"].sum()
total_profit = total_revenue - total_cogs

profit_margin = (total_profit / total_revenue) * 100

total_orders = orders["order_id"].nunique()
total_customers = orders["user_id"].nunique()
total_sessions = website_sessions["website_session_id"].nunique()

conversion_rate = (total_orders / total_sessions) * 100
revenue_per_session = total_revenue / total_sessions

total_refund = order_item_refunds["refund_amount_usd"].sum()

# =========================
# TITLE
# =========================

st.title("E-Commerce Analytics Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Executive Overview",
        "Website Performance",
        "Sales & Product Performance",
        "Customer Analysis",
        "Refund Analysis",
        "Business Insights",
        "Conversion Prediction"
    ]
)

# =========================
# EXECUTIVE OVERVIEW
# =========================

if page == "Executive Overview":

    st.header("Executive Overview")

    # KPI ROW 1
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "Total COGS",
        f"${total_cogs:,.2f}"
    )

    col3.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

    col4.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )

    st.divider()

    # KPI ROW 2
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col2.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col3.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

    col4.metric(
        "Revenue per Session",
        f"${revenue_per_session:.2f}"
    )

    st.divider()

    # REFUND
    st.metric(
        "Total Refund Amount",
        f"${total_refund:,.2f}"
    )

    st.subheader("Key Business Metrics")

    summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total COGS",
            "Total Profit",
            "Profit Margin",
            "Total Orders",
            "Total Customers",
            "Total Sessions",
            "Conversion Rate",
            "Revenue per Session",
            "Total Refund Amount"
        ],
        "Value": [
            total_revenue,
            total_cogs,
            total_profit,
            f"{profit_margin:.2f}%",
            total_orders,
            total_customers,
            total_sessions,
            f"{conversion_rate:.2f}%",
            f"${revenue_per_session:.2f}",
            total_refund
        ]
    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

# =========================
# OTHER PAGES
# =========================

elif page == "Website Performance":

    st.header("Website Performance")

    # =========================
    # WEBSITE KPIs
    # =========================

    total_pageviews = website_pageviews["website_pageview_id"].nunique()

    pageviews_per_session = total_pageviews / total_sessions

    repeat_sessions = (
        website_sessions["is_repeat_session"] == 1
    ).sum()

    repeat_session_rate = (
        repeat_sessions / total_sessions
    ) * 100

    # Bounce Rate
    sessions_with_pageviews = (
        website_pageviews["website_session_id"].nunique()
    )

    single_page_sessions = (
        website_pageviews.groupby("website_session_id")
        .size()
    )

    bounced_sessions = (
        single_page_sessions == 1
    ).sum()

    bounce_rate = (
        bounced_sessions / sessions_with_pageviews
    ) * 100

    # =========================
    # KPI CARDS
    # =========================

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Sessions",
        f"{total_sessions:,}"
    )

    col2.metric(
        "Total Pageviews",
        f"{total_pageviews:,}"
    )

    col3.metric(
        "Pageviews per Session",
        f"{pageviews_per_session:.2f}"
    )

    col4.metric(
        "Conversion Rate",
        f"{conversion_rate:.2f}%"
    )

    col5.metric(
        "Revenue per Session",
        f"${revenue_per_session:.2f}"
    )

    # =========================
    # SECOND KPI ROW
    # =========================

    col1, col2 = st.columns(2)

    col1.metric(
        "Repeat Session Rate",
        f"{repeat_session_rate:.2f}%"
    )

    col2.metric(
        "Bounce Rate",
        f"{bounce_rate:.2f}%"
    )

    st.divider()

    # =========================
    # DEVICE TYPE
    # =========================

    st.subheader("Sessions by Device Type")

    device_sessions = (
        website_sessions["device_type"]
        .value_counts()
        .reset_index()
    )

    device_sessions.columns = [
        "Device Type",
        "Sessions"
    ]

    st.bar_chart(
        device_sessions.set_index("Device Type")
    )

    # =========================
    # MARKETING SOURCE
    # =========================

    st.subheader("Sessions by Marketing Source")

    marketing_sessions = (
        website_sessions["utm_source"]
        .fillna("NULL")
        .value_counts()
        .reset_index()
    )

    marketing_sessions.columns = [
        "Marketing Source",
        "Sessions"
    ]

    st.bar_chart(
        marketing_sessions.set_index("Marketing Source")
    )

    # =========================
    # SESSIONS TREND
    # =========================

    st.subheader("Sessions Trend Over Time")

    website_sessions["created_at"] = pd.to_datetime(
        website_sessions["created_at"]
    )

    yearly_sessions = (
        website_sessions
        .groupby(website_sessions["created_at"].dt.year)
        ["website_session_id"]
        .nunique()
    )

    yearly_sessions.index.name = "Year"

    st.line_chart(yearly_sessions)

elif page == "Sales & Product Performance":

    st.header("Sales & Product Performance")

    # =========================
    # PRODUCT PERFORMANCE DATA
    # =========================

    product_performance = (
        order_items
        .merge(
            products[["product_id", "product_name"]],
            on="product_id",
            how="left"
        )
    )

    product_performance["profit"] = (
        product_performance["price_usd"]
        - product_performance["cogs_usd"]
    )

    # =========================
    # KPI CARDS
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"${order_items['price_usd'].sum():,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{order_items['order_id'].nunique():,}"
    )

    col3.metric(
        "Total Profit",
        f"${product_performance['profit'].sum():,.2f}"
    )

    st.divider()

    # =========================
    # TOP PRODUCTS BY SALES
    # =========================

    st.subheader("Top Products by Sales")

    top_products = (
        product_performance
        .groupby("product_name")["order_item_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_products)

    # =========================
    # TOP PRODUCTS BY PROFIT
    # =========================

    st.subheader("Top Products by Profit")

    top_profit_products = (
        product_performance
        .groupby("product_name")["profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(top_profit_products)

    # =========================
    # PRODUCT PERFORMANCE TABLE
    # =========================

    st.subheader("Product Performance")

    product_summary = (
        product_performance
        .groupby("product_name")
        .agg(
            Revenue=("price_usd", "sum"),
            COGS=("cogs_usd", "sum"),
            Profit=("profit", "sum"),
            Items_Sold=("order_item_id", "count")
        )
        .sort_values("Revenue", ascending=False)
        .reset_index()
    )

    st.dataframe(
        product_summary,
        use_container_width=True,
        hide_index=True
    )

elif page == "Customer Analysis":

    st.header("Customer Analysis")

    # =========================
    # CUSTOMER METRICS
    # =========================

    customer_orders = (
        orders.groupby("user_id")["order_id"]
        .nunique()
    )

    total_customers = customer_orders.count()

    repeat_customers = (
        customer_orders[customer_orders > 1].count()
    )

    repeat_customer_rate = (
        repeat_customers / total_customers
    ) * 100

    avg_orders_per_customer = (
        customer_orders.mean()
    )

    # =========================
    # KPI CARDS
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

    col2.metric(
        "Repeat Customers",
        f"{repeat_customers:,}"
    )

    col3.metric(
        "Repeat Customer Rate",
        f"{repeat_customer_rate:.2f}%"
    )

    st.divider()

    # =========================
    # ORDERS PER CUSTOMER
    # =========================

    st.subheader("Orders per Customer")

    orders_distribution = (
        customer_orders
        .value_counts()
        .sort_index()
    )

    orders_distribution.index.name = "Number of Orders"

    st.bar_chart(orders_distribution)

    st.divider()

    # =========================
    # TOP CUSTOMERS
    # =========================

    st.subheader("Top Customers by Orders")

    top_customers = (
        customer_orders
        .sort_values(ascending=False)
        .head(10)
    )

    top_customers.index = top_customers.index.astype(str)
    top_customers.index.name = "Customer ID"

    st.bar_chart(top_customers)

    # =========================
    # CUSTOMER SUMMARY
    # =========================

    st.subheader("Top Customers Summary")

    customer_summary = (
        orders.groupby("user_id")
        .agg(
            Orders=("order_id", "nunique"),
            Revenue=("price_usd", "sum")
        )
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        customer_summary,
        use_container_width=True,
        hide_index=True
    )

elif page == "Refund Analysis":

    st.header("Refund Analysis")

    # =========================
    # REFUND ANALYSIS
    # =========================

    refund_data = (
        order_item_refunds
        .merge(
            order_items[
                ["order_item_id", "product_id", "price_usd"]
            ],
            on="order_item_id",
            how="left"
        )
        .merge(
            products[
                ["product_id", "product_name"]
            ],
            on="product_id",
            how="left"
        )
    )

    total_refund_amount = (
        refund_data["refund_amount_usd"].sum()
    )

    refunded_items = (
        refund_data["order_item_id"].nunique()
    )

    total_items = (
        order_items["order_item_id"].nunique()
    )

    refund_rate = (
        refunded_items / total_items
    ) * 100

    # =========================
    # KPI CARDS
    # =========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Refund Amount",
        f"${total_refund_amount:,.2f}"
    )

    col2.metric(
        "Refund Rate",
        f"{refund_rate:.2f}%"
    )

    col3.metric(
        "Refunded Items",
        f"{refunded_items:,}"
    )

    st.divider()

    # =========================
    # REFUND BY PRODUCT
    # =========================

    st.subheader("Refund Amount by Product")

    refunds_by_product = (
        refund_data
        .groupby("product_name")["refund_amount_usd"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(refunds_by_product)

    # =========================
    # REFUND SUMMARY
    # =========================

    st.subheader("Refund Summary")

    refund_summary = (
        refund_data
        .groupby("product_name")
        .agg(
            Refund_Amount=("refund_amount_usd", "sum"),
            Refunded_Items=("order_item_id", "nunique")
        )
        .sort_values(
            "Refund_Amount",
            ascending=False
        )
        .reset_index()
    )

    st.dataframe(
        refund_summary,
        use_container_width=True,
        hide_index=True
    )
elif page == "Business Insights":

    st.header("Business Insights")

    st.subheader("Key Business Insights")

    st.markdown("""
    ### 1. Strong Overall Profitability
    The business generated strong profitability, with total revenue of approximately
    $1.94 million and a profit margin of 62.74%.

    ### 2. High Conversion Performance
    The overall conversion rate was 6.83%, indicating that a meaningful portion of
    website sessions resulted in orders.

    ### 3. Desktop Drives More Traffic
    Desktop generated approximately 327K sessions, compared with approximately
    146K mobile sessions. This indicates that desktop is the dominant device
    for website traffic.

    ### 4. Search Marketing Is the Major Traffic Source
    Gsearch generated the highest number of sessions, followed by Bsearch and
    Socialbook. Search marketing therefore represents an important source of
    website traffic.

    ### 5. The Original Mr. Fuzzy Is the Leading Product
    The Original Mr. Fuzzy was the top-selling product and also generated the
    highest profit among the products analysed.

    ### 6. Refunds Require Monitoring
    The business recorded approximately $85.34K in refund amounts. Refund
    patterns should be monitored at the product level to identify products
    with relatively high refund activity.

    ### 7. Revenue Performance Varied by Year
    Revenue increased significantly through 2014, which recorded the highest
    annual revenue among the years analysed.
    """)

    st.divider()

    st.subheader("Business Recommendations")

    st.markdown("""
    - Continue investing in high-performing products such as The Original Mr. Fuzzy.
    - Analyse mobile performance to identify opportunities to improve mobile traffic
      and conversion.
    - Continue monitoring search marketing sources because they generate a large
      share of website sessions.
    - Investigate products with high refund amounts and identify possible causes.
    - Use yearly sales trends to support inventory planning and marketing decisions.
    """)

elif page == "Conversion Prediction":
    st.header("Website Conversion Prediction")

    st.write(
        "Enter website session details to estimate the probability "
        "of conversion."
    )

    is_repeat_session = st.selectbox(
        "Repeat Session",
        [0, 1]
    )

    utm_source = st.selectbox(
        "Marketing Source",
        website_sessions["utm_source"].dropna().unique()
    )

    utm_campaign = st.selectbox(
        "Marketing Campaign",
        website_sessions["utm_campaign"].dropna().unique()
    )

    utm_content = st.selectbox(
        "Marketing Content",
        website_sessions["utm_content"].dropna().unique()
    )

    device_type = st.selectbox(
        "Device Type",
        website_sessions["device_type"].dropna().unique()
    )

    http_referer = st.selectbox(
        "HTTP Referrer",
        website_sessions["http_referer"].fillna("Unknown").unique()
    )

    if st.button("Predict Conversion"):

        new_session = pd.DataFrame({
            "is_repeat_session": [is_repeat_session],
            "utm_source": [utm_source],
            "utm_campaign": [utm_campaign],
            "utm_content": [utm_content],
            "device_type": [device_type],
            "http_referer": [http_referer]
        })

        prediction = model.predict(new_session)[0]

        probability = model.predict_proba(
            new_session
        )[0][1]

        st.metric(
            "Conversion Probability",
            f"{probability:.2%}"
        )

        if prediction == 1:
            st.success("Prediction: Likely to Convert")
        else:
            st.warning("Prediction: Not Likely to Convert")
