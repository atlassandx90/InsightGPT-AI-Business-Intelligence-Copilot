# Table Mapping

This document maps the original Olist dataset files to the PostgreSQL tables used in the InsightGPT Business Intelligence Copilot.

---

# Dataset Source

Olist Brazilian E-Commerce Dataset

---

# Source-to-Database Mapping

| Source CSV File | PostgreSQL Table | Purpose |
|-----------------|------------------|----------|
| customers.csv | customers | Customer location and identity data |
| orders.csv | orders | Order lifecycle and status information |
| orderitems.csv | orderitems | Product-level order transactions |
| products.csv | products | Product catalog information |
| sellers.csv | sellers | Seller information |
| payments.csv | payments | Payment transaction details |
| reviews.csv | reviews | Customer review scores |
| categories.csv | categories | Category translation and mapping |
| geolocation.csv | geolocation | Geographic reference data |

---

# Data Processing Pipeline

Raw Dataset

↓

data/raw/

↓

Data Cleaning

↓

data/cleaned/

↓

Feature Engineering

↓

data/engineered/

↓

PostgreSQL Tables

↓

Analytics APIs

↓

AI Copilot & Dashboard

---

# Cleaned Dataset Mapping

| Cleaned File | Database Table |
|-------------|----------------|
| customers_cleaned.csv | customers |
| orders_cleaned.csv | orders |
| orderitems_cleaned.csv | orderitems |
| products_cleaned.csv | products |
| sellers_cleaned.csv | sellers |
| payments_cleaned.csv | payments |
| reviews_cleaned.csv | reviews |
| categories_cleaned.csv | categories |
| geolocation_cleaned.csv | geolocation |

---

# Engineered Dataset Mapping

| Engineered File | Database Table |
|----------------|----------------|
| customers_engineered.csv | customers |
| orders_engineered.csv | orders |
| orderitems_engineered.csv | orderitems |
| products_engineered.csv | products |
| sellers_engineered.csv | sellers |
| payments_engineered.csv | payments |
| reviews_engineered.csv | reviews |
| categories_engineered.csv | categories |
| geolocation_engineered.csv | geolocation |

---

# Business Usage by Table

| Table | Used In |
|---------|---------|
| customers | Customer Analytics, State Analysis |
| orders | KPI Calculation, Revenue Analysis |
| orderitems | Revenue Analytics, Product Analytics |
| products | Category Analytics |
| sellers | Seller Analysis |
| payments | Payment Analysis |
| reviews | Customer Rating Analysis |
| categories | Product Category Reporting |
| geolocation | Geographic Reporting |

---

# AI Copilot Table Access

The AI Copilot can generate analytical SQL queries against approved business tables.

Accessible Tables:

- customers
- orders
- orderitems
- products
- sellers
- payments
- reviews
- categories
- geolocation

All generated SQL queries pass through the SQL validation layer before execution.

---

# Notes

- Source files are stored under `data/raw/`
- Cleaned datasets are stored under `data/cleaned/`
- Engineered datasets are stored under `data/engineered/`
- Data is loaded into PostgreSQL using the database loading utilities
- Analytics APIs and AI Copilot read data from PostgreSQL