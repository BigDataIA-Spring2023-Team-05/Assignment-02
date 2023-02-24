from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import BranchPythonOperator
# from airflow.utils.dates import days_ago
# from airflow.models.param import Param
from datetime import timedelta
from sql_aws_metadata import aws_extract_data_to_sqlite, populate_database
from datetime import datetime
# import pendulum
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
 
# user_input = {Metadata
# "user_sleep_timer": Param(30, type='integer', minimum=10, maximum=120),
# }
 
# default_args = {
# 'owner': 'airflow',
# # 'depends_on_past': False,
# # 'email_on_failure': ''' hindupur.v@northeastern.edu ''',
# # 'email_on_retry': False,
# # # 'schedule_interval': '@daily',
# # 'retries': 1,
# # 'retry_delay': timedelta(seqconds=5),
# start_date': datetime(2023, 02, 24)
# }
 
# now = pendulum.now(tz="UTC")
# now_to_the_hour = (now - datetime.timedelta(0, 0, 0, 0, 0, 3)).replace(minute=0, second=0, microsecond=0)
# START_DATE = now_to_the_hour
# DAG_NAME = "dag_task_1"
 
# dag = DAG(
# dag_id=DAG_NAME,
# schedule="0 0 * * *", 
# start_date=days_ago(0),
# catchup=False,
# dagrun_timeout=timedelta(minutes=60),
# tags=["labs", "damg7245"],
# default_args={"depends_on_past": True},
# start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
# )
 
# dag = DAG('aws_extraction_to_sqlite')
# PythonOperator(dag=dag,
# task_id='aws_task_powered_by_airflow',
# provide_context=False,
# python_callable=sql_f.aws_extract_data_to_sqlite,
# op_args=['arguments_passed_to_callable'],
# op_kwargs={'keyword_argument':'which will be passed to function'})
 
# run_this_1 = PythonOperator(task_id="aws_task_powered_by_airflow", dag=dag)
# # run_this_2 = EmptyOperator(task_id="run_this_2", dag=dag)
# run_this_1.set_upstream(run_this_1)
# #run_this_3 = EmptyOperator(task_id="run_this_3", dag=dag)
# #run_this_3.set_upstream(run_this_2)
 
# with DAG('target_dag', 
# schedule_interval="0 0 * * *", 
# default_args=default_args, 
# catchup=False) as dag:
 
# storing = BashOperator(
# task_id='storing',
# bash_command='sleep 30'
# )
 
# aws_to_sql_extraction_process = PythonOperator(dag=dag,
# task_id='aws_task_powered_by_airflow',
# python_callable=sql_f.aws_extract_data_to_sqlite)
 
# trigger_target = TriggerDagRunOperator(
# task_id='trigger_target',
# trigger_dag_id='target_dag'
# )
 
# storing >> aws_to_sql_extraction_process >> trigger_target
 
with DAG("aws_extract_dag", start_date=datetime(2023, 2, 24), schedule_interval="*/5 * * * *", catchup=False) as dag: 
    sleep_process = BashOperator(
    task_id='storing',
    bash_command='sleep 30'
    )
    
    aws_to_sql_extraction_process = PythonOperator(dag=dag,
    task_id='aws_task_powered_by_airflow',
    python_callable=aws_extract_data_to_sqlite
    )

    database_populated = PythonOperator(dag=dag,
    task_id='database_populate',
    python_callable=populate_database
    )
    
    sleep_process >> aws_to_sql_extraction_process >> database_populate