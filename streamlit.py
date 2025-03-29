import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

conn = duckdb.connect("ecommerce.duckdb")
if "transactions" not in conn.execute("SHOW TABLES").df()["name"].values:
    st.error("❌ Table 'transactions' does not exist! Load the data first.")
    st.stop()

@st.cache_data
def load_data():
    query = "SELECT * FROM transactions"
    df = conn.execute(query).df()
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df

df = load_data()

def load_data_profiling():
    query_void_cancel_no_initial = """
    SELECT COUNT(*) 
    FROM transactions 
    WHERE status IN ('void', 'cancel') 
    AND transaction_id NOT IN (
        SELECT transaction_id FROM transactions WHERE status = 'paid'
    );
    """
    void_cancel_no_initial = conn.execute(query_void_cancel_no_initial).fetchone()[0]

    query_negative_amount = "SELECT COUNT(*) FROM transactions WHERE amount < 0"
    negative_amount_count = conn.execute(query_negative_amount).fetchone()[0]

    query_status_distribution = """
    SELECT status, COUNT(*) 
    FROM transactions 
    GROUP BY status
    ORDER BY COUNT(*) DESC;
    """
    status_distribution = conn.execute(query_status_distribution).fetchall()

    query_transaction_trends = """
    SELECT timestamp AS transaction_date, COUNT(*) AS total_transactions
    FROM transactions
    GROUP BY transaction_date
    ORDER BY transaction_date;
    """
    transaction_trends = conn.execute(query_transaction_trends).fetchall()

    return void_cancel_no_initial, negative_amount_count, status_distribution, transaction_trends

void_cancel_no_initial, negative_amount_count, status_distribution, transaction_trends = load_data_profiling()

st.markdown(
    """
    <style>
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 20px;
    }

    .metric-box {
        flex: 1;
        background: #FAFAFA;
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #CCCCCC;
        text-align: left;
        font-size: 16px;
        font-weight: bold;
        color: #333333;
        min-width: 180px;
        vertical-align: top;
    }

    .metric-number {
        font-size: 20px;
        font-weight: 600;
        color: #2C3E50;
        margin-left:10px;
        display: inline-block;
        vertical-align: top;
    }

    .info-box {
        background-color: #f9f9f9;
        border-left: 5px solid #FF6B6B;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        color: #333333;
    }

    .dashboard-box {
        background-color: #f9f9f9;
        border-left: 7px solid #2C8EB3;
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
        font-size: 20px;
        font-weight: bold;
        color: #333333;
        line-height: 0.5; 
    }

    .dashboard-box h3 {
        font-size: 18px;
        margin-bottom: 10px; 
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 E-commerce Transaction Dashboard")

st.sidebar.markdown('<div class="sidebar-title">🔍 Filter Transactions</div>', unsafe_allow_html=True)
category = st.sidebar.selectbox("📌 Select Category", ["All"] + list(df["category"].unique()))
payment_method = st.sidebar.selectbox("💳 Select Payment Method", ["All"] + list(df["payment_method"].unique()))
date_range = st.sidebar.date_input("📅 Select Date Range", [])
if not date_range:
    date_range = [df["date"].min(), df["date"].max()]
st.sidebar.markdown("✅ Use the filters above to refine the data!")

filtered_df = df.copy()
if category != "All":
    filtered_df = filtered_df[filtered_df["category"] == category]
if payment_method != "All":
    filtered_df = filtered_df[filtered_df["payment_method"] == payment_method]
filtered_df = filtered_df[(filtered_df["date"] >= date_range[0]) & (filtered_df["date"] <= date_range[1])]

st.markdown(
    '<div class="dashboard-box">'
    '<h3>Total Transactions</h3>'
    f'<span class="metric-number">{len(filtered_df):,}</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-box">'
    '<h3>Total Revenue</h3>'
    f'<span class="metric-number">${filtered_df["amount"].sum():,.2f}</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-box">'
    '<h3>Average Amount</h3>'
    f'<span class="metric-number">${filtered_df["amount"].mean():,.2f}</span>'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-box">'
    '<h3>Transactions with Issues</h3>'
    f'<span class="metric-number">{len(filtered_df[filtered_df["amount"] < 0]):,}</span>'
    '</div>',
    unsafe_allow_html=True
)

st.subheader("📊 Transaction Status Distribution")
status_counts = filtered_df["status"].dropna().value_counts().reset_index()
status_counts.columns = ["status", "count"]

fig_status = px.bar(
    status_counts, 
    x="status", 
    y="count", 
    color="status", 
    title="Count of Transaction Statuses",
    color_discrete_sequence=['#A3C4BC', '#E9C46A', '#E76F51', '#2A9D8F']
)

fig_status.update_xaxes(tickangle=45)
st.plotly_chart(fig_status, use_container_width=True)

st.subheader("📊 Transaction Status Distribution (Data Table)")
st.dataframe(status_counts, use_container_width=True)

st.subheader("📅 Daily Transaction Summary")
daily_summary = (
    filtered_df.groupby("date").agg({"transaction_id": "count", "amount": "sum"}).reset_index()
)
daily_summary.columns = ["Date", "Transaction Count", "Total Revenue"]
st.dataframe(daily_summary, use_container_width=True)

st.subheader("⚠️ Transactions with Data Quality Issues")
issues_df = filtered_df[(filtered_df["amount"] < 0) | (filtered_df["status"].isin(["void", "cancel"]))] 
st.dataframe(issues_df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
st.subheader("🔍 Data Profiling Results")
st.markdown(f"""
<div class="info-box">
❌ Void/Cancel Transactions (without an initial 'paid' transaction): <span style="color:#D72638;">{void_cancel_no_initial}</span>
</div>

<div class="info-box">
💸 Transactions with Negative Amount: <span style="color:#D72638;">{negative_amount_count}</span>
</div>
""", unsafe_allow_html=True) 