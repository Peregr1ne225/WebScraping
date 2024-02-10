from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@localhost//')

@app.task
def process_script1():
    from Advice import GetSub as script1_main
    script1_main()

@app.task
def process_script2():
    from JIB import GetSub as script2_main
    script2_main()

# @app.task
# def process_script3():
#     from Banana import GetPath as script3_main
#     script3_main()