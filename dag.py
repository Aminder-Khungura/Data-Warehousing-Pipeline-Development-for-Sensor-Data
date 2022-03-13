from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.mysql_to_gcs import MySqlToGoogleCloudStorageOperator
from airflow.operators.mysql_operator import mysql_conn_id
from datetime import datetime


connection_id = mysql_conn_id(Host='localhost', Login='root', Password='root', Port=3306)


def convert_str(x):
    return float(x)


with DAG('Sensor_dag', start_date=datetime(2021, 1, 1), schedule_interval='@daily', catchup=False) as dag:

    Task_1 = MySqlOperator(task_id='get_data', sql=r"""SELECT * FROM Sensor_DB;""", dag=dag)

    Task_2 = PythonOperator(
        task_id='Convert str to float',
        python_callable=convert_str()
    )

    Task_3 = MySqlToGoogleCloudStorageOperator(mysql_conn_id='connection_id', ensure_utc=False, *args, **kwargs)