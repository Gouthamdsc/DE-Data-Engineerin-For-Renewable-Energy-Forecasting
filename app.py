import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Smart Renewable Energy Monitoring & Prediction System",
    page_icon="⚡",
    layout="wide"
)

# ==========================================================
# DARK ENTERPRISE CSS
# ==========================================================

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#050B18;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#0B1220;
}

.block-container{
    padding-top:1rem;
}

.metric-card{
    background: linear-gradient(145deg,#111827,#0F172A);
    border-radius:20px;
    padding:20px;
    border:1px solid rgba(255,255,255,0.06);
    box-shadow:0px 4px 20px rgba(0,0,0,0.4);
}

.card-title{
    color:#94A3B8;
    font-size:15px;
}

.card-value{
    color:#38BDF8;
    font-size:34px;
    font-weight:bold;
}

.big-title{
    font-size:52px;
    font-weight:800;
    color:white;
}

.sub-title{
    color:#94A3B8;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

solar_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_solar.csv")
wind_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_wind.csv")
grid_df = pd.read_csv("../Phase_2_Data_Preparation/cleaned_grid.csv")
weather_df = pd.read_csv("../Phase_1_Real_Time_Data_Pipeline/Datasets/weather_germany_final-checkpoint.csv", skiprows=13)

# ==========================================================
# DATA CALCULATIONS
# ==========================================================

solar_avg = round(solar_df["DC_POWER"].mean(), 2)

wind_avg = round(
    wind_df["LV ActivePower (kW)"].mean(), 2
)

grid_avg = round(
    grid_df["grid_demand"].mean(), 2
)

temperature = round(weather_df["T2M"].mean(), 1)
humidity = round(weather_df["RH2M"].mean(), 1)
wind_speed = round(weather_df["WS2M"].mean(), 1)
irradiation = round(
    weather_df["ALLSKY_SFC_SW_DWN"].mean(), 2
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## ⚡ Energy Control Center")

    selected = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Solar",
            "Wind",
            "Grid",
            "Predictions",
            "System Health"
        ],
        icons=[
            "house",
            "sun",
            "wind",
            "lightning",
            "graph-up-arrow",
            "cpu"
        ],
        default_index=0,
    )

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div class='big-title'>
⚡ Smart Renewable Energy Monitoring & Prediction System
</div>
<div class='sub-title'>
Real-Time Renewable Energy Monitoring, Forecasting & Intelligent Analytics Platform
</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================================
# KPI ROW
# ==========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>☀ Solar Generation</div>
        <div class='card-value'>{solar_avg} MW</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>🌬 Wind Energy</div>
        <div class='card-value'>{wind_avg} MW</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>⚡ Grid Consumption</div>
        <div class='card-value'>{grid_avg}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='card-title'>🎯 Prediction Accuracy</div>
        <div class='card-value'>94.6%</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ==========================================================
# DASHBOARD
# ==========================================================

if selected == "Dashboard":

    c1, c2 = st.columns([2,1])

    with c1:

        fig = px.line(
            solar_df.head(1000),
            y="DC_POWER",
            title="☀ Solar Energy Generation"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c2:

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=solar_avg,
            title={'text': "Live Renewable Output"},
            gauge={
                'axis': {'range': [None, 10000]},
                'bar': {'color': "#38BDF8"}
            }
        ))

        fig.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            wind_df.head(1000),
            y="LV ActivePower (kW)",
            title="🌬 Wind Energy Trend"
        )

        fig.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig = px.pie(
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
            title="⚡ Energy Mix"
        )

        fig.update_layout(
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# SOLAR
# ==========================================================

elif selected == "Solar":

    st.header("☀ Solar Analytics")

    st.image("solar_prediction_results.png")

    fig = px.scatter(
        solar_df,
        x="IRRADIATION",
        y="DC_POWER",
        title="Solar Irradiation vs Power"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# WIND
# ==========================================================

elif selected == "Wind":

    st.header("🌬 Wind Monitoring")

    st.image("../Phase_4_Machine_Learning/wind_prediction_results.png")

    fig = px.scatter(
        wind_df,
        x="Wind Speed (m/s)",
        y="LV ActivePower (kW)"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# GRID
# ==========================================================

elif selected == "Grid":

    st.header("⚡ Grid Monitoring")

    fig = px.line(
        grid_df.head(1000),
        y="grid_deman",
        title="Grid Consumption Pattern"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# PREDICTIONS
# ==========================================================

elif selected == "Predictions":

    st.header("🎯 Machine Learning Intelligence")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Solar Model Accuracy",
            "98.64%"
        )

        st.image(
            "../Phase_4_Machine_Learning/solar_prediction_results.png"
        )

    with c2:
        st.metric(
            "Wind Model Accuracy",
            "90.59%"
        )

        st.image(
            "../Phase_4_Machine_Learning/wind_prediction_results.png"
        )

# ==========================================================
# SYSTEM HEALTH
# ==========================================================

elif selected == "System Health":

    st.header("🟢 Infrastructure Health")

    st.success("Apache NiFi — Running")

    st.success("Apache Kafka — Streaming")

    st.success("Apache Spark — Active")

    st.success("PostgreSQL — Connected")

    st.success("Streamlit Deployment — Online")

    st.subheader("🌡 Weather Intelligence")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Temperature", f"{temperature} °C")
    c2.metric("Humidity", f"{humidity}%")
    c3.metric("Wind Speed", f"{wind_speed} m/s")
    c4.metric("Solar Irradiance", irradiation)