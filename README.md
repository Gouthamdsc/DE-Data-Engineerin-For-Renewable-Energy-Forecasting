Data-Engineerin-For-Renewable-Energy-Forecasting

## Project Overview

The **Data-Engineerin-For-Renewable-Energy-Forecasting** is an end-to-end **Data Engineering and Machine Learning project** designed to monitor, process, analyze, and predict renewable energy generation using **Solar, Wind, Weather, and Grid Energy datasets**.

The project focuses on building a scalable renewable energy analytics pipeline using modern technologies such as **Apache NiFi, Apache Kafka, PostgreSQL, Apache Spark, Python, Machine Learning, and Streamlit**.

The system integrates heterogeneous renewable datasets, performs preprocessing and analytics, predicts energy generation, and provides interactive dashboard visualization for monitoring and decision-making.

---

## Project Objectives

The main objectives of this project are:

* Integrate renewable energy datasets from multiple sources
* Build a real-time ingestion pipeline
* Perform data preprocessing and feature engineering
* Analyze renewable energy trends
* Predict renewable energy generation using Machine Learning
* Develop an interactive monitoring dashboard

---

## Technology Stack

### Data Ingestion

* Apache NiFi
* Apache Kafka

### Storage

* PostgreSQL

### Processing & Transformation

* Apache Spark
* Python
* Pandas

### Orchestration

* Apache Airflow DAGs

### Analysis & Visualization

* Matplotlib
* Seaborn

### Machine Learning

* Scikit-learn
* Random Forest Regression

### Dashboard Deployment

* Streamlit

### Monitoring & Governance

* Logging
* Data Quality Checks

---

## Project Architecture

```text
Raw Renewable Datasets
        ↓
Data Integration
        ↓
Timestamp Standardization
        ↓
Apache NiFi Pipeline
(GetFile → SplitText → PublishKafka)
        ↓
Apache Kafka Streaming
        ↓
PostgreSQL Storage
        ↓
Apache Spark Preprocessing
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis (EDA)
        ↓
Machine Learning Prediction
(Random Forest Regression)
        ↓
Streamlit Dashboard Deployment
        ↓
Monitoring & Logging
```

---

## Data Sources

### 1. Wind Energy Dataset

Source:
https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset

Purpose:

* Wind power generation analysis
* Wind turbine performance prediction
* Wind speed monitoring

Required Columns:

* timestamp
* LV ActivePower (kW)
* Wind Speed (m/s)
* Wind Direction (°)

---

### 2. Solar Energy Dataset

Source:
https://www.kaggle.com/datasets/anikannal/solar-power-generation-data

Purpose:

* Solar energy generation monitoring
* Irradiation analysis
* Power prediction

Required Columns:

* DATE_TIME
* PLANT_ID
* SOURCE_KEY
* DC_POWER
* AC_POWER
* IRRADIATION
* AMBIENT_TEMPERATURE
* MODULE_TEMPERATURE

---

### 3. Grid Energy Dataset

Source:
https://www.kaggle.com/datasets/uciml/electric-power-consumption-data-set/data

Purpose:

* Grid consumption monitoring
* Energy demand forecasting

Required Columns:

* Date
* Time
* Global_active_power
* Voltage
* Global_intensity

---

### 4. Weather Data Integration

Source:
https://openweathermap.org/api

Purpose:
Weather conditions significantly affect renewable energy generation. Therefore, environmental data was integrated into the system.

Weather Parameters:

* Temperature
* Humidity
* Wind Speed
* Cloud Coverage

API Integration:
Weather data is dynamically fetched using **OpenWeather API** through Python-based API requests.

---

## Project Phases

### Phase 1 — Real-Time Data Pipeline

Tasks:

* Raw data collection
* Dataset integration
* Timestamp standardization
* NiFi pipeline implementation
* Kafka streaming
* PostgreSQL storage

Components:

```text
GetFile → SplitText → PublishKafka
```

Kafka Topics:

* solar_topic
* wind_topic
* weather_topic
* grid_topic

Database Tables:

* solar_data
* wind_data
* weather_data
* grid_data

---

### Phase 2 — Data Preparation & Feature Engineering

Tasks:

* Data cleaning
* Missing value handling
* Timestamp processing
* Feature engineering

Generated Features:

* Hour
* Day
* Month

Technologies:

* Apache Spark
* Pandas
* Python

Generated Outputs:

* rq2_cleaned_solar.csv
* rq2_cleaned_wind.csv
* rq2_cleaned_grid.csv

---

### Phase 3 — Exploratory Data Analysis (EDA)

Tasks:

* Trend analysis
* Correlation analysis
* Statistical visualization

Generated Visualizations:

* solar_power_distribution.png
* solar_irradiation_vs_power.png
* wind_speed_vs_power.png
* grid_demand_trend.png
* solar_heatmap.png

---

### Phase 4 — Machine Learning Prediction

Algorithm Used:
**Random Forest Regressor**

Prediction Targets:

* Solar energy generation
* Wind energy generation

Evaluation Metrics:

* MAE (Mean Absolute Error)
* RMSE (Root Mean Square Error)
* R² Score

Model Performance:

Solar Model:

* R² = 98.64%

Wind Model:

* R² = 90.59%

---

### Phase 5 — Dashboard Deployment

Technology:
**Streamlit**

Dashboard Features:

* Solar monitoring
* Wind monitoring
* Grid monitoring
* Energy comparison
* Prediction visualization
* Performance analytics

Run Dashboard:

```bash
streamlit run app.py
```

Access:

```text
http://localhost:8501
```

---

## Folder Structure

```text
Smart_Renewable_Energy_System/
│
├── Phase_1_Real_Time_Data_Pipeline/
│   ├── Datasets/
│   ├── Data_Integration/
│   ├── NiFi_Kafka_Streaming/
│   ├── PostgreSQL/
│   └── Weather_API/
│
├── Phase_2_Data_Preparation/
│
├── Phase_3_Data_Analysis/
│
├── Phase_4_Machine_Learning/
│
├── Phase_5_Dashboard_Deployment/
│
├── Screenshots/
│
└── Documentation/
```

---

## Team Members

* Avila Kumar — Team Lead, Planning, Documentation, Integration
* Manideep — NiFi, Kafka, PostgreSQL
* Gowtham — Spark, Transformation, DAGs, Data Quality
* Sai Krishna — EDA, Machine Learning, Dashboard

---

## Current Progress

✅ Data Collection

✅ Pipeline Development

✅ Spark Processing

✅ Data Analysis

✅ Machine Learning

✅ Dashboard Development

🔄 Final Integration & Optimization in Progress

---

## Future Enhancements

* Real-time IoT sensor integration
* Cloud deployment
* Advanced forecasting models
* Deep learning integration
* Automated monitoring system
