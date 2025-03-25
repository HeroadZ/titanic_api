from celery import Celery
from model_singleton import ModelSingleton
from schema import PassengerData

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery.task(name="tasks.predict")
def predict(job_id: str, data: PassengerData):
    model = ModelSingleton()
    prediction = model.predict(data)
    return {"job_id": job_id, "prediction": prediction[0]}
