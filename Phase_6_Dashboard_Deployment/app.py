import os
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Smart Renewable Energy Monitoring & Prediction System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#07111F;
    color:white;
}

section[data-testid="stSidebar"]{
    background:#0E1628;
}

.block-container{
    padding-top:0rem;
    padding-bottom:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

.metric-card{
    background:#111827;
    border-radius:18px;
    padding:18px;
    border:1px solid rgba(255,255,255,0.05);
}

.metric-title{
    color:#94A3B8;
    font-size:15px;
}

.metric-value{
    color:#38BDF8;
    font-size:34px;
    font-weight:bold;
}

.main-title{
    font-size:42px;
    font-weight:800;
    color:white;
}

.sub-title{
    color:#CBD5E1;
    font-size:18px;
}

hr{
    border:1px solid #1E293B;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Phase_3_Spark_Preprocessing",
    "output"
)

ML_PATH = os.path.join(
    BASE_DIR,
    "..",
    "Phase_5_Machine_Learning",
    "ML_Output"
)

FIGURE_PATH = os.path.join(
    BASE_DIR,
    "dashboard_figures"
)

# ==========================================================
# LOAD DATASETS
# ==========================================================

@st.cache_data
def load_data():

    solar = pd.read_csv(
        os.path.join(DATA_PATH,"solar_processed.csv")
    )

    wind = pd.read_csv(
        os.path.join(DATA_PATH,"wind_processed.csv")
    )

    grid = pd.read_csv(
        os.path.join(DATA_PATH,"household_processed.csv")
    )

    daily = pd.read_csv(
        os.path.join(DATA_PATH,"daily_solar_generation.csv")
    )

    return solar,wind,grid,daily

solar_df,wind_df,grid_df,daily_df = load_data()

# ==========================================================
# PREPARE GRID DATA
# ==========================================================

grid_df["DateTime"] = pd.to_datetime(
    grid_df["Date"]+" "+grid_df["Time"]
)

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

solar_avg = round(
    solar_df["DC_POWER"].mean(),2
)

solar_max = round(
    solar_df["DC_POWER"].max(),2
)

wind_avg = round(
    wind_df["LV ActivePower (kW)"].mean(),2
)

wind_max = round(
    wind_df["LV ActivePower (kW)"].max(),2
)

grid_avg = round(
    grid_df["Global_active_power"].mean(),2
)

grid_max = round(
    grid_df["Global_active_power"].max(),2
)

total_records = (
    len(solar_df)
    +len(wind_df)
    +len(grid_df)
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/lightning-bolt.png",
        width=70
    )

    st.markdown("## Renewable Energy")

    selected = option_menu(

        menu_title=None,

        options=[
            "Dashboard",
            "Solar Analytics",
            "Wind Analytics",
            "Grid Analytics",
            "Machine Learning",
            "EDA",
            "Dataset Explorer",
            "System Health"
        ],

        icons=[
            "house",
            "sun",
            "wind",
            "lightning",
            "cpu",
            "bar-chart",
            "database",
            "activity"
        ],

        default_index=0
    )

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div style="
margin-top:20px;
margin-bottom:25px;
">

<h1 style="
font-size:46px;
font-weight:800;
color:white;
margin-bottom:8px;
">
⚡ Smart Renewable Energy Monitoring & Prediction System
</h1>

<p style="
font-size:19px;
color:#B8C7E0;
margin-top:0px;
">
Real-Time Renewable Energy Monitoring, Big Data Analytics,
Machine Learning & Interactive Dashboard
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# KPI ROW
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "☀ Solar Average",
        f"{solar_avg:.2f}"
    )

with c2:
    st.metric(
        "🌬 Wind Average",
        f"{wind_avg:.2f}"
    )

with c3:
    st.metric(
        "⚡ Grid Average",
        f"{grid_avg:.2f}"
    )

with c4:
    st.metric(
        "📊 Total Records",
        f"{total_records:,}"
    )

st.divider()

# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "Dashboard":

    st.subheader("📊 Executive Dashboard")

    row1_col1, row1_col2 = st.columns([3,1])

    with row1_col1:

        fig = px.line(
            solar_df.head(1000),
            y="DC_POWER",
            title="☀ Solar Power Generation Trend"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#07111F",
            plot_bgcolor="#07111F",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with row1_col2:

        fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=solar_avg,

                title={
                    "text":"Average Solar Output"
                },

                gauge={

                    "axis":{
                        "range":[0,solar_max]
                    },

                    "bar":{
                        "color":"orange"
                    },

                    "steps":[
                        {
                            "range":[0,solar_max*0.5],
                            "color":"#1E3A5F"
                        },

                        {
                            "range":[solar_max*0.5,solar_max],
                            "color":"#2563EB"
                        }

                    ]

                }

            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("")

    row2_col1,row2_col2=st.columns(2)

    with row2_col1:

        fig=px.line(

            wind_df.head(1000),

            y="LV ActivePower (kW)",

            title="🌬 Wind Power Generation"

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#07111F",

            plot_bgcolor="#07111F",

            height=350

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with row2_col2:

        fig=px.pie(

            names=[

                "Solar",

                "Wind",

                "Grid"

            ],

            values=[

                solar_avg,

                wind_avg,

                grid_avg

            ],

            title="⚡ Energy Contribution"

        )

        fig.update_layout(

            template="plotly_dark",

            height=350

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.write("")

    row3_col1,row3_col2=st.columns(2)

    with row3_col1:

        fig=px.line(

            grid_df.head(1000),

            x="DateTime",

            y="Global_active_power",

            title="⚡ Household Grid Consumption"

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#07111F",

            plot_bgcolor="#07111F",

            height=350

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with row3_col2:

        fig=px.line(

            daily_df,

            x=daily_df.columns[0],

            y=daily_df.columns[1],

            markers=True,

            title="☀ Daily Solar Generation"

        )

        fig.update_layout(

            template="plotly_dark",

            paper_bgcolor="#07111F",

            plot_bgcolor="#07111F",

            height=350

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    st.subheader("📈 Dataset Summary")

    s1,s2,s3=st.columns(3)

    s1.metric(

        "Solar Samples",

        len(solar_df)

    )

    s2.metric(

        "Wind Samples",

        len(wind_df)

    )

    s3.metric(

        "Grid Samples",

        len(grid_df)

    )

# ==========================================================
# SOLAR ANALYTICS
# ==========================================================

elif selected == "Solar Analytics":

    st.header("☀ Solar Energy Analytics")

    left,right=st.columns([3,2])

    with left:

        fig=px.scatter(
            solar_df,
            x="IRRADIATION",
            y="DC_POWER",
            color="MODULE_TEMPERATURE",
            title="Solar Irradiation vs DC Power"
        )

        fig.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Solar Statistics")

        st.metric(
            "Average DC Power",
            round(
                solar_df["DC_POWER"].mean(),
                2
            )
        )

        st.metric(
            "Maximum DC Power",
            round(
                solar_df["DC_POWER"].max(),
                2
            )
        )

        st.metric(
            "Average Irradiation",
            round(
                solar_df["IRRADIATION"].mean(),
                2
            )
        )

    st.divider()

    col1,col2=st.columns(2)

    with col1:

        fig=px.histogram(
            solar_df,
            x="DC_POWER",
            nbins=40,
            title="Distribution of DC Power"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        corr=solar_df.select_dtypes(
            include="number"
        ).corr()

        fig=px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="Viridis",
            title="Solar Correlation Heatmap"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    img=os.path.join(
        FIGURE_PATH,
        "solar_power_trend.png"
    )

    if os.path.exists(img):

        st.image(
            img,
            caption="Solar Trend Visualization"
        )

# ==========================================================
# WIND ANALYTICS
# ==========================================================

elif selected=="Wind Analytics":

    st.header("🌬 Wind Energy Analytics")

    left,right=st.columns([3,2])

    with left:

        fig=px.scatter(
            wind_df,
            x="Wind Speed (m/s)",
            y="LV ActivePower (kW)",
            color="Wind Direction (°)",
            title="Wind Speed vs Power Output"
        )

        fig.update_layout(
            template="plotly_dark",
            height=500
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Wind Statistics")

        st.metric(
            "Average Power",
            round(
                wind_df["LV ActivePower (kW)"].mean(),
                2
            )
        )

        st.metric(
            "Maximum Power",
            round(
                wind_df["LV ActivePower (kW)"].max(),
                2
            )
        )

        st.metric(
            "Average Wind Speed",
            round(
                wind_df["Wind Speed (m/s)"].mean(),
                2
            )
        )

    st.divider()

    col1,col2=st.columns(2)

    with col1:

        fig=px.histogram(
            wind_df,
            x="LV ActivePower (kW)",
            nbins=40,
            title="Wind Power Distribution"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        corr=wind_df.select_dtypes(
            include="number"
        ).corr()

        fig=px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="Turbo",
            title="Wind Correlation Heatmap"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    img=os.path.join(
        FIGURE_PATH,
        "wind_power_trend.png"
    )

    if os.path.exists(img):

        st.image(
            img,
            caption="Wind Trend Visualization"
        )

# ==========================================================
# GRID ANALYTICS
# ==========================================================

elif selected=="Grid Analytics":

    st.header("⚡ Household Grid Analytics")

    fig=px.line(
        grid_df.head(1500),
        x="DateTime",
        y="Global_active_power",
        title="Global Active Power"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    c1,c2=st.columns(2)

    with c1:

        fig=px.histogram(
            grid_df,
            x="Global_active_power",
            nbins=40,
            title="Power Distribution"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        corr=grid_df.select_dtypes(
            include="number"
        ).corr()

        fig=px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="Blues",
            title="Grid Correlation Heatmap"
        )

        fig.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    img=os.path.join(
        FIGURE_PATH,
        "grid_consumption_trend.png"
    )

    if os.path.exists(img):

        st.image(
            img,
            caption="Grid Trend Visualization"
        )

# ==========================================================
# MACHINE LEARNING
# ==========================================================

elif selected == "Machine Learning":

    st.header("🤖 Machine Learning Prediction Results")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("☀ Solar Prediction")

        st.metric(
            "Target",
            "DC Power"
        )

        st.metric(
            "Algorithm",
            "Random Forest"
        )

        solar_img = os.path.join(
            ML_PATH,
            "solar_prediction_results.png"
        )

        if os.path.exists(solar_img):

            st.image(
                solar_img,
                use_container_width=True
            )

        else:

            st.warning(
                "Solar prediction image not found."
            )

    with col2:

        st.subheader("🌬 Wind Prediction")

        st.metric(
            "Target",
            "Wind Power"
        )

        st.metric(
            "Algorithm",
            "Random Forest"
        )

        wind_img = os.path.join(
            ML_PATH,
            "wind_prediction_results.png"
        )

        if os.path.exists(wind_img):

            st.image(
                wind_img,
                use_container_width=True
            )

        else:

            st.warning(
                "Wind prediction image not found."
            )

    st.divider()

    st.subheader("📋 Model Summary")

    metric_file = os.path.join(
        ML_PATH,
        "model_metrics.txt"
    )

    if os.path.exists(metric_file):

        with open(metric_file) as f:

            st.code(f.read())

    else:

        st.info(
            "Run Machine Learning first to generate metrics."
        )

# ==========================================================
# EDA
# ==========================================================

elif selected == "EDA":

    st.header("📊 Exploratory Data Analysis")

    figures = [

        "solar_distribution.png",

        "wind_distribution.png",

        "grid_distribution.png",

        "solar_vs_wind_comparison.png",

        "daily_solar_generation.png"

    ]

    cols = st.columns(2)

    index = 0

    for fig_name in figures:

        fig_path = os.path.join(
            FIGURE_PATH,
            fig_name
        )

        if os.path.exists(fig_path):

            with cols[index % 2]:

                st.image(
                    fig_path,
                    caption=fig_name.replace("_"," ").replace(".png",""),
                    use_container_width=True
                )

            index += 1

# ==========================================================
# DATASET EXPLORER
# ==========================================================

elif selected == "Dataset Explorer":

    st.header("🗂 Dataset Explorer")

    dataset = st.selectbox(

        "Select Dataset",

        [

            "Solar",

            "Wind",

            "Grid"

        ]

    )

    if dataset == "Solar":

        st.dataframe(
            solar_df.head(100)
        )

        st.download_button(

            "Download Solar Dataset",

            solar_df.to_csv(index=False),

            "solar_processed.csv",

            "text/csv"

        )

    elif dataset == "Wind":

        st.dataframe(
            wind_df.head(100)
        )

        st.download_button(

            "Download Wind Dataset",

            wind_df.to_csv(index=False),

            "wind_processed.csv",

            "text/csv"

        )

    else:

        st.dataframe(
            grid_df.head(100)
        )

        st.download_button(

            "Download Grid Dataset",

            grid_df.to_csv(index=False),

            "household_processed.csv",

            "text/csv"

        )

# ==========================================================
# SYSTEM HEALTH
# ==========================================================

elif selected == "System Health":

    st.header("🟢 System Status")

    c1,c2 = st.columns(2)

    with c1:

        st.success("Apache NiFi")
        st.success("Apache Kafka")
        st.success("Apache Spark")

    with c2:

        st.success("PostgreSQL")
        st.success("Python")
        st.success("Streamlit")

    st.divider()

    st.subheader("📈 Project Summary")

    st.info(f"""
    Total Solar Records : {len(solar_df):,}

    Total Wind Records : {len(wind_df):,}

    Total Grid Records : {len(grid_df):,}

    Total Combined Records : {total_records:,}
    """)

    st.divider()

    st.subheader("🛠 Technologies Used")

    tech = [

        "Apache NiFi",

        "Apache Kafka",

        "PostgreSQL",

        "Apache Spark",

        "Python",

        "Pandas",

        "Scikit-learn",

        "Plotly",

        "Streamlit"

    ]

    for t in tech:

        st.write("✅", t)

    st.divider()

    st.success(
        "Renewable Energy Forecasting Dashboard is running successfully."
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
"""
<center>

<h4>⚡ Smart Renewable Energy Monitoring & Prediction System</h4>

Developed using Apache NiFi, Kafka, PostgreSQL, Apache Spark,
Machine Learning and Streamlit.


</center>
""",
unsafe_allow_html=True
)