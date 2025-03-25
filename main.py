from fastapi import FastAPI
from celery import Celery
from uuid import uuid4

from schema import PassengerData
from model_singleton import ModelSingleton

app = FastAPI()

# Celery configuration
celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


# Instantiate the singleton at the module level
model = ModelSingleton()

# synchronous endpoint that return prediction
@app.post("/titanic_sync")
async def titanic_sync(data: PassengerData):
    prediction = model.predict(data)
    return {"prediction": prediction[0]}


@app.post("/titanic_async")
async def titanic_async(data: PassengerData):
    job_id = str(uuid4())
    celery.send_task("tasks.predict", args=[job_id, data.dict()])
    return {"job_id": job_id}


@app.get("/result/{job_id}")
async def get_result(job_id: str):
    result = celery.AsyncResult(job_id)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "completed", "result": result.result}
    else:
        return {"status": "failed"}
