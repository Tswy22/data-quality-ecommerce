# E-commerce Transaction Dashboard

This project provides an interactive dashboard to visualize and analyze e-commerce transaction data using *Streamlit* and *DuckDB*. The dashboard allows users to explore transaction trends, key metrics, and data quality issues with interactive filters.

## Features
- **Total Transactions**: Displays the total number of transactions.
- **Total Revenue**: Shows the total revenue generated from all transactions.
- **Average Amount**: Displays the average transaction amount.
- **Transactions with Issues**: Identifies transactions that have issues such as negative amounts or canceled status.
- **Transaction Status Distribution**: Visualizes the distribution of transaction statuses.
- **Daily Transaction Summary**: Displays daily transaction counts and revenue.
- **Data Profiling**: Provides insights into data quality issues like void/cancel transactions and negative amounts.

## Installation

### Clone the Repository
First, clone the repository:
```bash
git clone https://github.com/Tswy22/data-quality-ecommerce.git
cd data-quality-ecommerce

### Install Dependencies
Install the required Python dependencies:
pip install -r requirements.txt

### Database Setup
Ensure you have the ecommerce.duckdb file in the project directory. This file should contain the transaction data. If you don’t have the data, you’ll need to load or generate the DuckDB file yourself.

### Run the App
Once the setup is complete, run the Streamlit app using:
streamlit run streamlit.py
You can access the dashboard at http://localhost:8501.

### Usage
Once the application is running:
- Use the sidebar filters to select the category, payment method, and date range for transactions.
- View visualizations of transaction status distributions, trends, and daily summaries.
- Analyze data quality issues such as negative amounts or canceled transactions.
- The dashboard displays key metrics, including total transactions, total revenue, and average amount.

### Running with Docker
You can also run the application using Docker. Here’s how:

### Build the Docker Image:
docker build -t data-quality-ecommerce-streamlit .

### Run the Docker Container:
docker run -p 8501:8501 data-quality-ecommerce-streamlit
The app will be available at http://localhost:8501.

### Contributing
Contributions are welcome! If you'd like to improve this project, follow these steps:
1.Fork the repository.
2.Create a new branch (git checkout -b feature-name).
3.Make your changes and commit them (git commit -am 'Add new feature').
4.Push to your fork (git push origin feature-name).
5.Open a pull request to merge your changes into the main repository.
