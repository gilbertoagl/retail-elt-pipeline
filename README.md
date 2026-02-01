# Automated Retail ELT Pipeline (End-to-End)

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.7-red)
![dbt](https://img.shields.io/badge/dbt-Core-orange)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

**Este proyecto consta de un pipeline de datos robusto que ingesta, transforma y audita datos de ventas retail, diseñado para soportar fallos y garantizar calidad de datos.**

---

## Resultado Final (Dashboard)
![Dashboard Preview](Dashboard_RetailData.png)
*Comparativa de Ventas Reales vs Objetivos de Negocio procesada automáticamente*

---

## Caso de Negocio
El objetivo del proyecto es procesar transacciones diarias de una tienda retail (simulada vía API) para generar un Reporte de Cumplimiento de Ventas. El sistema cruza los datos transaccionales vivos con objetivos estáticos de negocio para determinar qué categorías están cumpliendo sus KPIs.

## Arquitectura del Sistema

El flujo de datos sigue una arquitectura ELT (Extract, Load, Transform) contenerizada en Docker:

```mermaid
graph LR
    A[API Externa] -->|Extract JSON| B(Python Script)
    B -->|Load Raw Data| C[(PostgreSQL DW)]
    C -->|Transform & Test| D{dbt Core}
    D -->|Materialize Tables| E[Tablas Finales]
    E -->|Visualize| F[Metabase Dashboard]
```