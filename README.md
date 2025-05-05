# 🪙 Crypto Data Pipeline with Airflow, PostgreSQL, and Docker

A robust data pipeline that fetches real-time cryptocurrency data from the [CoinGecko API](https://www.coingecko.com/en/api), stores it in a PostgreSQL database, and orchestrates the entire workflow using Apache Airflow — all containerized via Docker for easy deployment and scalability.

---

## 🚀 Features

- ✅ Automated data extraction from CoinGecko API
- ✅ ETL pipeline with Apache Airflow
- ✅ PostgreSQL integration for persistent storage
- ✅ Modular, scalable architecture using Docker
- ✅ Easily extensible for more coins or additional analytics

---

## 🧱 Tech Stack

- **Python**: Data extraction and transformation
- **PostgreSQL**: Data warehouse
- **Apache Airflow**: Workflow orchestration
- **Docker**: Containerized deployment
- **CoinGecko API**: Free crypto data source

---

## 📌 Project Architecture

```text
            +--------------------+
            | CoinGecko API      |
            +--------+-----------+
                     |
                     v
            +--------+-----------+
            |   Airflow DAGs     |
            |  (ETL pipeline)    |
            +--------+-----------+
                     |
         +-----------+------------+
         |                        |
         v                        v
+----------------+      +---------------------+
| fetch_data.py  |      | PostgreSQL Database |
| (calls API)     --->  | Table: crypto_data  |
+----------------+      +---------------------+


---
```
## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/crypto-data-pipeline.git
cd crypto-data-pipeline
