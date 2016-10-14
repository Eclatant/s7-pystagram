import time

from celery import Celery

app = Celery(
        __name__,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0')

@app.task #celery worker로 등록함
def add(a, b):
    time.sleep(5)
    result = a+b
    print(result)
    return result

@app.task
def sum2(values):
    time.sleep(3)
    result = sum(values)
    print(type(values), values)
    print(result)
    return result
