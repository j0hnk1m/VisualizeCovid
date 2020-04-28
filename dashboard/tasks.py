from . import api
from celery import shared_task 

@shared_task
def update_db():
    api.fetch_api_data()


@shared_task
def asdf():
    print("asdf")
    return "asdf"
