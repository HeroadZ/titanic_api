import lightgbm as lgb
import pickle
import pandas as pd
import logging
from schema import PassengerData


class ModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelSingleton, cls).__new__(cls)
            cls._instance.model = lgb.Booster(model_file="models/model_v0.txt")  # Load LightGBM model
            with open('models/category_mapping.pkl', 'rb') as f:
                cls._instance.category_mapping = pickle.load(f)  # Load category mapping
        return cls._instance

    def preprocess_input(self, data: PassengerData) -> pd.DataFrame:
        """Preprocess input data for prediction."""
        df = pd.DataFrame([dict(data)])
        # Drop unnecessary columns
        df = df.drop(columns=['Name', 'Ticket', 'Cabin'], errors='ignore')
        # Map categorical columns
        df['Sex'] = df['Sex'].map(self.category_mapping['sex'])
        df['Embarked'] = df['Embarked'].map(self.category_mapping['embarked'])
        return df
    
    def infer(self, data: PassengerData) -> pd.Series:
        """Make predictions."""
        _data = self.preprocess_input(data)
        result = self.model.predict(_data.values)
        return result
