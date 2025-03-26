from fastapi import FastAPI
import logging
from schema import PassengerData
from model_singleton import ModelSingleton
from tasks import predict

app = FastAPI()

# Logging configuration
logging.basicConfig(level=logging.INFO)


# Instantiate the singleton at the module level
model_singleton = ModelSingleton()

# synchronous endpoint that return prediction
@app.post("/titanic_sync")
async def titanic_sync(data: PassengerData):
    prediction = model_singleton.infer(data)
    return {"prediction": prediction[0]}


@app.post("/titanic_async")
async def titanic_async(data: PassengerData):
    # Convert PassengerData to a dictionary before passing it to Celery
    job = predict.delay(dict(data))
    return {"job_id": job.id}


@app.get("/result/{job_id}")
async def get_result(job_id: str):
    result = predict.AsyncResult(job_id)
    if result.state == "SUCCESS":
        return {"job_id": job_id, "status": result.state, "result": result.result}
    else:
        return {"job_id": job_id, "status": result.state}
