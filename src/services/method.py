from fastapi import Depends
from typing import BinaryIO
from datetime import datetime
from src.db.db import Session, get_session
from src.models.method import Method
from src.models.schemas.utils.method_enum import Methods_Enum
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import pandas as pd


class MethodsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def data_processing(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.dataProcessing
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        df = pd.read_csv(input_file)
        with open('MLmodel/data.csv', 'wb') as fid:
            pickle.dump(df.to_csv(), fid)
        for i in df.columns:
            if df.dtypes[i] == "float64":
                df[i] = df[i].fillna(df[i].mean())
            elif df.dtypes[i] == "int64":
                df[i] = df[i].fillna(df[i].median())
            else:
                df[i] = df[i].fillna(df[i].mode())
        df_labeled = df.copy()
        for i in ['WeekStatus', 'Day_of_week', 'Load_Type']:
            df_labeled[i] = LabelEncoder().fit_transform(df_labeled[i])
        return df_labeled.to_csv(index=False)

    def fit(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.fit
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        df = pd.read_csv(input_file)
        y_train = df["Usage_kWh"]
        X_train = df.drop(["Usage_kWh", "date"], axis=1)
        model = DecisionTreeRegressor().fit(X_train, y_train)
        with open('MLmodel/tree_classifier.pkl', 'wb') as fid:
            pickle.dump(model, fid)

    def predict(self, user_id: int, input_file: BinaryIO):
        method = Method()
        method.method_name = Methods_Enum.predict
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        print(input_file)
        df = pd.read_csv(input_file)
        X = df.drop(["Usage_kWh", "date"], axis=1)
        with open('MLmodel/tree_classifier.pkl', 'rb') as fid:
            model = pickle.load(fid)
            df["Usage_kWh"] = model.predict(X)
            return df.to_csv()

    def download(self, user_id: int):
        method = Method()
        method.method_name = Methods_Enum.download
        method.used_at = datetime.now()
        method.user_id = user_id
        self.session.add(method)
        self.session.commit()
        with open('MLmodel/data.csv', 'rb') as fid:
            data = pickle.load(fid)
            return data
