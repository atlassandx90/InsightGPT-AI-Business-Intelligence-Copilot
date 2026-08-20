# Database Design

# Database Name

insightgpt

---

# Database Type

PostgreSQL

---

# Business Domain

Retail E-Commerce Analytics

Dataset Source:
- Olist Brazilian E-Commerce Dataset

---

# Database Purpose

The database acts as the analytical foundation of InsightGPT.

It stores cleaned and engineered business data used for:

- KPI Reporting
- Revenue Analytics
- State Performance Analysis
- Product Category Analysis
- Payment Analysis
- Customer Review Analysis
- AI Copilot Queries
- Revenue Forecasting
- Business Insight Generation

---

# Data Pipeline

Raw CSV Files

↓

Data Cleaning

↓

Feature Engineering

↓

PostgreSQL Database

↓

Analytics Services

↓

FastAPI APIs

↓

AI Copilot & Dashboard

---

# Core Tables

## customers

Purpose:
Stores customer location information.

Primary Key:
- customer_id

Columns:
- customer_id
- customer_unique_id
- customer_city
- customer_state

Relationship:
- One Customer → Many Orders

---

## orders

Purpose:
Stores order lifecycle information.

Primary Key:
- order_id

Foreign Key:
- customer_id → customers.customer_id

Columns:
- order_id
- customer_id
- order_status
- order_purchase_timestamp
- order_delivered_customer_date
- order_estimated_delivery_date

Relationship:
- One Order → Many Order Items
- One Order → Many Payments
- One Order → One Review

---

## orderitems

Purpose:
Stores products purchased within orders.

Columns:
- order_id
- product_id
- seller_id
- price
- freight_value

Foreign Keys:
- order_id → orders.order_id
- product_id → products.product_id
- seller_id → sellers.seller_id

Relationship:
- Many Order Items → One Product
- Many Order Items → One Seller

---

## products

Purpose:
Stores product information.

Primary Key:
- product_id

Columns:
- product_id
- product_category_name
- product_weight_g
- product_length_cm
- product_height_cm
- product_width_cm

Relationship:
- One Product → Many Order Items

---

## sellers

Purpose:
Stores seller information.

Primary Key:
- seller_id

Columns:
- seller_id
- seller_city
- seller_state

Relationship:
- One Seller → Many Order Items

---

## payments

Purpose:
Stores payment transaction details.

Foreign Key:
- order_id → orders.order_id

Columns:
- order_id
- payment_type
- payment_installments
- payment_value

Relationship:
- Many Payments → One Order

---

## reviews

Purpose:
Stores customer review information.

Foreign Key:
- order_id → orders.order_id

Columns:
- order_id
- review_score

Relationship:
- One Review → One Order

---

## categories

Purpose:
Maps Portuguese category names to English category names.

Primary Key:
- product_category_name

Columns:
- product_category_name
- product_category_name_english

Relationship:
- One Category → Many Products

---

## geolocation

Purpose:
Stores geographical reference information.

Columns:
- geolocation_zip_code_prefix
- geolocation_city
- geolocation_state

Used For:
- Geographic analysis
- State-level reporting
- Location enrichment

---

# Relationship Overview

customers
    |
    | 1:M
    |
orders
    |
    +----------------+
    |                |
    | 1:M            | 1:M
    |                |
orderitems       payments
    |
    |
    +--------+
    |        |
    | M:1    | M:1
    |        |
products   sellers

orders
   |
   | 1:1
   |
reviews

categories
   |
   | 1:M
   |
products

---

# Analytics Supported

The database supports:

- Total Revenue Calculation
- Total Orders Calculation
- Average Order Value
- Monthly Revenue Trends
- State Revenue Analysis
- Product Category Analysis
- Payment Distribution Analysis
- Customer Rating Analysis
- Revenue Forecasting
- AI Copilot Query Execution

---

# AI Copilot Database Access

The AI Copilot converts natural language questions into SQL queries using Google Gemini.

Example:

Question:
"Which category generates the highest revenue?"

↓

Generated SQL

↓

SQL Validation

↓

Database Execution

↓

Business Insight

↓

Visualization

---

# SQL Security Layer

AI-generated SQL is validated before execution.

Allowed Operations:

- SELECT

Blocked Operations:

- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- TRUNCATE
- CREATE
- REPLACE

Only read-only analytical queries are permitted.

Validation is enforced through:

- sql_generator.py
- sql_validator.py

All database access from the AI Copilot passes through the validation layer before execution.

---

# Database Access Layer

Database connectivity is managed through:

- app/database/config.py
- app/database/connection.py

Database initialization scripts:

- sql/create database.sql
- sql/create tables.sql

Data loading utilities:

- app/database/load_data.py

---

# Scalability Notes

Current implementation is optimized for:

- Local PostgreSQL deployment
- Analytical workloads
- Dashboard reporting
- AI-generated business queries

Future improvements may include:

- Query caching
- Materialized views
- Data warehouse integration
- Cloud-hosted PostgreSQL
- Multi-user access control