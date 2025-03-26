from celery import Celery, Task
import logging
import os
from schema import PassengerData
from model_singleton import ModelSingleton


# Celery configuration
celery = Celery(
    "worker",
    broker=os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.environ.get("CELERY_BACKEND_URL", "redis://redis:6379/0"),
)


class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            self.model = ModelSingleton()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@celery.task(bind=True,
             base=PredictTask)
def predict(self, data: dict):
    try:
        prediction = self.model.infer(PassengerData(**data))
        return prediction[0]
    except Exception as e:
        return str(e)
