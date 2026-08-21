# InsightGPT — AI Business Intelligence Copilot

An AI-powered Business Intelligence Copilot for **SQL analytics, interactive dashboards, revenue forecasting, data visualization, and natural-language business insights**.

InsightGPT combines **Python, FastAPI, Streamlit, PostgreSQL, SQL, Machine Learning, and Google Gemini AI** to help users explore business data and turn natural-language questions into actionable insights.

---

## Live Demo

### Dashboard

https://insightgpt-dashboard.onrender.com

### Backend API

https://insightgpt-ai-business-intelligence.onrender.com

### API Health Check

https://insightgpt-ai-business-intelligence.onrender.com/health

---

## Dashboard Preview

### Main Business Intelligence Dashboard

The main dashboard provides an overview of business performance through KPIs, order analytics, and monthly revenue trends.

![InsightGPT Main Dashboard](docs/images/Main%20Dashboard.png)

---

### AI Business Copilot

The AI Business Copilot allows users to ask business questions using natural language and receive AI-powered business insights.

![AI Business Copilot](docs/images/quick%20questions%20and%20answer.png)

---

### Result Data and Generated SQL

InsightGPT provides both the query result and the generated SQL, improving transparency and allowing users to understand how the analytical result was produced.

![Result Data and SQL](docs/images/result%20data%20and%20sql.png)

---

### Revenue Forecast

The forecasting module combines historical revenue with future forecast values to provide a forward-looking view of business performance.

![Revenue Forecast](docs/images/revenue%20forecast.png)

---

## Overview

InsightGPT is an AI-powered Business Intelligence application designed to help business users explore sales, customer, product, payment, and revenue data through an interactive dashboard and an AI Business Copilot.

The platform combines:

- Business Intelligence
- Data Analytics
- SQL Analytics
- Machine Learning
- Generative AI
- Interactive Data Visualization

Users can explore business performance through predefined dashboard analytics or ask questions directly using natural language.

---

## Key Features

### Business Intelligence Dashboard

The dashboard provides interactive analysis of:

- Total Revenue
- Total Orders
- Average Order Value
- Order Status Distribution
- Monthly Revenue Trend
- State Revenue Analysis
- Product Category Revenue
- Payment Type Distribution
- Customer Review Scores
- Revenue Forecast
- AI Business Insights

---

### Interactive Filters

Users can filter the dashboard by:

- State
- Product Category
- Payment Type

The selected filters are passed to the backend APIs and applied to the corresponding analytics.

---

### AI Business Copilot

The AI Business Copilot allows users to ask business questions using natural language.

Example questions:

- Which category generates the highest revenue?
- Which state has the highest revenue?
- Which payment type is used most?
- What is the average customer rating?
- Show revenue trend.
- What is the revenue forecast?

The Copilot can return:

- Natural-language answers
- Business insights
- Generated SQL
- Query results
- Data visualizations
- Business recommendations

---

## AI Copilot Workflow

```text
Natural Language Question
            │
            ▼
      Question Parser
            │
            ▼
       SQL Generator
            │
            ▼
       SQL Validator
            │
            ▼
      Database Query
            │
            ▼
       Query Result
            │
            ▼
    Business Interpretation
            │
       ┌────┴────┐
       ▼         ▼
 Visualization  Recommendation
```

---

## System Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    Streamlit Dashboard    │
                    │                           │
                    │  KPIs / Charts / Filters  │
                    │    AI Business Copilot    │
                    └─────────────┬─────────────┘
                                  │
                                  │ HTTP Requests
                                  ▼
                    ┌───────────────────────────┐
                    │       FastAPI API         │
                    │                           │
                    │  Analytics / Copilot APIs │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐        ┌──────────────────┐
          │   PostgreSQL     │        │    Gemini AI     │
          │    Database      │        │   AI Copilot     │
          └──────────────────┘        └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ Analytics & ML   │
          │ Revenue Forecast │
          └──────────────────┘
```

---

## Tech Stack

### Programming

- Python

### Backend

- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Psycopg2

### Data Analytics

- Pandas
- NumPy
- Plotly

### Machine Learning

- Scikit-Learn
- Revenue Forecasting

### Generative AI

- Google Gemini API

### Frontend

- Streamlit

### Testing

- Pytest
- HTTPX

### Deployment

- GitHub
- Render

---

## Project Structure

```text
InsightGPT-AI-Business-Intelligence-Copilot/
│
├── app/
│   ├── analytics/
│   │   ├── categories.py
│   │   ├── filters.py
│   │   ├── insights.py
│   │   ├── payments.py
│   │   ├── revenue.py
│   │   └── reviews.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── dashboard/
│   │   └── dashboard.py
│   │
│   ├── database/
│   │   ├── config.py
│   │   ├── connection.py
│   │   └── load_data.py
│   │
│   ├── llm/
│   │   ├── copilot.py
│   │   ├── query_parser.py
│   │   ├── response_models.py
│   │   ├── sql_generator.py
│   │   └── sql_validator.py
│   │
│   ├── ml/
│   │   └── forecasting.py
│   │
│   └── services/
│       └── analytics.py
│
├── docs/
│
├── notebooks/
│
├── powerbi/
│
├── sql/
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `/health` | API health check |
| `/kpis` | Business KPI metrics |
| `/sales/monthly` | Monthly revenue analysis |
| `/sales/state` | State-level revenue analysis |
| `/categories/top` | Top product categories |
| `/payments/types` | Payment type analysis |
| `/reviews/score` | Customer review analysis |
| `/forecast/revenue` | Revenue forecasting |
| `/insights` | Business insights |
| `/filters` | Dashboard filter values |
| `/copilot` | AI Business Copilot |

---

## Dashboard Analytics

### Revenue Analytics

The dashboard analyzes:

- Total revenue
- Monthly revenue trends
- Average order value
- State-level revenue
- Revenue by product category

### Order Analytics

The dashboard provides:

- Total orders
- Order status distribution
- Order-level performance indicators

### Payment Analytics

Payment behavior can be analyzed using payment type distribution.

### Customer Analytics

Customer satisfaction is analyzed using review scores and average customer rating.

### Forecasting

The application provides historical revenue and forecasted revenue through the forecasting module.

---

## Example Business Questions

The AI Business Copilot can answer questions such as:

- Which category generates the highest revenue?
- Which state has the highest revenue?
- Which payment type is used most?
- What is the average customer rating?
- Show revenue trend.
- What is the revenue forecast?

The returned response can include the answer, supporting data, generated SQL, visualization, and recommendation.

---

## SQL Transparency

One of the key features of InsightGPT is SQL transparency.

When the Copilot generates a database query, users can expand the generated SQL section to inspect the query used for the business question.

The project also includes SQL validation logic to prevent destructive database operations.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/atlassandx90/InsightGPT-AI-Business-Intelligence-Copilot.git
```

```bash
cd InsightGPT-AI-Business-Intelligence-Copilot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

GEMINI_API_KEY=your_gemini_api_key
```

> Do not commit `.env` or database credentials to GitHub.

### 5. Run the FastAPI backend

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

### 6. Run the Streamlit dashboard

```bash
streamlit run app/dashboard/dashboard.py
```

The dashboard will open in your browser.

---

## Deployment

InsightGPT is deployed using Render.

### Backend

https://insightgpt-ai-business-intelligence.onrender.com

### Frontend

https://insightgpt-dashboard.onrender.com

The Streamlit frontend communicates with the deployed FastAPI backend through HTTP API endpoints.

---

## Testing

The project includes automated tests for:

- Analytics
- API endpoints
- AI Copilot
- Query parsing
- SQL generation
- SQL validation
- Utility functions

Run the test suite:

```bash
pytest
```

---

## Security

Sensitive configuration is stored using environment variables.

The following information should never be committed to the repository:

- Database passwords
- API keys
- `.env` files
- Production secrets

SQL validation is also used to provide an additional safety layer before generated SQL is executed.

---

## Business Use Cases

InsightGPT can support:

- Sales performance monitoring
- Revenue analysis
- Product performance analysis
- Geographic performance analysis
- Payment behavior analysis
- Customer satisfaction monitoring
- Revenue forecasting
- Natural-language business intelligence

The goal is to reduce the time between asking a business question and obtaining an actionable data-driven insight.

---

## Project Status

**v1.0 — Working & Deployed**

### Current Release Includes

- Interactive Business Intelligence Dashboard
- FastAPI backend
- PostgreSQL integration
- AI Business Copilot
- Natural-language business questions
- SQL generation
- SQL validation
- Interactive Plotly visualizations
- Revenue forecasting
- Business insights
- Business recommendations
- Dashboard filters
- Production deployment
- Stable release

**Release:** `v1.0-working-dashboard`

---

## Future Improvements

Potential future improvements include:

- More advanced natural-language analytics
- Additional business KPIs
- More advanced forecasting models
- Improved customer segmentation
- Additional visualization types
- More detailed AI recommendations
- Production monitoring
- Improved query understanding
- Advanced comparative analytics

---

## Author

**Abhijeet**

Data Analyst | Business Intelligence | SQL | Python | AI Analytics

- LinkedIn: [Connect with me](https://www.linkedin.com/in/abhijeetroy9/)
- Portfolio: [View my portfolio](https://abhijeetroy.netlify.app/)
- GitHub: [View my GitHub profile](https://github.com/atlassandx90)

---

## Project Keywords

`business-intelligence` `data-analytics` `ai-copilot` `sql` `python` `fastapi` `streamlit` `postgresql` `machine-learning` `generative-ai` `gemini` `revenue-forecasting` `data-visualization`
