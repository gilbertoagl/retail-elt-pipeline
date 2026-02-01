from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import requests
import json
from sqlalchemy import create_engine, text

# CONFIGURACIÓN
default_args = {
    'owner': 'gilberto',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

db_connection_str = 'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'
db_connection = create_engine(db_connection_str)

# EXTRACCIÓN API REAL
def extract_and_load():
    url = "https://fakestoreapi.com/products"
    print(f"--- Descargando datos reales desde {url} ---")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            
            # Limpieza básica
            df['rating'] = df['rating'].apply(json.dumps)
            df = df[['id', 'title', 'price', 'category', 'rating']]
            df['ingestion_date'] = datetime.now()
            
            # Borrar datos viejos
            print("--- Limpiando base de datos (CASCADE) ---")
            with db_connection.begin() as conn:
                conn.execute(text("DROP TABLE IF EXISTS raw_products CASCADE;"))
            
            # Cargar datos nuevos
            print("--- Cargando a Postgres... ---")
            df.to_sql('raw_products', con=db_connection, if_exists='replace', index=False)
            
            print("--- ¡Carga Exitosa! ---")
        else:
            print(f"Error en API: {response.status_code}")
            raise Exception("Fallo en API")
            
    except Exception as e:
        print(f"Error crítico: {e}")
        raise e

# 2. DEFINICIÓN DEL DAG
with DAG(
    dag_id='3_pipeline_completo_elt',
    default_args=default_args,
    description='Pipeline Final: API -> Postgres -> dbt (Joins & Tests)',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Extraer
    t1_extract_load = PythonOperator(
        task_id='carga_datos_crudos',
        python_callable=extract_and_load
    )

    # Transformar (dbt run)
    t2_transform_dbt = BashOperator(
        task_id='transformacion_dbt',
        bash_command='cd /opt/airflow/dags/retail_project && /home/airflow/.local/bin/dbt run --profiles-dir .'
    )

    # Testear (dbt test)
    t3_test_dbt = BashOperator(
        task_id='test_calidad_datos',
        bash_command='cd /opt/airflow/dags/retail_project && /home/airflow/.local/bin/dbt test --profiles-dir .'
    )

    t1_extract_load >> t2_transform_dbt >> t3_test_dbt