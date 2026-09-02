# E-Commerce Analytics Web Application

## Project Overview

This project presents an interactive web application for analysing
e-commerce business performance using Python and Streamlit.

The application converts the Python data analysis into an interactive
dashboard with business KPIs, charts, product analysis, customer analysis,
refund analysis, and business insights.

## Technology Used

- Python
- Pandas
- Scikit-learn
- Joblib
- Streamlit

## Data Sources

The application was developed using six e-commerce datasets:

- Orders
- Order Items
- Order Item Refunds
- Products
- Website Pageviews
- Website Sessions

The raw datasets are not included in this repository.

## Dashboard Sections

### 1. Executive Overview

Displays key business KPIs:

- Total Revenue
- Total COGS
- Total Profit
- Profit Margin
- Total Orders
- Total Customers
- Conversion Rate
- Revenue per Session
- Total Refund Amount

### 2. Website Performance

Includes:

- Total Sessions
- Total Pageviews
- Pageviews per Session
- Conversion Rate
- Revenue per Session
- Repeat Session Rate
- Bounce Rate
- Sessions by Device Type
- Sessions by Marketing Source
- Sessions Trend

### 3. Sales & Product Performance

Includes:

- Total Revenue
- Total Orders
- Total Profit
- Top Products by Sales
- Top Products by Profit
- Product Performance Summary

### 4. Customer Analysis

Includes:

- Total Customers
- Repeat Customers
- Repeat Customer Rate
- Orders per Customer
- Top Customers by Orders
- Customer Revenue Summary

### 5. Refund Analysis

Includes:

- Total Refund Amount
- Refund Rate
- Refunded Items
- Refund Amount by Product
- Refund Summary

### 6. Business Insights

Provides key findings and business recommendations based on the
e-commerce data analysis.

### 7. Conversion Prediction

Provides a machine-learning based prediction of whether a website session is likely to convert.

Users can enter:

- Repeat Session
- Marketing Source
- Marketing Campaign
- Marketing Content
- Device Type
- HTTP Referrer

The application displays the predicted conversion probability and conversion prediction.

## Project Structure

```text
ecommerce_web_app/
│
├── README.md
├── Ecommerce_Data_Analysis_Python.ipynb
├── app.py
├── ecommerce_conversion_model.pkl
└── requirements.txt

## Predictive Modeling

The project includes a Logistic Regression model for predicting website session conversion.

The trained model is saved as:

ecommerce_conversion_model.pkl

The model is integrated into the Streamlit application to provide conversion probability predictions for new website sessions.
