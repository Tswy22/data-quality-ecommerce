# E-commerce Transaction Dashboard

This project provides an interactive dashboard to visualize and analyze e-commerce transactions using **Streamlit** and **DuckDB**. The dashboard allows users to explore transaction trends, key metrics, and detect data quality issues with interactive filters.

## Features
- **Total Transactions & Revenue** – Displays key business metrics.
- **Transaction Status Distribution** – Visualizes transaction categories.
- **Daily Transaction Summary** – Shows daily transaction counts and revenue.
- **Data Quality Insights** – Identifies issues like void transactions and negative amounts.
- **Interactive Filters** – Allows exploration by category, payment method, and date range.

## Installation
### 1.Clone the Repository
<pre><code>
git clone https://github.com/YourUsername/data-quality-ecommerce.git
cd data-quality-ecommerce
</code></pre>

### 2.Install Dependencies
<pre><code>
pip install -r requirements.txt
</code></pre>
  
### 3.Set Up the Database
Ensure ecommerce.duckdb exists in the project directory. If missing, generate or load the transaction data.

### 4.Run the App
streamlit run streamlit.py
Access the dashboard at: http://localhost:8501

Running with Docker
Build & Run the Docker Container
If you want to run the application inside a Docker container, follow these steps:
1.Build the Docker image:
docker-compose up --build
2.Access the dashboard: Open your web browser and go to http://localhost:8501.

Data Generation
The data_generation.py file is responsible for generating both historical transaction data and daily transaction data with optional data issues. The following functions are available:
- generate_transactions: Generates 1,000,000 historical transaction records.
- simulate_daily_transactions: Simulates daily transaction records for a given number of days.
To generate the data:
python data_generation.py

Data Storage
The data_storage.py file handles the process of storing transaction data in a DuckDB database. It loads both historical and daily transaction data into separate tables.
To load the data into DuckDB:
python data_storage.py

Data Profiling
The data_profiling.py file runs queries against the DuckDB database to provide data quality insights. It checks for:
- Void/Cancel transactions without initial 'paid' status.
- Negative transaction amounts.
- The distribution of transaction statuses.
- Daily transaction trends.

Running the Application
Streamlit Application:
- The streamlit.py file is the core of the dashboard application. It allows users to filter and explore transaction data interactively.
To run the application, simply run:
streamlit run streamlit.py
The dashboard provides key metrics such as:
- Total transactions
- Total revenue
- Average transaction amount
- Transactions with issues
You can filter the data by category, payment method, and date range.

Docker Configuration
Dockerfile
The Dockerfile creates an image for the Streamlit application, installs dependencies from the requirements.txt file, and exposes port 8501 for the Streamlit dashboard.
docker-compose.yaml
The docker-compose.yaml file simplifies the process of building and running the application with Docker. It ensures that the Streamlit application is correctly configured to run in a container.
