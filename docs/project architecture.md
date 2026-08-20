# Project Architecture

# Project Name

InsightGPT – AI Business Intelligence Copilot

---

# System Overview

InsightGPT is an AI-powered Business Intelligence platform built on top of the Olist E-Commerce dataset.

The system combines:

- PostgreSQL Database
- FastAPI Backend
- Gemini AI
- SQL Generation Engine
- SQL Validation Layer
- Machine Learning Forecasting
- Streamlit Dashboard
- Power BI Dashboard
- Automated Testing Framework

Users can explore business KPIs through dashboards or ask natural language business questions through the AI Copilot.

---

# High-Level Architecture

+----------------------+
| Streamlit Dashboard  |
+----------+-----------+
           |
           v
+----------------------+
| FastAPI Backend      |
+----------+-----------+
           |
           |
   -------------------
   |        |        |
   v        v        v

Analytics   AI      Forecasting
Engine      Copilot Engine

   |         |          |
   |         |          |
   ----------------------
              |
              v

      PostgreSQL Database

---

# Technology Stack

## Frontend

- Streamlit
- Plotly

## Backend

- FastAPI
- Uvicorn

## Database

- PostgreSQL

## AI Layer

- Google Gemini

## Machine Learning

- Scikit-Learn

## Data Processing

- Pandas
- NumPy

## Testing

- Pytest

## Additional Analytics

- Power BI

---

# Application Layers

## 1. Data Layer

Location:

app/database

Components:

- connection.py
- config.py
- load_data.py

Responsibilities:

- Database connection
- Data loading
- Query execution
- Data retrieval

---

## 2. Analytics Layer

Location:

app/analytics

Modules:

- revenue.py
- categories.py
- payments.py
- reviews.py
- filters.py
- insights.py

Responsibilities:

- KPI calculations
- Revenue analytics
- Category analytics
- Payment analytics
- Customer review analytics
- Business insights generation

---

## 3. Forecasting Layer

Location:

app/ml

Module:

- forecasting.py

Responsibilities:

- Revenue forecasting
- Historical trend analysis
- Future revenue prediction

Output:

- Historical revenue
- Forecast revenue

---

## 4. AI Copilot Layer

Location:

app/llm

Modules:

- copilot.py
- query_parser.py
- sql_generator.py
- sql_validator.py
- response_models.py

Responsibilities:

- Natural language understanding
- Filter extraction
- SQL generation
- SQL validation
- Result explanation
- Recommendation generation
- Chart metadata generation

---

# AI Copilot Workflow

User Question

↓

Query Parser

↓

Gemini Understanding

↓

SQL Generator

↓

SQL Validator

↓

Database Query Execution

↓

Result Processing

↓

Chart Metadata Generation

↓

Business Insight Generation

↓

Recommendation Generation

↓

Response to User

---

# SQL Security Boundary

To prevent unsafe database operations, every AI-generated query passes through the SQL Validator.

Allowed:

- SELECT

Blocked:

- DROP
- DELETE
- UPDATE
- INSERT
- ALTER
- TRUNCATE

This ensures the AI Copilot operates in read-only mode.

---

# API Layer

Location:

app/api/routes.py

Major Endpoints:

GET /health

GET /kpis

GET /sales/monthly

GET /sales/state

GET /categories/top

GET /payments/types

GET /reviews/score

GET /forecast/revenue

GET /filters

GET /insights

GET /copilot

---

# Streamlit Dashboard Workflow

User

↓

Select Filters

↓

FastAPI Request

↓

Analytics Engine

↓

Database Query

↓

Visualization Generation

↓

Interactive Dashboard

---

# Dashboard Components

## KPI Cards

- Total Revenue
- Total Orders
- Average Order Value

## Analytics Charts

- Order Status Distribution
- Monthly Revenue Trend
- State Revenue Analysis
- Category Revenue Analysis
- Payment Distribution
- Customer Rating Analysis
- Revenue Forecast

## AI Business Insights

- Revenue Summary
- Top State
- Top Category
- Top Payment Type
- Customer Rating

## AI Business Copilot

- Natural Language Queries
- SQL Transparency
- Result Tables
- Visualizations
- Recommendations
- Query History

---

# Power BI Layer

Location:

powerbi/

File:

Insightgpt Sales Dashboard.pbix

Purpose:

- Executive reporting
- Interactive business dashboards
- Additional visualization layer

---

# Testing Architecture

Location:

tests/

Test Coverage:

- Analytics Tests
- API Tests
- Copilot Tests
- Query Parser Tests
- SQL Generator Tests
- SQL Validator Tests
- Utility Tests

Current Status:

48 Automated Tests Passed

---

# End-to-End Workflow

Olist Dataset

↓

Data Cleaning

↓

Feature Engineering

↓

PostgreSQL Database

↓

FastAPI Analytics Services

↓

Gemini AI Copilot

↓

Forecasting Engine

↓

Streamlit Dashboard

↓

Business Decision Support