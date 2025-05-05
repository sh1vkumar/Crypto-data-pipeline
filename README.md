# 🪙 Crypto ETL Pipeline with Airflow, PostgreSQL, and Docker

This project implements a fully automated ETL pipeline that:
- 📡 Fetches real-time cryptocurrency data from the [CoinGecko API](https://www.coingecko.com/en/api)
- 🗃 Loads the data into a PostgreSQL database
- ⚙️ Uses Apache Airflow for scheduling and orchestration
- 🐳 Is containerized and deployable via Docker for consistency and portability

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
