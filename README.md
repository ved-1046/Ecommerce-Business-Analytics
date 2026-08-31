# 🛒 E-Commerce Business Analytics & Customer Intelligence

An end-to-end **Business Analytics and Machine Learning project** built using **Python, SQL, MySQL, Pandas, Streamlit, Scikit-learn, and Folium** to analyze e-commerce data, uncover business insights, and understand customer behavior.

## 📌 Project Overview

This project analyzes a real-world e-commerce dataset to understand **sales performance, customer behavior, payment methods, product categories, and geographical revenue distribution**.

The project also applies **RFM analysis, K-Means clustering, and repeat purchase prediction** to extract deeper customer-level insights.

## 🎯 Business Problems Solved

- Which states and cities generate the highest revenue?
- How does revenue change over time?
- Which payment methods are most preferred?
- Which product categories perform best?
- How is revenue distributed geographically?
- What different customer segments exist based on purchasing behavior?
- Can customer purchasing behavior be used to predict repeat purchases?

## 🚀 Project Features

- Interactive KPI Dashboard
- Monthly Revenue Trend
- Revenue by State
- Payment Method Distribution
- Top 10 Revenue-Generating Cities
- Top Product Categories
- Geographic Revenue Heatmap
- Dynamic State Filtering
- RFM Customer Analysis
- K-Means Customer Segmentation
- Repeat Purchase Prediction Experiments

## 🤖 Machine Learning

### Customer Segmentation

Customers are analyzed using **RFM (Recency, Frequency, Monetary)** features.

**ML Pipeline:**

- RFM Feature Engineering
- Data Distribution Analysis
- Log Transformation
- Feature Scaling using StandardScaler
- K-Means Clustering
- Elbow Method
- Silhouette Score

The final segmentation identifies four customer groups:

- **High-Value Repeat**
- **Recent Customers**
- **High-Value Inactive**
- **Low-Value Inactive**

### Repeat Purchase Prediction

A supervised ML experiment was also developed to predict whether a customer would purchase again.

**Features explored:**

- Recency
- Frequency
- Monetary
- Average Order Value
- Customer Lifetime
- Average Payment per Order

**Models evaluated:**

- Logistic Regression
- Random Forest
- XGBoost
- XGBoost with class-imbalance handling

Model performance was evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

The analysis highlighted the challenges of predicting repeat purchases due to the **highly imbalanced target variable**.

## 🛠 Tech Stack

- Python
- SQL
- MySQL
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SQLAlchemy
- PyMySQL
- Streamlit
- Matplotlib
- Folium
- Streamlit-Folium

## 📚 Skills Demonstrated

### SQL
- Joins
- Aggregate Functions
- GROUP BY
- Filtering & Sorting
- Business Query Writing

### Python & Machine Learning
- Data Cleaning
- Data Merging
- RFM Analysis
- Feature Engineering
- Log Transformation
- Feature Scaling
- K-Means Clustering
- Classification
- Model Evaluation
- Handling Class Imbalance

### Business Analytics
- KPI Development
- Revenue Analysis
- Customer Analysis
- Product Analysis
- Payment Analysis
- Geospatial Analysis

## 📈 Key Insights

- Identified high-revenue states and cities.
- Analyzed monthly revenue trends.
- Compared customer payment preferences.
- Identified top-performing product categories.
- Segmented customers based on purchasing behavior.
- Identified high-value and repeat customer groups.
- Evaluated the challenges of repeat-purchase prediction in a highly imbalanced dataset.

## ▶️ Getting Started

### Clone the Repository

```bash
git clone https://github.com/ved-1046/Ecommerce-Business-Analytics.git
cd Ecommerce-Business-Analytics
pip install -r requirements.txt
streamlit run app.py

👩‍💻 Author
Vedika Tamshetti
```



