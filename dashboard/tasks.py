from . import scrape
from celery import shared_task 

@shared_task
def update_db_country():
    scrape.fetch_api_data()

@shared_task
def update_db_time():
    scrape.update_time_data()
