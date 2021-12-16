from datetime import datetime
from logging import log

from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.sqlite.hooks.sqlite import SqliteHook
from airflow.providers.sqlite.operators.sqlite import SqliteOperator

from git_app.git_app_config import worker_orgs, worker_repos

default_args = {
    'start_date': datetime(2021, 12, 1)
}


def _processing_orgs(ti):
    orgs_repos_url = [url for url in worker_orgs.run()]
    return orgs_repos_url


def _processing_repos(ti):
    orgs_repos_url = ti.xcom_pull(task_ids='processing_orgs')
    top_repos = [worker_repos.run(r) for r in orgs_repos_url]
    top_repos = [j for i in top_repos for j in i]
    top_repos = worker_repos.get_stars_top(top_repos)
    return top_repos


def _insert_sqlite(ti):
    top_repos = ti.xcom_pull(task_ids='processing_repos')
    sqlite_hook = SqliteHook(sqlite_conn_id='sqlite_default')
    target_fields = ['id', 'org_name', 'repo_name', 'stars_count']
    rows = [(r['id'], r['org_name'], r['repo_name'], r['stars_count'])
            for r in top_repos]
    sql = '''
        INSERT INTO top (id, org_name, repo_name, stars_count)
            VALUES (?, ?, ?, ?)
        '''
    for row in rows:
        sqlite_hook.run(sql, parameters=row, autocommit=True)
    # sqlite_hook.insert_rows(table='top', rows=rows,
    #                         target_fields=target_fields)


def _show_rows(ti):
    sqlite_hook = SqliteHook(sqlite_conn_id='sqlite_default')
    sql = 'SELECT id, org_name, repo_name, stars_count FROM top'
    result = sqlite_hook.run(sql, autocommit=True)
    print(result)
    return result


with DAG('git_processing', schedule_interval='@daily',
         default_args=default_args, catchup=False) as dag:

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='git_api',
        endpoint='organizations'
    )

    drop_table = SqliteOperator(
        task_id='drop_table',
        sqlite_conn_id='sqlite_default',
        sql='''
            DROP TABLE IF EXISTS top;
        '''
    )

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='sqlite_default',
        sql='''
            CREATE TABLE IF NOT EXISTS top (
                id INTEGER PRIMARY KEY,
                org_name TEXT,
                repo_name TEXT,
                stars_count TEXT
            );
        '''
    )

    processing_orgs = PythonOperator(
        task_id='processing_orgs',
        python_callable=_processing_orgs,
    )

    processing_repos = PythonOperator(
        task_id='processing_repos',
        python_callable=_processing_repos,
    )

    insert_sqlite = PythonOperator(
        task_id='insert_sqlite',
        python_callable=_insert_sqlite,
    )

    show_rows = PythonOperator(
        task_id='show_rows',
        python_callable=_show_rows,
    )

    # show_rows = SqliteOperator(
    #     task_id='show_rows',
    #     sqlite_conn_id='sqlite_default',
    #     sql='SELECT * from top',
    # )

    is_api_available >> drop_table >> creating_table >> processing_orgs
    processing_orgs >> processing_repos >> insert_sqlite >> show_rows
