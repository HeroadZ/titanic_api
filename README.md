# titanic_api

Code for creation, deployment of a model trained on Titanic data.

# Folder Structure

```
.
├── .gitignore              
├── create_model.ipynb       # Jupyter notebook for training the LightGBM model
├── docker-compose.yml       # Docker Compose configuration for deploying the API and worker
├── Dockerfile               # Dockerfile for building the API container
├── main.py                  # Entry point for the FastAPI application
├── model_singleton.py       # Singleton class for loading and using the trained model
├── poetry.lock              
├── pyproject.toml           # Poetry configuration file for project dependencies
├── README.md                
├── schema.py                # Defines the data schema for API requests
├── tasks.py                 # Celery tasks for background processing
├── data/                    # Folder containing Titanic dataset files
│   ├── gender_submission.csv
│   ├── test.csv
│   ├── train.csv
│   └── train_processed.csv
├── models/                  
│   ├── category_mapping.pkl # Pickle file for categorical mappings
│   └── model_v0.txt         # Trained LightGBM model file
```

# Data Source

https://www.kaggle.com/competitions/titanic/overview

# Usage

## Train Model

### 1. setup environment

```bash
pip install poetry
poetry install
```

### 2. train model

run the `create_model.ipynb` notebook to create a lightgbm model.

## Deploy Model

### 1. setup environment

install docker and [docker-compose](https://docs.docker.com/compose/install/)

### 2. build and run the docker container

```bash
docker-compose up -d --build
```

### 3. test the API

open the browser and go to `http://localhost:8000/docs`, test the api by swagger UI.

### 4. stop the container

```bash
docker-compose down
```
