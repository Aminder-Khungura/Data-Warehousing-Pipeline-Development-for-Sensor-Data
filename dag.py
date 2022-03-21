from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryUpdateTableOperator
from datetime import datetime
import mysql.connector


def read_data():
    database = mysql.connector.connect(host='localhost', user='root', password='pass', port='3306', database='sensor_data', auth_plugin='mysql_native_password')
    cursor = database.cursor()
    cursor.execute('SELECT * FROM data')
    data = cursor.fetchall()
    cursor.close();
    database.close()

    date = []
    temperature = []
    heart_rate = []
    for i in range(len(data)):
        date.append(data[i][0])
        temperature.append(data[i][1])
        heart_rate.append(data[i][2])
    return date, temperature, heart_rate


def process_data(ti):
    values = ti.xcom_pull(task_ids='Read Values From MySQL')
    date = values[0].apply(lambda x: x.strftime("%m/%d/%Y, %H:%M:%S"))
    temperature = values[1].apply(lambda x: float(x))
    heart_rate = values[2].apply(lambda x: float(x))
    return date, temperature, heart_rate


with DAG(
    'sensor_dag',
    start_date=datetime(2021,1,1),
    schedule_interval='@daily',
    catchup=False
) as dag:
    read_data = PythonOperator(
        task_id='Read Values From MySQL',
        python_callable=read_data
    )

    data_conversion = PythonOperator(
        task_id='Process Data',
        python_callable=process_data
    )

    upload_data = BigQueryUpdateTableOperator(
        task_id='Load Data Into BigQuery',
        dataset_id=sensor_data,
        dataset_resource={"description": "Updated dataset"},
    )

    read_data >> data_conversion >> upload_data