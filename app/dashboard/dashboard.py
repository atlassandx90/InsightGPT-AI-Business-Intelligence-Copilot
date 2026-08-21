import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="InsightGPT Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- Custom CSS ---------------- #

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:42px;
    font-weight:700;
    margin-top:15px;
    margin-bottom:35px;
}

.metric-card{
    background:#f0f5f7;
    padding:22px;
    border-radius:15px;
    border:1px solid #7587fa;
    text-align:center;
    box-shadow:0px 2px 10px rgba(0,0,0,0.08);
}

.metric-title{
    font-size:18px;
    color:#555;
}

.metric-value{
    font-size:38px;
    font-weight:bold;
}

/* Search Box Styling */

.stTextInput > div > div > input {
    height: 75px;
    font-size: 20px;
    border-radius: 12px;
    border: 2px solid #00244f;
    padding-left: 15px;
}

.stTextInput > div > div > input:focus {
    border: 2px solid #fa0202;
    box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}

/* Quick Action Buttons */

div.stButton > button {
    height: 55px;
    border-radius: 10px;
    border: 1px solid #D1D5DB;
    font-weight: 600;
    width: 100%;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #2563EB;
    transform: translateY(-2px);
}

/* Primary Copilot Button */

.stButton button[kind="primary"] {
    height: 60px;
    font-size: 20px;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg,#2563EB,#7C3AED);
    color: white;
}

.stButton button[kind="primary"]:hover {
    transform: translateY(-2px);
}

</style>
""", unsafe_allow_html=True)

# ---------------- Dashboard Title ---------------- #

st.markdown(
    "<div class='main-title'>InsightGPT Business Intelligence Dashboard</div>",
    unsafe_allow_html=True
)

# ---------------- API URLs ---------------- #

BACKEND_URL = "https://insightgpt-ai-business-intelligence.onrender.com"

API_URL = f"{BACKEND_URL}/kpis"
MONTHLY_API = f"{BACKEND_URL}/sales/monthly"
STATE_API = f"{BACKEND_URL}/sales/state"
CATEGORY_API = f"{BACKEND_URL}/categories/top"
PAYMENT_API = f"{BACKEND_URL}/payments/types"
REVIEW_API = f"{BACKEND_URL}/reviews/score"
FORECAST_API = f"{BACKEND_URL}/forecast/revenue"
FILTER_API = f"{BACKEND_URL}/filters"
INSIGHT_API = f"{BACKEND_URL}/insights"
    
# Load filter values

if "query_history" not in st.session_state:
    st.session_state["query_history"] = []

if "total_queries" not in st.session_state:
    st.session_state["total_queries"] = 0

if "auto_ask" not in st.session_state:
    st.session_state["auto_ask"] = False

if "copilot_question" not in st.session_state:
    st.session_state["copilot_question"] = ""

try:
    filter_response = requests.get(
        FILTER_API,
        timeout=30
    )

    if filter_response.status_code != 200:
        st.error(
            f"Filter API returned HTTP {filter_response.status_code}"
        )
        st.code(filter_response.text[:2000])
        st.stop()

    filter_options = filter_response.json()

    # Validate expected response structure
    required_keys = ["states", "categories", "payment_types"]

    missing_keys = [
        key for key in required_keys
        if key not in filter_options
    ]

    if missing_keys:
        st.error(
            f"Filter API response is missing: {missing_keys}"
        )
        st.json(filter_options)
        st.stop()

except requests.exceptions.Timeout:
    st.error("Filter API request timed out after 30 seconds.")
    st.stop()

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to Filter API: {e}")
    st.stop()

except ValueError:
    st.error("Filter API returned invalid JSON.")
    st.code(filter_response.text[:2000])
    st.stop()

selected_state = st.sidebar.selectbox(
    "State",
    ["All"] + filter_options["states"]
)

selected_category = st.sidebar.selectbox(
    "Category",
    ["All"] + filter_options["categories"]
)

selected_payment = st.sidebar.selectbox(
    "Payment Type",
    ["All"] + filter_options["payment_types"]
)

params = {}

if selected_state != "All":
    params["state"] = selected_state

if selected_category != "All":
    params["category"] = selected_category

if selected_payment != "All":
    params["payment_type"] = selected_payment


try:

    # ================= Fetch KPI Data ================= #
       response = requests.get(API_URL, params=params)

       if response.status_code == 200:

        data = response.json()

        # ================= KPI Cards ================= #

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Total Revenue</div>
                    <div class="metric-value" style="color:#16A34A;">
                        ${data['total_revenue']:,.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Total Orders</div>
                    <div class="metric-value" style="color:#2563EB;">
                        {data['total_orders']:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Average Order Value</div>
                    <div class="metric-value" style="color:#9333EA;">
                        ${data['average_order_value']:,.2f}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ================= Load Data ================= #

        df = pd.DataFrame(data["order_status"])

        monthly_response = requests.get(MONTHLY_API, params=params)

        monthly = monthly_response.json()
        monthly_df = pd.DataFrame(monthly)

       # ================= State Revenue =================

        state = requests.get(STATE_API, params=params).json()

        state_df = pd.DataFrame(state)

      # ================= Category Revenue =================

        category = requests.get(CATEGORY_API, params=params).json()
        category_df = pd.DataFrame(category)

      # ================= Payments ====================
        
        payment = requests.get(PAYMENT_API, params=params).json()
        payment_df = pd.DataFrame(payment)

        # ================= Review =================

        review = requests.get(REVIEW_API, params=params).json()

        review_df = pd.DataFrame(review["ratings"])

        average_rating = review["average_rating"]


        # ================= Forecast =================

        forecast = requests.get(FORECAST_API, params=params).json()

        history_df = pd.DataFrame(forecast.get("history", []))

        forecast_df = pd.DataFrame(forecast["forecast"])

        has_history = (
        not history_df.empty
        and "month" in history_df.columns
        and "revenue" in history_df.columns
    )


       insight = requests.get(INSIGHT_API,params=params).json()

                # ================= Layout ================= #

       left, right = st.columns(2)

        # =====================================================
        # Left Side : Order Status
        # =====================================================

       with left:

            fig_bar = px.bar(
                df,
                x="total_orders",
                y="status",
                orientation="h",
                text="total_orders",
                color_discrete_sequence=["#4F46E5"]
            )

            fig_bar.update_traces(
                textposition="outside",
                cliponaxis=False
            )

            fig_bar.update_xaxes(
                range=[0, df["total_orders"].max() * 1.20],
                showgrid=False
            )

            fig_bar.update_layout(
                title=dict(
                    text="Order Status Distribution",
                    x=0.5,
                    xanchor="center",
                    font=dict(
                        size=28,
                        color="#1F2937"
                    )
                ),
                yaxis=dict(
                    categoryorder="total ascending"
                ),
                showlegend=False
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

        # =====================================================
        # Right Side : Monthly Revenue
        # =====================================================

       with right:

            fig_line = px.line(
                monthly_df,
                x="month",
                y="revenue",
                markers=True,
                color_discrete_sequence=["#16A34A"]
            )

            fig_line.update_layout(
                title=dict(
                    text="Monthly Revenue Trend",
                    x=0.5,
                    xanchor="center",
                    font=dict(
                        size=28,
                        color="#1F2937"
                    )
                )
            )

            st.plotly_chart(
                fig_line,
                use_container_width=True
            )


except Exception as e:
    st.error(f"Error: {e}")

st.markdown("<br>", unsafe_allow_html=True)

left2, right2 = st.columns(2)


# ================= State Revenue =================

with left2:

    fig_state = px.bar(
        state_df,
        x="state",
        y="revenue",
        text="revenue",
        color="revenue",
        color_continuous_scale="Blues"
    )

    fig_state.update_traces(
        texttemplate="$%{y:,.0f}",
        textposition="outside"
    )

    fig_state.update_layout(
        height=500,
        title=dict(
            text="Top 10 States by Revenue",
            x=0.5,
            xanchor="center",
            font=dict(
                size=28,
                color="#1F2937"
            )
        ),
        coloraxis_showscale=False,
        xaxis_title="State",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )

# ================= Category Revenue =================

with right2:

    fig_category = px.bar(
        category_df,
        x="revenue",
        y="category",
        orientation="h",
        text="revenue",
        color="revenue",
        color_continuous_scale="Greens"
    )

    fig_category.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside"
    )

    fig_category.update_layout(
        height=500,
        title=dict(
            text="Top 10 Product Categories",
            x=0.5,
            xanchor="center",
            font=dict(
                size=28,
                color="#1F2937"
            )
        ),
        coloraxis_showscale=False,
        xaxis_title="Revenue",
        yaxis_title="Category",
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)


fig_payment = px.pie(
    payment_df,
    names="payment_type",
    values="total_payments",
    hole=0.55,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig_payment.update_traces(
    textinfo="percent+label"
)

fig_payment.update_layout(

    title=dict(
        text="Payment Type Distribution",
        x=0.5,
        xanchor="center",
        font=dict(
            size=28,    
            color="#1F2937"
        )
    ),

    height=650,                     
    margin=dict(
        t=60,                       
        b=70,                      
        l=40,
        r=40
    ),
    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=-0.15
    )
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)


st.markdown("""
<h2 style='text-align:center;
font-size:28px;
font-weight:700;
margin-bottom:20px;'>
Customer Review Score
</h2>
""", unsafe_allow_html=True)

with st.container(border=True):

    st.markdown(
        "<h3 style='text-align:center;'>Average Customer Rating</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<h1 style='text-align:center;color:#16A34A;'>⭐ {average_rating}/5</h1>",
        unsafe_allow_html=True
    )

fig_review = px.bar(
    review_df,
    x="total_reviews",
    y="review_score",
    orientation="h",
    text="total_reviews",
    color="review_score",
    color_continuous_scale="RdYlGn"
)

fig_review.update_traces(
    textposition="outside"
)

fig_review.update_layout(
    height=380,
    coloraxis_showscale=False,
    xaxis_title="Number of Reviews",
    yaxis_title="Rating",
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig_review,
    use_container_width=True
)


st.markdown("<br>", unsafe_allow_html=True)

if not history_df.empty:


    fig_forecast = px.line()

    # Actual Revenue
    fig_forecast.add_scatter(
        x=history_df["month"],
        y=history_df["revenue"],
        mode="lines+markers",
        name="Actual Revenue"
    )

    # Forecast
    if not forecast_df.empty:
        fig_forecast.add_scatter(
            x=forecast_df["month"],
            y=forecast_df["revenue"],
            mode="lines+markers",
            name="Forecast",
            line=dict(dash="dash")
        )

    fig_forecast.update_layout(
        title=dict(
            text="Revenue Forecast",
            x=0.5,
            xanchor="center",
            font=dict(size=28, color="#1F2937")
        ),
        height=550,
        xaxis_title="Month",
        yaxis_title="Revenue"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )



st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<h2 style='text-align:center;
font-size:28px;
font-weight:700;
margin-bottom:20px;'>
AI Business Insights
</h2>
""", unsafe_allow_html=True)

with st.container(border=True):

    st.markdown(f"""
- **Total Revenue:** ${insight['revenue']:,.2f}

- **Highest Revenue State:** {insight['top_state']}

- **Top Product Category:** {insight['top_category'].replace('_',' ').title()}

- **Most Used Payment Type:** {insight['payment_type'].replace('_',' ').title()}

- **Average Customer Rating:** {insight['rating']}/5
""")


# =========================================================
# AI BUSINESS COPILOT
# =========================================================

st.divider()

st.markdown("""
<div style="
text-align:center;
padding:40px 20px;
background:linear-gradient(180deg,#F8FAFC,#EFF6FF);
border:1.5px solid #230094;
border-radius:20px;
margin-bottom:20px;
">
<h1>🤖 AI Business Copilot</h1>
<p style="font-size:18px;color:#475569;">
Ask business questions and receive AI-powered insights,
SQL transparency, visualizations, and recommendations.
</p>
</div>
""", unsafe_allow_html=True)

with st.container(border=True):

    st.caption(
        "Ask questions about revenue, orders, states, categories, payments, ratings, or forecasts."
    )

    question = st.text_input(
    "",
    value=st.session_state["copilot_question"],
    placeholder="Ask anything about revenue, sales, categories, customers..."
)

    ask_button = st.button(
        "Ask Copilot",
        type="primary",
        use_container_width=True
    )

    st.markdown("### Quick Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 Revenue Trend", use_container_width=True):
             st.session_state["copilot_question"] = "Show revenue trend"
             st.session_state["auto_ask"] = True
             st.rerun()
    
        if st.button("🏆 Top Category", use_container_width=True):
             st.session_state["copilot_question"] = "Which category generates highest revenue?"
             st.session_state["auto_ask"] = True
             st.rerun()
    
        if st.button("🌎 Top State", use_container_width=True):
             st.session_state["copilot_question"] = "Top performing state"
             st.session_state["auto_ask"] = True
             st.rerun()
    
    with col2:
        if st.button("💳 Payment Analysis", use_container_width=True):
             st.session_state["copilot_question"] = "Which payment type is used most?"
             st.session_state["auto_ask"] = True
             st.rerun()
    
        if st.button("⭐ Customer Rating", use_container_width=True):
             st.session_state["copilot_question"] = "What is the average customer rating?"
             st.session_state["auto_ask"] = True
             st.rerun()
    
        if st.button("🔮 Revenue Forecast", use_container_width=True):
             st.session_state["copilot_question"] = "Revenue forecast"
             st.session_state["auto_ask"] = True
             st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)

    if ask_button or st.session_state.get("auto_ask", False):

        question = st.session_state.get("copilot_question", "")

        result = None

        st.session_state["auto_ask"] = False

        if not question.strip():

            st.warning("⚠ Please enter a business question before running Copilot.")

        else:

            try:

                with st.spinner("Analyzing business data..."):

                   start_time = time.time()
                   
                   copilot_params = {
                       "query": question,
                       **params
                   }

                   copilot_response = requests.get(
                       f"{BACKEND_URL}/copilot",
                       params=copilot_params,
                       timeout=30
                    )

                st.session_state["total_queries"] += 1
                if copilot_response.status_code == 200:

                    result = copilot_response.json()

                    response_time = round(
                        time.time() - start_time,
                        2
                    )

                    if question not in st.session_state["query_history"]:
                       st.session_state["query_history"].append(question)

                    st.markdown("""
                    <div style="
                    background:#F8FAFC;
                    padding:20px;
                    border-radius:12px;
                    border-left:5px solid #2563EB;
                    margin-bottom:15px;
                    ">
                    <h3>Copilot Answer</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(
                        f"""
                        <div style="
                        background:white;
                        padding:20px;
                        border-radius:12px;
                        border:1px solid #E2E8F0;
                        font-size:17px;
                        ">
                        {result.get("answer")}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.caption(
                        f"Response Time: {response_time} sec"
                    )

                    st.markdown("""
                    <div style="
                    background:#EFF6FF;
                    padding:18px;
                    border-radius:12px;
                    border-left:5px solid #2563EB;
                    margin-top:10px;
                    margin-bottom:10px;
                    ">
                    <h4>Business Insight</h4>
                    <p style="font-size:16px;">
                    """ + result.get("insight","No insight available.") + """
                    </p>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    st.error(
                        f"Copilot API error: {copilot_response.status_code}"
                    )

                    st.stop()

# ================= Result Data =================

                if result and result.get("result") is not None:

                    query_result = result.get("result")

                    if not query_result:

                        st.info("No data found for this query.")

                    else:

                        st.markdown("""
                        <div style="
                        background:#F8FAFC;
                        padding:15px;
                        border-radius:12px;
                        border-left:5px solid #6366F1;
                        margin-top:15px;
                        margin-bottom:10px;
                        ">
                        <h3>Result Data</h3>
                        </div>
                        """, unsafe_allow_html=True)

                    with st.container(border=True):

                       try:

                            if isinstance(result["result"], list):

                               result_df = pd.DataFrame(result["result"])

                               st.dataframe(
                                   result_df,
                                   use_container_width=True
                                )

                               csv = result_df.to_csv(index=False)

                               st.download_button(
                                   "Download CSV",
                                   csv,
                                   file_name="copilot_results.csv",
                                   mime="text/csv"
                                )

                            elif isinstance(result["result"], dict):

                               st.dataframe(
                                   pd.DataFrame([result["result"]]),
                                   use_container_width=True
                                )

                            else:

                             st.write(result["result"])

                       except Exception as e:

                              st.error(f"Data display error: {e}")

                    with st.expander("View Generated SQL"):

                       st.code(
                           result.get("sql", "No SQL generated"),
                           language="sql"
                        )

                    chart = result.get("chart_metadata")

                    if chart:

                        st.markdown("""
                        <div style="
                        background:#F8FAFC;
                        padding:15px;
                        border-radius:12px;
                        border-left:5px solid #10B981;
                        margin-top:15px;
                        margin-bottom:10px;
                        ">
                        <h3>Visualization</h3>
                        </div>
                        """, unsafe_allow_html=True)

                        with st.container(border=True):

                            if chart["chart_type"] == "pie":

                                df = pd.DataFrame({
                                    "Category": chart["labels"],
                                    "Value": chart["values"]
                                })

                                fig = px.pie(
                                    df,
                                    names="Category",
                                    values="Value",
                                    title=chart["title"]
                                )

                                st.plotly_chart(
                                    fig,
                                    use_container_width=True
                                )

                                csv_chart = df.to_csv(index=False)

                                st.download_button(
                                    "Download Chart Data",
                                    csv_chart,
                                    file_name="chart_data.csv",
                                    mime="text/csv"
                                )

                            else:

                             df = pd.DataFrame({
                                 "Category": chart["x"],
                                 "Value": chart["y"]
                            })

                             if chart["chart_type"] == "bar":

                                 fig = px.bar(
                                     df,
                                     x="Category",
                                     y="Value",
                                     title=chart["title"]
                                )

                                 st.plotly_chart(
                                     fig,
                                     use_container_width=True
                                )

                                 csv_chart = df.to_csv(index=False)

                                 st.download_button(
                                    "Download Chart Data",
                                    csv_chart,
                                    file_name="chart_data.csv",
                                    mime="text/csv"
                                )

                             elif chart["chart_type"] == "line":

                                 fig = px.line(
                                     df,
                                     x="Category",
                                     y="Value",
                                     title=chart["title"],
                                     markers=True
                                )

                                 st.plotly_chart(
                                     fig,
                                     use_container_width=True
                                )

                                 csv_chart = df.to_csv(index=False)

                                 st.download_button(
                                    "Download Chart Data",
                                    csv_chart,
                                    file_name="chart_data.csv",
                                    mime="text/csv"
                                )

                recommendation = result.get("recommendation")

                if recommendation:

                    st.markdown("""
                    <div style="
                    background:#FEFCE8;
                    padding:15px;
                    border-radius:12px;
                    border-left:5px solid #F59E0B;
                    margin-top:15px;
                    margin-bottom:10px;
                    ">
                    <h3>Recommendation</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(
                        f"""
                        <div style="
                        background:white;
                        padding:20px;
                        border-radius:12px;
                        border:1px solid #E2E8F0;
                        font-size:17px;
                        ">
                        {recommendation}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to Copilot API: {e}"
                )


# ==========================================
# Copilot Analytics
# ==========================================

            st.markdown("### 📊 Copilot Analytics")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Total Queries Asked",
                    st.session_state["total_queries"]
                )

            with col2:
                st.metric(
                    "Unique Questions",
                    len(st.session_state["query_history"])
                )
            if st.session_state["query_history"]:

                st.markdown("### Query History")

                for q in reversed(st.session_state["query_history"][-5:]):
                    st.write("•", q)