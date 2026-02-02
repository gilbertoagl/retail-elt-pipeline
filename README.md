# Automated Retail ELT Pipeline (End-to-End)

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-red?style=for-the-badge&logo=apache-airflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Core-orange?style=for-the-badge&logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=for-the-badge&logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-13-336791?style=for-the-badge&logo=postgresql&logoColor=white)

**End-to-End Data Engineering Pipeline that orchestrates the ingestion, transformation, and validation of simulated retail sales data, fully deployed in Docker containers.**

---

## Final Result: Compliance Dashboard
![Dashboard Preview](Dashboard_RetailData.png)
*(Metabase Visualization: Automatic comparison of Actual Sales vs Business Objectives)*

---

## Project Description

This project simulates a real-world data environment for a Retail company. The system extracts "live" transactions from a public API, stores them in a Data Warehouse, and transforms them to answer a critical business question: **Which product categories are meeting their monthly sales targets?**

Unlike a traditional ETL, an **ELT (Extract, Load, Transform)** architecture was implemented, leveraging the power of PostgreSQL for heavy processing and **dbt** for data lifecycle management and quality testing.

### Key Features
* **Robust Orchestration:** Scheduled Airflow DAGs with retry handling and dependencies.
* **Data Quality:** "Quality Gates" implemented with dbt tests that halt the pipeline if duplicates or nulls are detected.
* **Idempotency:** The pipeline can be executed multiple times without duplicating data or creating inconsistencies.
* **Infrastructure as Code (IaC):** The entire environment spins up with a single Docker Compose command.

---

## System Architecture

The data flow follows a modular architecture:

```mermaid
graph LR
    A[External API\nFakeStoreAPI] -->|Extract JSON| B(Python Operator\nAirflow)
    B -->|Load Raw Data| C[(PostgreSQL DW\nSchema: Public)]
    C -->|Transform & Test| D{dbt Core}
    D -->|Materialize Tables| E[Final Tables\nSchema: Public]
    E -->|Visualize| F[Metabase Dashboard]
```