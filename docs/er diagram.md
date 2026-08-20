# Entity Relationship Diagram (ERD)

## Database: insightgpt

The project uses the Olist Brazilian E-Commerce Dataset and stores cleaned business data inside PostgreSQL.

---

# Core Entities

## Customers

Primary Key:
- customer_id

Attributes:
- customer_unique_id
- customer_city
- customer_state

Relationships:
- One Customer → Many Orders

---

## Orders

Primary Key:
- order_id

Foreign Keys:
- customer_id → customers.customer_id

Attributes:
- order_status
- order_purchase_timestamp
- order_delivered_customer_date
- order_estimated_delivery_date

Relationships:
- One Order → Many Order Items
- One Order → Many Payments
- One Order → One Review

---

## Order Items

Composite Relationship Table

Foreign Keys:
- order_id → orders.order_id
- product_id → products.product_id
- seller_id → sellers.seller_id

Attributes:
- price
- freight_value

Relationships:
- Many Order Items → One Product
- Many Order Items → One Seller

---

## Products

Primary Key:
- product_id

Attributes:
- product_category_name
- product_weight_g
- product_length_cm
- product_height_cm
- product_width_cm

Relationships:
- One Product → Many Order Items

---

## Sellers

Primary Key:
- seller_id

Attributes:
- seller_city
- seller_state

Relationships:
- One Seller → Many Order Items

---

## Payments

Foreign Key:
- order_id → orders.order_id

Attributes:
- payment_type
- payment_installments
- payment_value

Relationships:
- Many Payments → One Order

---

## Reviews

Foreign Key:
- order_id → orders.order_id

Attributes:
- review_score

Relationships:
- One Review → One Order

---

## Categories

Primary Key:
- product_category_name

Attributes:
- product_category_name_english

Relationships:
- One Category → Many Products

---

# Relationship Summary

customers
    |
    | 1:M
    |
orders
    |
    +------------------+
    |                  |
    | 1:M              | 1:M
    |                  |
order_items        payments
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

# AI Layer (Application Level)

Natural Language Question
            |
            v
      Gemini LLM
            |
            v
      SQL Generator
            |
            v
      SQL Validator
            |
            v
       PostgreSQL
            |
            v
      Result Dataset
            |
            +------------------+
            |                  |
            v                  v
      Chart Generator     Business Insights
            |
            v
      Streamlit Dashboard